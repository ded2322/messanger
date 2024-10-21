import asyncio
import websockets
import json

async def connect_to_server(token):
    """
    Подключается к WebSocket-серверу, передает токен и отправляет сообщения.
    Постоянно прослушивает входящие сообщения.
    """
    # Формируем URL для подключения с токеном
    uri = f"ws://localhost:8000/ws?token={token}"

    async with websockets.connect(uri) as websocket:
        print("Соединение установлено")

        # Отправляем сообщение серверу (можно отправлять циклически или при каком-то событии)
        message = {
            "recipient_id": 1,  # ID получателя
            "message": "Привет, как дела?"
        }
        await websocket.send(json.dumps(message))
        print(f"Отправлено сообщение: {message}")

        # Постоянно прослушиваем входящие сообщения
        try:
            while True:
                # Получаем входящее сообщение
                incoming_message = await websocket.recv()
                print(f"Новое сообщение: {incoming_message}")
        except websockets.exceptions.ConnectionClosed:
            print("Соединение закрыто")
        except Exception as e:
            print(f"Ошибка: {str(e)}")

# Асинхронный запуск клиента
token = "token"  # Замените на действительный токен
asyncio.get_event_loop().run_until_complete(connect_to_server(token))

