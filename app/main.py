from fastapi import FastAPI
from app.routers import users
from app.db.session import engine
from app.db.base import Base
from app.routers import tickets


app = FastAPI(
    title="Help API",
    description="API de chamados de TI",
    version="0.1.0"
)

Base.metadata.create_all(bind=engine)
app.include_router(users.router)
app.include_router(tickets.router)



@app.get("/health")
def health_check():
    return {"status": "ok"}
