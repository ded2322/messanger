from datetime import datetime, timedelta

from fastapi.responses import JSONResponse
from jose import ExpiredSignatureError, JWTError, jwt
from passlib.context import CryptContext

from core.config import settings

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def verification_password(input_password, hashed_password) -> bool:
    """Проверяет соответствие введённого пароля и хешированного пароля."""
    return pwd_context.verify(input_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_jwt_user_id(token: str) -> str | JSONResponse:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
        return payload.get("sub")
    except (ExpiredSignatureError, JWTError) as e:
        if isinstance(e, ExpiredSignatureError):
            return JSONResponse(
                status_code=401, content={"detail": "The access token has expired"}
            )
        if isinstance(e, JWTError):
            return JSONResponse(
                status_code=401, content={"detail": "Invalid access token format"}
            )


class DecodeJWT:
    @staticmethod
    def decode_jwt(jwt_token: str) -> int:
        return int(decode_jwt_user_id(jwt_token))
