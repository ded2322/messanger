from fastapi import HTTPException

from core.orm.user_orm import UserOrm
from core.schemas.users_schemas import UserDataRegisterSchema, UserDataLoginSchema
from core.utils.auth import verification_password


class AuthCheck:
    @classmethod
    async def check_username_exists(cls, **kwargs) -> bool:
        return await UserOrm.found_one_or_none(**kwargs) is not None

    @classmethod
    async def get_user_info(cls, **kwargs) -> dict :
        """Возвращает информацию о пользователе по заданным критериям"""
        user_data = await UserOrm.found_one_or_none(**kwargs)
        if not user_data:
            raise HTTPException(status_code=404, detail="User not found")
        return user_data


class UserValidator:
    @classmethod
    async def validate_fields(cls, data_user: UserDataRegisterSchema):
        """Проверяет данные при регистрации"""
        if not data_user.name or not data_user.password:
            raise HTTPException(status_code=401, detail="Fields cannot be empty")

    @classmethod
    async def validate_name_availability(cls, name: str):
        """Проверяет, занято ли имя пользователя."""
        if await UserOrm.found_one_or_none(name=name):
            raise HTTPException(status_code=409, detail="Name is occupied")

    @classmethod
    async def validate_login_credentials(cls, user, data_user: UserDataLoginSchema):
        """Проверяет, существует ли пользователь и правильный ли пароль."""
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if not verification_password(data_user.password, user["password"]):
            raise HTTPException(status_code=401, detail="Invalid credentials")

    @classmethod
    def check_availability_user(cls, user_data):
        if not user_data:
            raise HTTPException(status_code=404, detail="User not found")
