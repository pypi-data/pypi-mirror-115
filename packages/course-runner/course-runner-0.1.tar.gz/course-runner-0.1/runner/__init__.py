import sched
import time

from loguru import logger

from runner.camisole import CamisoleAPiClient
from runner.config import Config
from runner.course import CourseApiClient
from runner.runner import Runner
import subprocess

__all__ = [
    '__title__',
    '__summary__',
    '__uri__',
    '__version__',
    '__author__',
    '__email__',
    '__license__',
    '__copyright__',
]

__title__ = 'course-runner'
__summary__ = 'autOevaluate yoUr Student Easily'
__keywords__ = 'autoevaluate'
__uri__ = 'https://gitlab.com/course-autoevaluate/runner'
__version__ = '0.1'
__author__ = 'Thibault Falque'
__email__ = 'thibault.falque@univ-artois.fr'

__license__ = 'LGPLv3+'
__copyright__ = '2019-2020'



s = sched.scheduler(time.time, time.sleep)


def init_configuration(c):
    api_client = CourseApiClient(c)
    api_client.register()
    logger.info('Register runner OK')
    with open('.config', 'w') as f:
        f.close()


def run_camisole_server():
    logger.info("Run Camisole server")
    cmd = ['camisole',   'serve', '-h', '127.0.0.1', '-p', '4242']
    p = subprocess.Popen(cmd)
    with open('.config', 'w') as f:
        f.write(str(p.pid))

    logger.info(f"The pid of camisole server is {p.pid}")


def run(sc):
    logger.info("Run thread")
    c = Config()
    logger.info(f"API COURSE URL: {c.course_url}")
    api_client = CourseApiClient(c)
    camisole_api_client = CamisoleAPiClient(c)
    try:
        next_submission = api_client.get_first_pending_submission()
    except ValueError as e:
        s.enter(c.time_waiting, 1, run, (sc,))
        return
    if len(next_submission) == 0:
        s.enter(c.time_waiting, 1, run, (sc,))
        return
    logger.info(next_submission)
    logger.info(f"Start execution of submission {next_submission['id']}")
    runner = Runner(next_submission, api_client, camisole_api_client)
    runner.run()
    logger.info(f"End execution of submission {next_submission['id']}")
    s.enter(c.time_waiting, 1, run, (sc,))
