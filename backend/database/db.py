from sqlalchemy import create_engine
from ..models import check_log, user, website, telegram
from ..models.base import Base

engine = create_engine("sqlite+pysqlite:///database/database.db", echo=True)

Base.metadata.create_all(engine)