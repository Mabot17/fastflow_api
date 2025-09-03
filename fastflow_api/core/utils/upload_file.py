from fastapi import UploadFile
import os

async def save_uploaded_file(upload_folder: str, file: UploadFile) -> str:
    # Pastikan direktori ada
    os.makedirs(upload_folder, exist_ok=True)
    
    # Tentukan lokasi penyimpanan file
    file_location = os.path.join(upload_folder, file.filename)
    
    # Simpan file
    with open(file_location, "wb") as file_object:
        file_object.write(file.file.read())
    
    return file_location
