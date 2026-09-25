from fastapi import APIRouter, FastAPI, Depends, Header, HTTPException
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from contextlib import asynccontextmanager
from ..database.repositories.websiteRepository import WebsiteRepository
from ..models.website import WebsiteRequest
from ..dependencies import get_current_user, check_websites
from ..utils.scheduler import scheduler

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    
    # scheduler.start()

    yield

    # scheduler.shutdown()


router = APIRouter(lifespan=lifespan)

@router.post('/api/websites')
def add_website(website: WebsiteRequest, repo: WebsiteRepository = Depends(), token: str = Header()):
    user_id = get_current_user(token)["id"]
    if user_id == None:
        raise HTTPException(status_code=401, detail="User is not authorized")
    repo.insert_website(user_id, website.name, website.url)

    return JSONResponse({"message": "Website has been added"}, status_code=201)
    
@router.get('/api/websites')
def show_websites_of_user(repo: WebsiteRepository = Depends(), token: str = Header()):
    user_id = get_current_user(token)
    if user_id == None:
        raise HTTPException(status_code=401, detail="User is not authorized")
    res = repo.get_websites_by_user_id(user_id)

    return JSONResponse(res, status_code=200)

@router.get('/api/websites/{id}/stats')
def check_status(id: int, repo: WebsiteRepository = Depends(), token: str = Header()):
    user_id = get_current_user(token)
    if user_id == None:
        raise HTTPException(status_code=401, detail="User is not authorized")

    res = repo.get_website_by_id(id)

    return JSONResponse(res, status_code=200)

@router.get('/api-admin/websites')
def admin_show_all_websites(repo: WebsiteRepository = Depends()):
    res = repo.get_all_websites()
    return JSONResponse(res)

@router.delete('/api-admin/websites/{id}')
def admin_remove_website_by_id(id: int, repo: WebsiteRepository = Depends()):
    repo.delete_website_by_id(id)
    return JSONResponse({"message": "Website has been removed"}, status_code=200)