from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from .token import verify_token
from .response_handle import show_unauthorized

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    response_unauth = show_unauthorized()
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=response_unauth,
        headers={"WWW-Authenticate": "Bearer"},
    )

    return verify_token(token, credentials_exception)
