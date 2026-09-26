from fastapi import APIRouter, FastAPI, Depends, Body, HTTPException
from fastapi.responses import JSONResponse
from fastapi.security.oauth2 import OAuth2PasswordBearer
from dotenv import load_dotenv
from contextlib import asynccontextmanager
from ..database.repositories.websiteRepository import WebsiteRepository
from ..database.repositories.checkLogRepository import CheckLogRepository
from ..models.website import WebsiteRequest, UpdateValues
from ..dependencies import get_current_user
from ..utils.scheduler import scheduler

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    
    scheduler.start()

    yield

    scheduler.shutdown()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter(lifespan=lifespan)

@router.post('/api/websites')
def add_website(website: WebsiteRequest, repo: WebsiteRepository = Depends(), token: str = Depends(oauth2_scheme)):
    user_id = get_current_user(token)["id"]
    if user_id == None:
        raise HTTPException(status_code=401, detail="User is not authorized")
    repo.insert_website(user_id, website.name, website.url)

    return JSONResponse({"message": "Website has been added"}, status_code=201)
    
@router.get('/api/websites')
def show_websites_of_user(repo: WebsiteRepository = Depends(), token: str = Depends(oauth2_scheme)):
    user_id = get_current_user(token)["id"]
    if user_id == None:
        raise HTTPException(status_code=401, detail="User is not authorized")
    res = repo.get_websites_by_user_id(user_id)

    return JSONResponse(res, status_code=200)

@router.get('/api/websites/{id}/stats')
def check_status(id: int, w_repo: WebsiteRepository = Depends(), cl_repo: CheckLogRepository = Depends(), token: str = Depends(oauth2_scheme)):
    user_id = get_current_user(token)["id"]
    if user_id == None:
        raise HTTPException(status_code=401, detail="User is not authorized")
    try:
        res = w_repo.get_website_by_id(id)
    except:
        raise HTTPException(status_code=404, detail="Website is not found")
    logs = cl_repo.get_logs_by_website_id(res["id"])

    return JSONResponse({"website": res, "check_logs": logs}, status_code=200)

@router.delete('/api/websites/{id}')
def remove_website_by_id(id: int, repo: WebsiteRepository = Depends(), token: str = Depends(oauth2_scheme)):
    repo.delete_website_by_id(id)
    return JSONResponse({"message": "Website has been removed"}, status_code=200)

@router.put('/api/websites/{id}')
def change_website(id: int, repo: WebsiteRepository = Depends(), token: str = Depends(oauth2_scheme), updated_values: UpdateValues = Body()):
    repo.update_website_check_interval(id, updated_values.check_interval)
    repo.update_website_is_active(id, updated_values.is_active)
    return JSONResponse({"message": "Website has been updated"}, status_code=200)