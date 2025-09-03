# ============================================= Start Noted UTILS - upload_foto ===================================
# Author : Abdul Rohman Masrifan | https://fastflow.pybot.cloud/ | masrifan26@gmail.com
# ============================================= END Noted UTILS - upload_foto ===================================
from fastapi import UploadFile
from PIL import Image, ImageOps
from pathlib import Path
import os
import uuid
import aiofiles
import boto3
from botocore.exceptions import ClientError
from aiobotocore.session import get_session
from io import BytesIO

# Import utils local
from ..config import ZONA_WAKTU_SERVER, UPLOAD_FOLDER, config, AWS_BUCKET, AWS_SUB_BUCKET, AWS_REGION
import logging


def delete_file(foto_dir, subdir_name, filename):
    if subdir_name:
        del_foto = Path.joinpath(foto_dir, subdir_name, filename)
        if del_foto.is_file():
            os.remove(del_foto)
    else:
        del_foto = Path.joinpath(foto_dir, filename)
        if del_foto.is_file():
            os.remove(del_foto)

def create_folder_foto(foto_dir, subdir_name):
    if subdir_name:
        if not Path.exists(foto_dir / subdir_name):
            Path(foto_dir / subdir_name).mkdir(parents=True, exist_ok=True)
        return foto_dir / subdir_name
    else:
        if not Path.exists(foto_dir):
            Path(foto_dir).mkdir(parents=True, exist_ok=True)
        return foto_dir
    
async def upload_aws_file(index: int | str, file: UploadFile, modul: str = "path", old_files: dict = None):
    filename, fileext = os.path.splitext(file.filename)
    photoname = modul + str(uuid.uuid4()) + fileext
    is_image = file.content_type.startswith("image/")

    if AWS_SUB_BUCKET:
        s3_path = f"{AWS_SUB_BUCKET}/{modul}/{index}"
    else:
        s3_path = f"testing/{modul}/{index}"

    s3 = boto3.client(
        "s3",
        region_name=AWS_REGION,
        aws_access_key_id=config["AWS_ACCESS_KEY_ID"],
        aws_secret_access_key=config["AWS_SECRET_ACCESS_KEY"],
    )

    try:
        # Proses upload
        if is_image:
            result = await process_and_upload_image(file, s3, s3_path, photoname)
        else:
            file_content = await file.read()
            s3.upload_fileobj(
                BytesIO(file_content),
                AWS_BUCKET,
                f"{s3_path}/{filename}",
                ExtraArgs={"ContentType": file.content_type, "ACL": "public-read"},
            )
            result = {
                "fullpath": f"https://{AWS_BUCKET}.s3.{AWS_REGION}.amazonaws.com/{s3_path}/{filename}",
                "path": s3_path,
                "filename": filename,
                "content_type": file.content_type,
            }

        # Hapus file lama jika diberikan
        if old_files and isinstance(old_files, dict):
            for key in ["T", "M", "H", "original"]:
                old_key = old_files.get(key)
                if old_key:
                    try:
                        s3.delete_object(Bucket=old_files.get("bucket", AWS_BUCKET), Key=old_key)
                    except ClientError as e:
                        logging.warning(f"Gagal hapus file lama: {old_key}, error: {e}")

        return result

    except Exception as e:
        logging.error(f"Upload AWS Error: {e}")
        return None


