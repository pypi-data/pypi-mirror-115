from http import HTTPStatus

import requests

from runner.api import APIClient
from loguru import logger


class CamisoleAPiClient(APIClient):
    def __init__(self, config):
        super().__init__(config)

    def get_headers(self):
        return None

    def submit_job(self, lang, test_case, test_case_content, source):
        if test_case_content is None or source is None:
            logger.error("test_case content or source content can't be None !")
            return

        data = {
            "lang": lang,
            "source": source,
            "tests": [{"name": test_case.get('input'), "stdin": test_case_content}]
        }

        url = self._construct_url(self._config.camisole_url, "/run")
        r = requests.post(url, json=data, headers=self.get_headers())
        if r.status_code != HTTPStatus.OK:
            logger.error(r.status_code)
            logger.error(r.json())
            return None
        j = r.json()
        return j
