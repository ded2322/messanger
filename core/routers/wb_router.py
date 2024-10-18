from fastapi import APIRouter, WebSocket

from core.services.web_socket_service import WebsocketService

router = APIRouter(prefix="/ws", tags=["Websocket"])


@router.websocket("")
async def websocket_endpoint(websocket: WebSocket):
    await WebsocketService.create_connect(websocket)
