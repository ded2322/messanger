from fastapi import HTTPException

from core.orm.user_orm import UserOrm
from core.schemas.users_schemas import UserDataRegisterSchema, UserDataLoginSchema
from core.utils.auth import get_password_hash, create_access_token
from core.utils.user_validator import UserValidator, AuthCheck

class AuthService:
    @classmethod
    async def register_user(cls, data_user: UserDataRegisterSchema):
        """Регистрация. Создает запись пользователя в таблице users"""

        await UserValidator.validate_fields(data_user)
        await UserValidator.validate_name_availability(data_user.name)

        hash_password = get_password_hash(data_user.password)

        await UserOrm.insert_data(name=data_user.name, password=hash_password)

        return {"message": "User registered successfully"}


    @classmethod
    async def login_user(cls,response, data_user: UserDataLoginSchema):
        """Аутентификация пользователя и возврат токена."""

        user = await AuthCheck.get_user_info(name=data_user.name)

        if await UserValidator.validate_login_credentials(user, data_user):
                raise HTTPException(status_code=401, detail="Invalid credentials")

        #response.set_cookie("access_token", create_access_token({"sub": str(user["id"])}), httponly=True)
        return create_access_token({"sub": str(user["id"])})
        #return {"message": "User logged successfully"}
