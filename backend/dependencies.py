import dotenv, httpx, random, string
from datetime import datetime
from .database.repositories.websiteRepository import WebsiteRepository
from .database.repositories.checkLogRepository import CheckLogRepository
import time

def generate_token():
    return "".join(random.choices(string.ascii_lowercase+string.ascii_uppercase+string.digits, k=20))

def get_user_id_by_token(X_TOKEN):
    tokens = dotenv.dotenv_values(".env").items()
    for user_token in tokens:
        if user_token[1] == X_TOKEN:
            return int(user_token[0])

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