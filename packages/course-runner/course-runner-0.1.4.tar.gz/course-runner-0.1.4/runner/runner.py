import hashlib
import sched
import time
import subprocess

from loguru import logger

from runner.config import Config
from runner.camisole import CamisoleAPiClient
from runner.course import RUNNING_STATUS, COMPILATION_ERROR_STATUS, CourseApiClient


class Runner:
    def __init__(self, submission, course_api_client: CourseApiClient,
                 camisole_api_client: CamisoleAPiClient):
        self._submission = submission
        self._course_api_client = course_api_client
        self._camisole = camisole_api_client

    def _download_submission_file(self):
        file_name = self._submission.get('file').split('/')[-1]
        logger.debug(file_name)
        content = self._course_api_client.download_file(file_name, "submit")
        logger.debug(content)
        return content

    def _verify_submission_file(self, content):
        s = hashlib.sha256(content).hexdigest()
        correct_sum = self._submission.get('file_sha')
        if s != correct_sum:
            logger.warning(f"{s}!={correct_sum}")
            return False
        return True

    def _run_jobs(self, j, language, source_content):
        logger.info(f"Start job {j.get('id')} with test_case_id {j.get('test_case')} ")
        update_ok = self._course_api_client.update_job(pk=j.get('id'), data={"status": 'RUNNING'})

        if not update_ok:
            logger.warning(f"Updating job {j.get('id')} via API not working. We stop the "
                           f"execution of the job ")
            return False

        test_case = self._course_api_client.get_test_case(j.get('test_case'))

        test_case_content_input = self._course_api_client.download_file(
            test_case.get('input').split('/')[-1], "test").decode("utf-8")
        test_case_content_output = self._course_api_client.download_file(
            test_case.get('output').split('/')[-1], "test").decode("utf-8")

        logger.info(test_case_content_input)
        logger.info(test_case_content_output)

        response = self._camisole.submit_job(language.get("name"), test_case,
                                             test_case_content_input,
                                             source_content)

        self._check_response(j, response)

        logger.debug(response)
        logger.info(f"end job {j.get('id')}")

    def run(self):
        update_ok = self._course_api_client.update_submission(self._submission.get('id'),
                                                              {"status": RUNNING_STATUS})
        logger.debug(update_ok)
        content = self._download_submission_file()
        if not self._verify_submission_file(content):
            logger.warning("We stop the execution because the hash sums do not match.")
            return

        jobs = self._course_api_client.get_list_of_jobs(submission_id=self._submission.get("id"))
        language = self._course_api_client.get_language_information(
            language_id=self._submission.get("language"))
        if len(jobs) == 0:
            logger.warning("pending submissio  with 0 jobs")
            return
        if language is None:
            logger.warning("Language not found")
            return
        logger.info(jobs)
        for j in jobs[:1]:
            self._run_jobs(j, language, content.decode("utf-8"))

    def _check_response(self, j, response):
        pass

    def _check_compilation(self, j, response: dict):
        if 'compile' not in response:
            return True
        compile_object = response.get('compile')
        if compile_object.get('exitcode') != 0 or compile_object.get('meta').get('exitcode') != 0 or \
                compile_object.get('meta').get('status') != 'OK':
            self._course_api_client.update_job(j.get('id'),
                                               data={"status": COMPILATION_ERROR_STATUS})
            return False



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
