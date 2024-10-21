from pydantic import ValidationError
from fastapi import WebSocket, WebSocketException

from core.schemas.message_schemas import WebSocketDataSchema
from core.logs.logs import logger_websocket

class WebsocketValidator:
    """Класс для валидации данных WebSocket"""
    @classmethod
    async def validate_recent_message(cls, data_json: str) -> WebSocketDataSchema:
        """Валидирует данные по схеме WebSocketDataSchema."""
        try:
            websocket_data = WebSocketDataSchema.parse_raw(data_json)

            if not await cls.check_data(websocket_data.message) or not await cls.check_data(websocket_data.token):
                raise ValueError("Empty message or token")

            return websocket_data
        except (ValidationError, ValueError) as e:
            logger_websocket.error(f"Invalid message format: {str(e)}")
            raise WebSocketException(code=1003, reason="Invalid message format")


    @classmethod
    async def check_data(cls, data_check: str) -> bool:
        return data_check.isspace() and data_check is not None
