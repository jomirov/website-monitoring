from ..db import engine
from ..models.check_log import Check_log
from sqlalchemy import select
from sqlalchemy.orm import Session

class CheckLogRepository:
    def add_check_log(self, website_id, 
                      status_code, 
                      response_time_ms, 
                      is_up, 
                      checked_at):
        with Session(engine) as session:
            l = Check_log(website_id=website_id,
                           status_code=status_code,
                           response_time_ms=response_time_ms,
                           is_up=is_up,
                           checked_at=checked_at)
            session.add(l)
            session.commit()

    def get_logs_by_website_id(self, website_id):
        with Session(engine) as session:
            res = session.execute(select(Check_log).where(Check_log.website_id==website_id)).all()
            logs = []

            for row in res:
                logs.append({
                    "id": row[0].id,
                    "website_id": row[0].id,
                    "status_code": row[0].status_code,
                    "response_time_ms": row[0].response_time_ms,
                    "is_up": row[0].is_up,
                    "checked_at": row[0].checked_at
                })

            return logs