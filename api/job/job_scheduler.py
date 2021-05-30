from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor


class JobScheduler(object):

    def __init__(self):
        self.schedule = BackgroundScheduler(executors={
            'default': ThreadPoolExecutor(16),
            'processpool': ProcessPoolExecutor(4)
        })

    def add_job(self, job, interval):
        self.schedule.add_job(job, 'interval', seconds=interval)

    def start(self):
        self.schedule.start()
