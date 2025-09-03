from datetime import datetime, timedelta
from typing import Optional
from jose import jwt, JWTError
from typing import Optional
from pydantic import BaseModel

SECRET_KEY = "fastflowinfinity2025"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 30

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    sub: Optional[str] = None
    user_id: Optional[int] = None
    user_name: Optional[str] = None
    grup: Optional[str] = None


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # logging.debug(f"payload: {payload}")
        sub: str = payload.get("sub")
        user_id: int = payload.get("user_id")
        user_name: str = payload.get("user_name")
        grup: str = payload.get("grup")

        if sub is None:
            raise credentials_exception
        return TokenData(sub=sub, user_id=user_id, user_name=user_name, grup=grup)
    except JWTError:
        raise credentials_exception
