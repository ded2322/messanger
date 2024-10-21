from fastapi import WebSocket

from core.logs.logs import logger_websocket

class WebSocketManager:
    def __init__(self):
        self.active_connections: dict[int, WebSocket] = {}

    async def connect(self, websocket: WebSocket, user_id: int):
        """Добавляем соединение для конкретного пользователя."""
        await websocket.accept()
        self.active_connections[user_id] = websocket

    def disconnect(self, user_id: int):
        """Удаляем соединение, если пользователь отключился."""
        if user_id in self.active_connections:
            del self.active_connections[user_id]

    async def send_personal_message(self, message: str, user_id: int):
        """Отправляем сообщение конкретному пользователю."""
        websocket = self.active_connections.get(user_id)
        if websocket and websocket.client_state.name == "CONNECTED":
            await websocket.send_text(message)
        else:
            logger_websocket.warning(f"User {user_id} not connected")

    async def close_connection(self, user_id: int):
        """Закрываем соединение пользователя."""
        websocket = self.active_connections.get(user_id)
        if websocket:
            await websocket.close()


manager = WebSocketManager()
