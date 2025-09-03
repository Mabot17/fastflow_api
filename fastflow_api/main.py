import pendulum
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError

#Import api_router.py
from core.router import api_router
from core.router.api_metadata import TITLE_API, TAGS_METADATA_API, DESCRIPTION_API, VERSI_API
from core.router.api_middleware import validation_exception_handler, api_middleware_response
from core.router.api_log_middleware import LoggingMiddleware

from core.utils import log
from core import config

logger = log.setup_custom_logger("root")
pendulum.set_locale("id")


app = FastAPI(
    title=TITLE_API,
    version=VERSI_API,
    openapi_tags=TAGS_METADATA_API,
    description=DESCRIPTION_API,
    root_path=config.ROOT_PATH
)

# Mount static files
app.mount("/static", StaticFiles(directory=str(config.UPLOAD_FOLDER)), name="static")
app.include_router(api_router.apiSettings)

# CORS Middleware
origins = ["*"]

app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_middleware(LoggingMiddleware)
app.middleware("http")(api_middleware_response)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)