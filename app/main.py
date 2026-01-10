from fastapi import FastAPI
from app.api.v1 import (
    tickets,
    comments,
    users,
    auth,
    admin,
)

app = FastAPI(
    title="Help API",
    description="API de chamados de TI",
    version="0.1.0"
)

# -------------------------
# API v1
# -------------------------
app.include_router(users.router, prefix="/api/v1")
app.include_router(auth.router, prefix="/api/v1")
app.include_router(tickets.router, prefix="/api/v1")
app.include_router(comments.router, prefix="/api/v1")
app.include_router(admin.router, prefix="/api/v1")








@app.get("/health")
def health_check():
    return {"status": "ok"}