async def process_and_upload_image(file: UploadFile, s3, s3_path: str, photoname: str):
    try:
        file.file.seek(0)
        img = Image.open(file.file._file)
        img = ImageOps.exif_transpose(img)
        width, height = img.size
        fileext = os.path.splitext(file.filename)[1]
        format_img = "JPEG" if fileext[1:].upper() == "JPG" else fileext[1:].upper()

        versions = {
            "T": {"size": (128, 128), "quality": 40},
            "M": {"size": (width, height), "quality": 50},
            "H": {"size": (width, height), "quality": 75}
        }

        for level, props in versions.items():
            file.file.seek(0)
            img = Image.open(file.file._file)
            img = ImageOps.exif_transpose(img)
            if props["size"] != (width, height):
                img.thumbnail(props["size"], Image.LANCZOS)
            else:
                img = img.resize(props["size"], Image.LANCZOS)

            out = BytesIO()
            img.save(out, format_img, quality=props["quality"])
            out.seek(0)
            img.close()

            s3.upload_fileobj(
                out,
                AWS_BUCKET,
                f"{s3_path}/{level}/{photoname}",
                ExtraArgs={"ContentType": file.content_type, "ACL": "public-read"},
            )

        return {
            "fullpath": f"https://{AWS_BUCKET}.s3.{AWS_REGION}.amazonaws.com/{s3_path}/H/{photoname}",
            "path": s3_path,
            "filename": photoname,
            "width": width,
            "height": height,
            "content_type": file.content_type,
        }

    except Exception as e:
        logging.error(f"Image process/upload error: {e}")
        return None

    
# old_filename == untuk replace file
async def upload_image_file(index: int | str, image_file: UploadFile, old_filename: str = None, modul: str = 'path'):
    foto_dir = UPLOAD_FOLDER / modul / str(index)

    create_folder_foto(foto_dir, "")
    foto_dir_t = create_folder_foto(foto_dir, "T")
    foto_dir_m = create_folder_foto(foto_dir, "M")
    foto_dir_h = create_folder_foto(foto_dir, "H")

    filename, fileext = os.path.splitext(image_file.filename)
    photoname = modul + str(uuid.uuid4()) + fileext

    # Simpan foto ke local harddisk
    async with aiofiles.open(foto_dir / image_file.filename, "wb") as saved_file:
        while content := await image_file.read(1024):
            await saved_file.write(content)

    original_file = str(foto_dir / image_file.filename)
    new_file = str(foto_dir / photoname)
    os.rename(original_file, new_file)

    # Create thumbnail
    img = Image.open(new_file)
    img = ImageOps.exif_transpose(img)
    width, height = img.size

    img.thumbnail((128, 128), Image.LANCZOS)
    img.save(foto_dir_t / photoname)
    img.close()

    # Create medium quality
    img = Image.open(new_file)
    img = ImageOps.exif_transpose(img)
    img.resize((width, height), Image.LANCZOS)
    img.save(foto_dir_m / photoname, quality=50)
    img.close()

    # Create high quality
    img = Image.open(new_file)
    img = ImageOps.exif_transpose(img)
    img.resize((width, height), Image.LANCZOS)
    img.save(foto_dir_h / photoname, quality=75)
    img.close()

    if old_filename is not None:
        delete_file(foto_dir, "", old_filename)
        delete_file(foto_dir, "T", old_filename)
        delete_file(foto_dir, "M", old_filename)
        delete_file(foto_dir, "H", old_filename)

    fullpath = os.path.join('static', str(modul), str(index), "H", str(photoname))
    path_simple = os.path.join('static', str(modul), str(index))

    data_foto = {
        "fullpath": fullpath,
        "path": path_simple,
        "filename": photoname,
        "width": width,
        "height": height,
        "content_type": image_file.content_type
    }

    return data_foto

