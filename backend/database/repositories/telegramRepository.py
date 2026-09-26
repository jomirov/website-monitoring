from ..db import engine
from ...models.telegram import Telegram
from sqlalchemy import select, insert
from sqlalchemy.orm import Session

class TelegramRepository():
    def get_chat_id_by_user_id(self, user_id):
        with Session(engine) as session:
            res = session.execute(select(Telegram).where(Telegram.user_id==user_id)).first()
            return res[0].chat_id

    def insert_session(self, user_id, chat_id):
        with Session(engine) as session:
            s = Telegram(user_id=user_id, chat_id=chat_id)
            session.add(s)
            session.commit()