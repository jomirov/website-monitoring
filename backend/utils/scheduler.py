from pytz import utc

from apscheduler.schedulers.background import BackgroundScheduler
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

scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults, timezone=utc)

# scheduler.remove_job('websites_checker')
# scheduler.add_job(check_websites, 'interval', seconds=10, id='websites_checker')