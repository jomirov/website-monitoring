import dotenv, httpx, time
from datetime import datetime, timedelta
from .database.repositories.websiteRepository import WebsiteRepository
from .database.repositories.checkLogRepository import CheckLogRepository
from .database.repositories.userRepository import UserRepository
from .models.user import UserAuth

def check_url(url):
    res = httpx.get(url)

    status_code = res.status_code
    response_time_ms = res.elapsed.microseconds
    is_up = True if status_code == 200 else False
    checked_at = datetime.now()

    return {
        "status_code": status_code,
        "response_time_ms": response_time_ms,
        "is_up": is_up,
        "checked_at": checked_at
    }

def check_websites():
    w_repo = WebsiteRepository()
    cl_repo = CheckLogRepository()
    
    websites = w_repo.get_websites_need_to_check()

    if len(websites) != 0:
        for w in websites:
            w_id = w["id"]
            w_url = w["url"]
            w_check_interval = w["check_interval"]

            check_logs = cl_repo.get_logs_by_website_id(w_id)
            if len(check_logs) == 0:
                pass
            elif datetime.timestamp(check_logs[-1]["checked_at"]) > time.time() - w_check_interval:
                continue

            status = check_url(w_url)
            
            cl_repo.add_check_log(w_id, 
                                status["status_code"],
                                status["response_time_ms"],
                                status["is_up"],
                                status["checked_at"])

import jwt
from pwdlib import PasswordHash

def authenticate_user(form: UserAuth):
    repo = UserRepository()
    password_hash = PasswordHash.recommended()

    user = repo.get_user_by_email(form.email)
    if not user:
        return False
    if not password_hash.verify(form.password, user.get("hashed_password")):
        return False
    
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()

    if timedelta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=5)

    to_encode.update({"exp":expire})

    SECRET_KEY = dotenv.get_key(".env", "SECRET_KEY")
    ALGORITHM = dotenv.get_key(".env", "ALGORITHM")
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return token

def get_current_user(token):
    repo = UserRepository()
    data = jwt.decode(token, SECRET_KEY=dotenv.get_key(".env", "SECRET_KEY"), algorithms=[dotenv.get_key(".env", "ALGORITHM")])

    email = data.get("sub")
    
    return repo.get_user_by_email(email)