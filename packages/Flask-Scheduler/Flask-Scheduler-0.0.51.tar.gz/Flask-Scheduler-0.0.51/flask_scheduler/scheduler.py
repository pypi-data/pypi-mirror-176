import atexit
from typing import Callable

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask


class Scheduler(object):

    def __init__(self, app: Flask = None) -> None:  # type: ignore
        self.scheduler = BackgroundScheduler(daemon=True)
        self.jobs = []
        self._runner = None
        self._interval = 30
        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask = None) -> None:  # type: ignore
        """
        Initialize the application for use with this

        :param app:
            The Flask application object
        """
        if not hasattr(app, 'extensions'):
            app.extensions = {}
        app.extensions['scheduler'] = self
        self._default_configuration(app)
        self.current_app = app

        self.scheduler.start()
        atexit.register(lambda: self.scheduler.shutdown())
        self._interval = app.config['SCHEDULER_API_INTERVAL']
        self.scheduler.add_job(self._run, 'interval', seconds=self._interval)

    @staticmethod
    def _default_configuration(app: Flask) -> None:
        """
        Set default configuration values for the application.

        :param app:
            The Flask application object
        :return: None
        """
        app.config.setdefault('SCHEDULER_API_INTERVAL', 30)

    def _run(self):
        for job in self.jobs:
            job()

    def runner(self, interval: int = None):  # type: ignore
        """
        Decorator to register a function as a job.

        :param interval: default interval for the job is 30 seconds
        :return:
        """

        def decorator(f):
            if interval is not None:
                self.scheduler.add_job(f, 'interval', seconds=interval)
            else:
                if not hasattr(self, 'jobs'):
                    self.jobs = []
                self.jobs.append(f)
            return f

        return decorator

    def register_job(self,
                     job: Callable,
                     interval: int = None):  # type: ignore
        if interval is not None:
            self.scheduler.add_job(job, 'interval', seconds=interval)
        else:
            if not hasattr(self, 'jobs'):
                self.jobs = []
            self.jobs.append(job)

    def register_jobs(self,
                      jobs: list[Callable],
                      interval: int = None) -> None:  # type: ignore
        if interval is not None:
            for job in jobs:
                self.scheduler.add_job(job, 'interval', seconds=interval)
        else:
            if not hasattr(self, 'jobs'):
                self.jobs = []
            self.jobs.extend(jobs)
