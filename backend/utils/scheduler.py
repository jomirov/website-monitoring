from pytz import utc

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ProcessPoolExecutor

from ..dependencies import check_websites

jobstores = {
    'default': SQLAlchemyJobStore('sqlite:///utils/jobs.sqlite')
}
executors = {
    'default': ProcessPoolExecutor(3)
}
job_defaults = {
    'coalesce': False,
    'max_instances': 3
}

scheduler = AsyncIOScheduler(jobstores=jobstores, job_defaults=job_defaults, timezone=utc) #executors default = asyncioexecutor

scheduler.add_job(check_websites, 'interval', seconds=10, id='websites_checker', replace_existing=True)