# Params dibawah ini untuk replace file
# old_region
# old_bucket
# old_file_t
# old_file_m
# old_file_h
async def upload_aws_image_file(
    index: int,
    image_file: UploadFile,
    modul: str = 'path',
    old_region: str = None,
    old_bucket: str = None,
    old_file_t: str = None,
    old_file_m: str = None,
    old_file_h: str = None
):
    try:
        # Struktur direktori di S3
        if AWS_SUB_BUCKET is not None:
            foto_dir_s3 = f"{AWS_SUB_BUCKET}/{modul}/{str(index)}"
        else:
            foto_dir_s3 = f"testing/{modul}/{str(index)}"

        filename, fileext = os.path.splitext(image_file.filename)
        if fileext[1:].upper() == "JPG":
            format_img = "JPEG"
        else:
            format_img = fileext[1:].upper()
        photoname = modul + str(uuid.uuid4()) + fileext

        s3 = boto3.client(
            "s3",
            region_name=AWS_REGION,
            aws_access_key_id=config["AWS_ACCESS_KEY_ID"],
            aws_secret_access_key=config["AWS_SECRET_ACCESS_KEY"],
        )

        # Create thumbnail file
        img = Image.open(image_file.file._file)
        img = ImageOps.exif_transpose(img)
        width, height = img.size
        img.thumbnail((128, 128), Image.LANCZOS)

        thumb_file = BytesIO()
        img.save(thumb_file, format_img)
        thumb_file.seek(0)
        img.close()
        try:
            s3.upload_fileobj(
                thumb_file,
                AWS_BUCKET,
                foto_dir_s3 + "/T/" + photoname,
                ExtraArgs={"ContentType": image_file.content_type, "ACL": "public-read"},
                # ExtraArgs={"ContentType": image_file.content_type},
            )
        except ClientError as e:
            logging.error(e)
            return None

        # Create medium quality
        img = Image.open(image_file.file._file)
        img = ImageOps.exif_transpose(img)
        width, height = img.size
        img.resize((width, height), Image.LANCZOS)

        med_file = BytesIO()
        img.save(med_file, format_img, quality=50)
        med_file.seek(0)
        img.close()
        try:
            s3.upload_fileobj(
                med_file,
                AWS_BUCKET,
                foto_dir_s3 + "/M/" + photoname,
                ExtraArgs={"ContentType": image_file.content_type, "ACL": "public-read"},
                # ExtraArgs={"ContentType": image_file.content_type},
            )
        except ClientError as e:
            logging.error(e)
            return None

        # Create high quality
        img = Image.open(image_file.file._file)
        img = ImageOps.exif_transpose(img)
        width, height = img.size
        img.resize((width, height), Image.LANCZOS)

        high_file = BytesIO()
        img.save(high_file, format_img, quality=75)
        high_file.seek(0)
        img.close()
        try:
            s3.upload_fileobj(
                high_file,
                AWS_BUCKET,
                foto_dir_s3 + "/H/" + photoname,
                ExtraArgs={"ContentType": image_file.content_type, "ACL": "public-read"},
                # ExtraArgs={"ContentType": image_file.content_type},
            )
        except ClientError as e:
            logging.error(e)
            return None
        
        if old_region is not None:
            try:
                s3 = boto3.client(
                    "s3",
                    region_name=old_region,
                    aws_access_key_id=config["AWS_ACCESS_KEY_ID"],
                    aws_secret_access_key=config["AWS_SECRET_ACCESS_KEY"],
                )
                s3.delete_object(Bucket=old_bucket, Key=old_file_t)
                s3.delete_object(Bucket=old_bucket, Key=old_file_m)
                s3.delete_object(Bucket=old_bucket, Key=old_file_h)
            except ClientError as e:
                logging.error(e)

        fullpath = f"https://{AWS_BUCKET}.s3.{AWS_REGION}.amazonaws.com/{foto_dir_s3}/H/{photoname}"

        data_foto = {
            "fullpath": fullpath,
            "path": foto_dir_s3,
            "filename": photoname,
            "width": width,
            "height": height,
            "content_type": image_file.content_type
        }

        return data_foto
    except Exception as e:
        logging.error(f"Exception AWS Upload : {e}")
        return None
    
async def upload_to_s3_from_local(file_path: str, s3_path: str):
    try:
        s3 = boto3.client(
            "s3",
            region_name=AWS_REGION,
            aws_access_key_id=config["AWS_ACCESS_KEY_ID"],
            aws_secret_access_key=config["AWS_SECRET_ACCESS_KEY"],
        )

        # Upload file
        s3.upload_file(file_path, AWS_BUCKET, s3_path, ExtraArgs={"ACL": "public-read"})

        # URL publik dari objek
        fullpath = f"https://{AWS_BUCKET}.s3.{AWS_REGION}.amazonaws.com/{s3_path}"

        return {"fullpath": fullpath}

    except Exception as e:
        logging.error(f"Error uploading to S3: {e}")
        return None