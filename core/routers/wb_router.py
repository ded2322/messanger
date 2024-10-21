from fastapi import APIRouter, WebSocket, Query

from core.services.websocket_service import WebsocketService
from core.utils.auth import DecodeJWT
router = APIRouter(prefix="/ws", tags=["Websocket"])


@router.websocket("")
async def websocket_endpoint(websocket: WebSocket, token: str = Query(...)):
    """
    WebSocket-роутер с проверкой токена перед подключением.
    Пример подключения: ws://your-server-url/ws?token=your_jwt_token
    """
    # Проверяем токен перед тем, как принять соединение
    try:
        user_id = DecodeJWT.decode_jwt(token)
        if not user_id:
            # Если токен недействителен, закрываем соединение с кодом 1008 (некорректный токен)
            await websocket.close(code=1008, reason="Invalid token")
            return
    except Exception as e:
        # Закрываем соединение, если произошла ошибка декодирования токена
        await websocket.close(code=1008, reason="Token verification failed")
        return

    # Передаём WebSocket и user_id в WebsocketService для обработки
    await WebsocketService.create_connect(websocket, user_id)
