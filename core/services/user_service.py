from core.utils.auth import DecodeJWT,get_password_hash
from core.orm.user_orm import UserOrm
from core.schemas.users_schemas import JWTTokenSchema, UserUpdateDataSchema
from core.utils.validator import UserValidator, AuthCheck


class UserService:
    @classmethod
    async def show_all_users(cls):
        """Возвращает всех пользователей из базы данных"""
        return await UserOrm.all_users()

    @classmethod
    async def update_data_user(cls, data_update: UserUpdateDataSchema, jwt_token: JWTTokenSchema):
        """Обновляет данные пользователя на основе предоставленной информации."""

        # Декодируем токен и получаем данные пользователя
        user_data = await AuthCheck.get_user_info(id=DecodeJWT.decode_jwt(jwt_token.token))

        # Валидируем наличие пользователя
        UserValidator.check_availability_user(user_data)

        # Собираем поля для обновления
        update_fields = {}

        if data_update.name:
            await UserValidator.validate_name_availability(data_update.name)
            update_fields["name"] = data_update.name

        if data_update.password:
            update_fields["password"] = get_password_hash(data_update.password)

        if update_fields:
            await UserOrm.update_data(id=user_data["id"], **update_fields)

        return {"message": "Data updated successfully"}


    @classmethod
    async def delete_user(cls, jwt_token: JWTTokenSchema):
        """
        Удаляет пользователя на основе его токена.
        Присваивает пользователю имя вида 'Удалённый #ID' и сбрасывает пароль.
        """

        user_data = await AuthCheck.get_user_info(id=DecodeJWT.decode_jwt(jwt_token.token))
        UserValidator.check_availability_user(user_data)

        update_fields = {
            "name": f"Удаленный # {user_data['id']}",
            "password": get_password_hash(user_data["password"]),
        }

        await UserOrm.update_data(id=user_data['id'], **update_fields)

        return {"message": "User deleted successfully"}