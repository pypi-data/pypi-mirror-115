class APIClient:
    def __init__(self, config):
        self._config = config

    def get_headers(self):
        return {'Authorization': f'Api-Key {self._config.course_api_key}'}

    def _construct_url(self, api_url, route=None, parameters=None):
        if parameters is None:
            parameters = {}
        params = []
        for k, v in parameters.items():
            params.append(f'{k}={v}')
        if len(params) > 0:
            param_string = "&".join(params)
            return f'{api_url}{route}?{param_string}'
        return f'{api_url}{route}'
