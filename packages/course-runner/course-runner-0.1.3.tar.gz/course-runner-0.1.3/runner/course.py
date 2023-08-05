import json
import socket

import requests
from loguru import logger
from http import HTTPStatus
from runner.api import APIClient
from runner.config import Config

PENDING_STATUS = "PENDING"
RUNNING_STATUS = "RUNNING"
COMPILATION_ERROR_STATUS = "COMPILATION_ERROR"


class CourseApiClient(APIClient):
    def __init__(self, config: Config):
        super().__init__(config)

    def get_first_pending_submission(self):
        route = '/api/submission/'
        url = self._construct_url(self._config.course_url, route=route,
                                  parameters={'status': PENDING_STATUS})
        r = requests.get(url, headers=self.get_headers())
        if r.status_code != HTTPStatus.OK:
            logger.error(r.status_code)
            logger.error(r.json())
            raise ValueError("Request for get pending submission failed")
        submissions = r.json()
        logger.info(f"Find {len(submissions)} submissions")
        return submissions[0] if len(submissions) > 0 else []

    def get_list_of_jobs(self, submission_id):
        logger.info(f'submission_id = {submission_id}')
        route = '/api/job/'
        url = self._construct_url(self._config.course_url, route=route,
                                  parameters={'submission': submission_id,
                                              'status': PENDING_STATUS})
        r = requests.get(url, headers=self.get_headers())
        if r.status_code != HTTPStatus.OK:
            logger.error(url)
            logger.error(r.status_code)
            logger.error(r.json())
            raise ValueError("Request for get job submission failed")
        return r.json()

    def get_language_information(self, language_id):
        logger.info(f'language_id = {language_id}')
        route = f'/api/language/{language_id}'
        url = self._construct_url(self._config.course_url, route=route)
        r = requests.get(url, headers=self.get_headers())
        if r.status_code != HTTPStatus.OK:
            logger.error(url)
            logger.error(r.status_code)
            logger.error(r.json())
            return None
        return r.json()

    def get_test_case(self, test_case_id):
        logger.info(f'test_case_id = {test_case_id}')
        route = f'/api/testcase/{test_case_id}'
        url = self._construct_url(self._config.course_url, route=route)
        r = requests.get(url, headers=self.get_headers())
        if r.status_code != HTTPStatus.OK:
            logger.error(url)
            logger.error(r.status_code)
            logger.error(r.json())
            return None
        return r.json()

    def update_submission(self, pk, data):
        route = f'/api/submission/{pk}/'
        url = self._construct_url(self._config.course_url, route=route)
        r = requests.patch(url, json=data, headers=self.get_headers())
        if r.status_code != HTTPStatus.OK:
            logger.error(r.status_code)
            logger.error(r.content)
            return False
        return True

    def update_job(self, pk, data):
        route = f'/api/job/{pk}/'
        url = self._construct_url(self._config.course_url, route=route)
        r = requests.patch(url, json=data, headers=self.get_headers())
        if r.status_code != HTTPStatus.OK:
            logger.error(r.status_code)
            logger.error(r.content)
            return False
        return True

    def download_file(self, file_name, t):
        route = f'/api/file/{file_name}/{t}'
        url = self._construct_url(self._config.course_url, route=route)
        r = requests.get(url, headers=self.get_headers())
        if r.status_code != HTTPStatus.OK:
            logger.info(url)
            logger.error(r.status_code)
            logger.error(r.content)
        return r.content

    def register(self):
        route = '/api/runner/'
        url = self._construct_url(self._config.course_url, route=route)
        logger.info(url)
        r = requests.post(url, json={"name": socket.gethostname()}, headers=self.get_headers())
        if r.status_code != HTTPStatus.CREATED:
            logger.error(r.status_code)
            logger.error(r.content)
            raise ValueError(r.content)
        return True
