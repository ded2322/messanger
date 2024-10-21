import json
from datetime import datetime

from fastapi import WebSocket, WebSocketDisconnect

from core.utils.websocket import manager
from core.orm.messages_orm import MessagesOrm
from core.orm.user_orm import UserOrm
from core.logs.logs import logger_websocket



class WebsocketSerializer:
    @staticmethod
    async def serialize_message(user_id: int, message: str, date_send: list):
        """Сериализует данные в json"""
        data_user = await UserOrm.found_one_or_none(id=user_id)


        data = {
            "user_id": data_user["id"],
            "name": data_user["name"],
            "message": message,
            "message_id": date_send[1],
            "time_send": date_send[0],
        }

        return json.dumps(data)


class WebsocketMessageAddDB:
    @staticmethod
    async def add_message_db(user_id: int, message: str) -> list:
        """
        Добавляет данные в базу данных.
        Возвращает время когда было отправлено сообщение
        """
        current_time = datetime.now().time()
        #todo секунды убрать, текущее время?
        formatted_time = current_time.strftime("%H:%M:%S")
        time_object = datetime.strptime(formatted_time, "%H:%M:%S").time()

        # Добавляем в базу данных сообщение
        id_column = await MessagesOrm.insert_data(
            user_id=user_id, message=message, time_send=time_object
        )
        return [formatted_time, id_column]


class WebsocketService:
    @classmethod
    async def create_connect(cls, websocket: WebSocket, user_id:int):
        """
        Устанавливает WebSocket соединение и сохраняет его для личных сообщений.
        """

        # Подключаем пользователя и сохраняем его WebSocket соединение
        await manager.connect(websocket, user_id)
        logger_websocket.info(f"User {user_id} connected")

        try:
            while True:
                # Получаем сообщение от пользователя
                data_json = await websocket.receive_text()
                data = json.loads(data_json)

                # Обрабатываем сообщение
                await cls.process_message(user_id, data, websocket)

        except WebSocketDisconnect:
            logger_websocket.info(f"User {user_id} disconnected")
            await manager.disconnect(user_id)
        except Exception as e:
            logger_websocket.error(f"Error in create_connect: {str(e)}")

    @classmethod
    async def process_message(cls, sender_id: int, data: dict, websocket: WebSocket):
        """
        Обрабатывает входящее сообщение и направляет его получателю.
        data должен содержать 'recipient_id' и 'message'.
        """
        recipient_id = data.get("recipient_id")
        message = data.get("message")

        if not recipient_id or not message:
            await cls.send_user_message("Invalid message format", websocket)
            return

        # Отправляем личное сообщение получателю
        await cls.handle_private_message(sender_id, recipient_id, message)

    @classmethod
    async def handle_private_message(cls, sender_id: int, recipient_id: int, message: str):
        """
        Отправляем личное сообщение от одного пользователя другому.
        """
        # Добавляем сообщение в базу данных
        date_sender = await WebsocketMessageAddDB.add_message_db(sender_id, message)

        # Сериализуем сообщение для отправки
        serialized_message = await WebsocketSerializer.serialize_message(
            sender_id, message, date_sender
        )

        # Отправляем сообщение получателю через менеджер
        await manager.send_personal_message(serialized_message, recipient_id)

    @classmethod
    async def send_user_message(cls, message: str, websocket: WebSocket):
        """
        Отправляет персональное сообщение пользователю.
        """
        data_send = {"event": "send user message", "message": message}
        if websocket.client_state.name == "CONNECTED":
            await websocket.send_text(json.dumps(data_send))
        else:
            logger_websocket.warning("Skipped sending message to closed connection")
