# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from main_router import main_router
from chat_router import chat_router
import uvicorn

def create_app():
    app = FastAPI()

    origins = ["*"]
    # Enable CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(main_router, prefix="/", tags=["main"])
    app.include_router(chat_router, prefix="/chat", tags=["chat"])

    return app

app = create_app()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
