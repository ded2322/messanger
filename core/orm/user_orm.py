from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from core.orm.base_orm import BaseOrm
from core.database import async_session_maker
from core.logs.logs import logger_error
from core.models.users_models import Users


class UserOrm(BaseOrm):
    model = Users

    @classmethod
    async def all_users(cls):
        """Возвращает всех пользователей"""
        async with async_session_maker() as session:
            try:
                """'''
                SELECT users.id as user_id, users.name
                FROM users
                '''"""
                query = select(cls.model.id.label("user_id"),cls.model.name.label("username"))
                result = await session.execute(query)
                return result.mappings().all()
            except (SQLAlchemyError, Exception) as e:
                if isinstance(e, SQLAlchemyError):
                    logger_error.error(f"SQLAlchemy exc in select_user_info: {str(e)}")
                else:
                    logger_error.error(f"Unknown exc in select_user_info: {str(e)}")
