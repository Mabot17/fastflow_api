from pathlib import Path
from dotenv import dotenv_values

ZONA_WAKTU_SERVER = "Asia/Jakarta"

config = dotenv_values(Path(__file__).parent / ".env")
UPLOAD_FOLDER = Path(config["STATIC_FILES_FOLDER"])

ROOT_PATH = config["ROOT_PATH"]
ENABLE_SISTEM_JOB = int(config["ENABLE_SISTEM_JOB"])

AWS_BUCKET = config["AWS_BUCKET"]
AWS_SUB_BUCKET = config["AWS_SUB_BUCKET"]
AWS_REGION = config["AWS_REGION"]

SMS_ENABLED = False

MAX_PHOTO_PER_POST = 4
MAX_VIDEO_PER_POST = 1

# Setup env PATH
WKHTMLTOPDF_PATH = config["WKHTMLTOPDF_PATH"]

# Setup ENV EMAIL
MAIL_USERNAME = config["MAIL_USERNAME"]
MAIL_PASSWORD = config["MAIL_PASSWORD"]
MAIL_FROM = config["MAIL_FROM"]
MAIL_PORT = config["MAIL_PORT"]
MAIL_SERVER = config["MAIL_SERVER"]
MAIL_FROM_NAME = config["MAIL_FROM_NAME"]
MAIL_TLS = config["MAIL_TLS"]
MAIL_SSL = config["MAIL_SSL"]

WABLAS_TOKEN = config["WABLAS_TOKEN"]
WABLAS_SECRET_KEY = config["WABLAS_SECRET_KEY"]