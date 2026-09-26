from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from fastapi.security.oauth2 import OAuth2PasswordBearer
from ..models.user import UserRequest
from ..database.repositories.userRepository import UserRepository
from ..database.repositories.telegramRepository import TelegramRepository
from ..dependencies import get_current_user

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post('/api/users')
def make_user(user: UserRequest, repo: UserRepository = Depends()):
    
    try:
        repo.add_user(user.email, user.password)
    except:
        raise HTTPException(status_code=400, detail="User email is already registered")
    return JSONResponse({"message": "User has been created", "status_code": 201}, status_code=201)

@router.get('/api/users')
def show_all_users(repo: UserRepository = Depends()):
    users = repo.get_all_users()
    return JSONResponse(users, status_code=200)

@router.get('/api/users/{id}')
def show_user_by_id(id: int, repo: UserRepository = Depends()):
    user = repo.get_user_by_id(id)
    
    return JSONResponse(user, status_code=200)

@router.delete('/api/users/{id}')
def remove_user_by_id(id: int, repo: UserRepository = Depends()):
    if repo.delete_user_by_id(id) == None:
        raise HTTPException(status_code=404, detail="User is not found")

    return JSONResponse({"message": "User has been deleted"}, status_code=200)

@router.post('/api/users/telegram')
def add_telegram_session(chat_id: int = Query(), repo: TelegramRepository = Depends(), token: str = Depends(oauth2_scheme)):
    try:
        user_id = get_current_user(token)["id"]
    except:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    repo.insert_session(user_id, chat_id)

    return JSONResponse({"message": "Telegram session has been added"}, status_code=200)