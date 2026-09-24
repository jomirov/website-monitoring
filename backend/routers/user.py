from fastapi import APIRouter, Depends, HTTPException, Cookie
from fastapi.responses import JSONResponse
from ..database.models.user import UserRequest
from ..database.repositories.userRepository import UserRepository

router = APIRouter()

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