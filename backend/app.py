import httpx
from dotenv import load_dotenv, get_key
from datetime import timedelta
from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from backend.routers import user, website
from .dependencies import authenticate_user, create_access_token
from .models.user import UserAuth
from .dependencies import get_current_user

load_dotenv()

app = FastAPI()

app.add_middleware(CORSMiddleware,
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"],
                   allow_origins=["*"])

app.include_router(user.router)
app.include_router(website.router)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get('/')
def notification():
    return {"message": "You're already logged"}

@app.post('/token')
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(UserAuth(email=form_data.username, password=form_data.password))

    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password", headers={"WWW-Authenticate": "Bearer"})

    access_token_expire_minutes = timedelta(minutes=int(get_key(".env", "ACCESS_TOKEN_EXPIRE_MINUTES")))
    access_token = create_access_token(data={"sub": user.get("email")}, expires_delta=access_token_expire_minutes)

    return JSONResponse({"access_token": access_token, "token_type": "bearer"})

@app.post('/users/me')
def current_user(token: str = Depends(oauth2_scheme)):
    return JSONResponse(get_current_user(token), status_code=200)