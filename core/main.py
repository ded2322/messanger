from fastapi import FastAPI, Request
# from fastapi.middleware.cors import CORSMiddleware
# from starlette.responses import JSONResponse

from core.routers.user_router import router_auth
from core.routers.user_router import  router_user
from core.routers.wb_router import router as websocket_router
from core.routers.message_router import router as message_router



app = FastAPI(title="Real-time chat", version="1")

app.include_router(router_auth)
app.include_router(router_user)
app.include_router(websocket_router)
app.include_router(message_router)

#
# origins = ["localhost"]
#
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
#     allow_headers=[
#         "Content-Type",
#         "Set-Cookie",
#         "Access-Control-Allow-Headers",
#         "Access-Control-Allow-Origin",
#         "Authorization",
#     ],
# )
#
# @app.exception_handler(ValueError)
# async def exception_handler(request: Request, exc):
#     return JSONResponse(
#         status_code=400,
#         content={"detail": str(exc)},
#     )