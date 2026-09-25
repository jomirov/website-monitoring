from datetime import datetime
from dotenv import load_dotenv, unset_key
from sqlalchemy.orm import Session
from sqlalchemy import select, delete
from pwdlib import PasswordHash
from ..db import engine
from ...models.user import User

load_dotenv()

class UserRepository:
    def add_user(self, email, password):
        with Session(engine) as session:
            hashed_password = PasswordHash.recommended().hash(str(password))
            u = User(email=str(email), hashed_password=hashed_password, created_at=datetime.now())
            session.add(u)
            session.commit()

    def get_all_users(self):
        with Session(engine) as session:
            res = session.execute(select(User)).all()

            users = []

            for row in res:
                users.append({
                    "id": row[0].id,
                    "email": row[0].email,
                    "hashed_password": row[0].hashed_password,
                    "created_at": datetime.strftime(row[0].created_at, "%Y-%m-%d")
                })

            return users

    def get_user_by_id(self, id):
        with Session(engine) as session:
            res = session.execute(select(User).where(User.id==id)).first()

            if res == None:
                return None
            
            return {
                "id": res[0].id,
                "email": res[0].email,
                "hashed_password": res[0].hashed_password,
                "created_at": datetime.strftime(res[0].created_at, "%Y-%m-%d")
            }

    def get_user_by_email(self, email):
        with Session(engine) as session:
            res = session.execute(select(User).where(User.email==email)).first()

            if not res: return None

            return {
                "id": res[0].id,
                "email": res[0].email,
                "hashed_password": res[0].hashed_password,
                "created_at": datetime.strftime(res[0].created_at, "%Y-%m-%d")
            }

    def delete_user_by_id(self, id):
        with Session(engine) as session:
            doesExist = session.execute(select(User).where(User.id==id)).first()
            if doesExist == None:
                return None
            session.execute(delete(User).where(User.id==id))
            session.commit()
            unset_key(".env", key_to_unset=str(id))

            return 1