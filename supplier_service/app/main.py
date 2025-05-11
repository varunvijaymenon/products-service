from fastapi import FastAPI
from .routes import router
import uvicorn

app = FastAPI(title="Supplier Service API with RabbitMQ", version="1.0.0")
app.include_router(router)


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8082, reload=True)
