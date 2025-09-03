# middleware/logging_middleware.py
import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from core.utils.log import setup_custom_logger
from jose import JWTError, jwt
from typing import Optional
from core.utils.token import SECRET_KEY

# Inisialisasi logger khusus untuk request log
logger = setup_custom_logger("api_logger", "api_request.log")

# Fungsi bantu ambil user ID dari token Authorization: Bearer ...
def extract_user_id_from_token(auth_header: Optional[str]) -> str:
    if not auth_header or not auth_header.startswith("Bearer "):
        return "anonymous"
    token = auth_header.split(" ")[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return str(payload.get("sub") or "unknown")
    except JWTError:
        return "invalid_token"

# Middleware logging
class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        ip = request.client.host
        user_agent = request.headers.get("user-agent", "unknown")
        auth_header = request.headers.get("authorization")
        user_id = extract_user_id_from_token(auth_header)

        response = await call_next(request)
        process_time = round((time.time() - start_time) * 1000, 2)

        log_message = (
            f"{ip} | {request.method} {request.url.path} | "
            f"UserID: {user_id} | UA: {user_agent} | "
            f"Status: {response.status_code} | Time: {process_time}ms"
        )

        logger.info(log_message)

        return response
