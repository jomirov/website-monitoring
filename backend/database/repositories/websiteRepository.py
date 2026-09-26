import time
from ..db import engine
from sqlalchemy import select, delete, update
from sqlalchemy.orm import Session
from ...models.website import Website

class WebsiteRepository:
    def insert_website(self, user_id, name, url):
        with Session(engine) as session:
            w = Website(user_id=user_id, name=name, url=str(url), check_interval=60, is_active=True)
            session.add(w)
            session.commit()

    def get_websites_by_user_id(self, user_id):
        with Session(engine) as session:
            res = session.execute(select(Website).where(Website.user_id == user_id)).all()
            websites = []

            for row in res:
                websites.append({
                    "id": row[0].id,
                    "user_id": row[0].user_id,
                    "name": row[0].name,
                    "url": row[0].url,
                    "check_interval": row[0].check_interval,
                    "is_active": row[0].is_active
                })

            return websites

    def get_website_by_id(self, id):
        with Session(engine) as session:
            res = session.execute(select(Website).where(Website.id==id)).first()

            if not res:
                raise ValueError
            
            return {
                "id": res[0].id,
                "user_id": res[0].user_id,
                "name": res[0].name,
                "url": res[0].url,
                "check_interval": res[0].check_interval,
                "is_active": res[0].is_active
            }

    def get_websites_need_to_check(self):
        with Session(engine) as session: 
            res = session.execute(select(Website.id, Website.user_id, Website.url, Website.check_interval)).all()

            websites = []
            
            for row in res:
                websites.append({
                    "id": row.id,
                    "user_id": row.user_id,
                    "url": row.url,
                    "check_interval": row.check_interval
                })

            return websites

    def update_website_is_active(self, id, new_state):
        with Session(engine) as session:
            session.execute(update(Website).where(Website.id==id).values(is_active=new_state))
            session.commit()

    def update_website_check_interval(self, id, new_value):
        with Session(engine) as session:
            session.execute(update(Website).where(Website.id==id).values(check_interval=new_value))
            session.commit()

    def delete_website_by_id(self, id):
        with Session(engine) as session:
            res = session.execute(select(Website).where(Website.id==id)).first()

            if res[0] == None:
                return None
            
            session.execute(delete(Website).where(Website.id==id))
            session.commit()