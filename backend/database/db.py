from sqlalchemy import create_engine
from .models import user, website, check_log
from .models.user import User
from .models.base import Base

engine = create_engine("sqlite+pysqlite:///database/database.db", echo=True)

Base.metadata.create_all(engine)