# main.py
from fastapi import FastAPI
from database import Base, engine
from models import User
from auth import router as auth_router
import uvicorn

app = FastAPI(title="GostStorageAPI")

# создаём таблицы в базе
Base.metadata.create_all(bind=engine)

# подключаем маршруты
app.include_router(auth_router)

@app.get("/")
def read_root():
    return {"message": "Добро пожаловать в API!"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)