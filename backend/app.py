from fastapi import FastAPI
from backend.routers import user, website


app = FastAPI()

app.include_router(user.router)
app.include_router(website.router)