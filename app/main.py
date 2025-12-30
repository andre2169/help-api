from fastapi import FastAPI
from app.routers import users
from app.db.session import engine
from app.db.base import Base
from app.routers import tickets
from app.routers import auth


app = FastAPI(
    title="Help API",
    description="API de chamados de TI",
    version="0.1.0"
)


app.include_router(users.router)
app.include_router(tickets.router)
app.include_router(auth.router)



@app.get("/health")
def health_check():
    return {"status": "ok"}
