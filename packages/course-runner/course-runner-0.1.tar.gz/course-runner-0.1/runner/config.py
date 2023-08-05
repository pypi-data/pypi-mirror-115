import os

from loguru import logger


def handler(signum, frame):
    with open('.config', 'r') as f:
        pid = int(f.read())
        os.kill(pid, 9)


class Config:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            logger.info('Creating the object')
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance.__init__()
            # Put any initialization here.
        logger.info(cls._instance)
        return cls._instance

    def __init__(self):
        self.camisole_url = 'http://127.0.0.1:4242'

        self.course_url = os.getenv("COURSE_URL", None)
        if self.course_url is None:
            raise ValueError("COURSE_URL environment variable can't be none !")
        self.course_api_key = os.getenv("COURSE_API_KEY", None)
        if self.course_api_key is None:
            raise ValueError("COURSE_API_KEY environment variable can't be none !")
        self.time_waiting = int(os.getenv("TIME_WAITING", 60))

    def init(self, camisole_url, course_url, course_api_key):
        self.camisole_url = camisole_url
        self.course_api_key = course_api_key
        self.course_url = course_url

    def __str__(self):
        return f'{self.course_url} {self.camisole_url}'
