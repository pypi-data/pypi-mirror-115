import json

import urllib3

from iqs_client.api_client import ApiClient
from iqs_client.configuration import Configuration


class ApiClientWithOIDC(ApiClient):
    def __init__(self, configuration: Configuration, username: str, password: str, tokenPath="/token"):
        super(ApiClientWithOIDC, self).__init__(configuration)
        self.tokenPath = tokenPath
        self.username = username
        self.password = password
        self._get_or_refresh_token()

    def _get_or_refresh_token(self, forceNew=False):
        auth_url = self.configuration.host.replace("/api", "") + self.tokenPath
        if self.configuration.access_token == "":
            auth_req = {
                "username": self.username,
                "password": self.password,
                "forceNew": forceNew
            }
        else:
            auth_req = {
                "accessToken": self.configuration.access_token
            }
        http = urllib3.PoolManager()
        r = http.request('POST', auth_url, body=json.dumps(auth_req).encode('utf-8'))
        token = json.loads(r.data.decode('utf-8'))['token']
        self.configuration.access_token = token

    def call_api(self, resource_path, method,
                 path_params=None, query_params=None, header_params=None,
                 body=None, post_params=None, files=None,
                 response_type=None, auth_settings=None, async_req=None,
                 _return_http_data_only=None, collection_formats=None,
                 _preload_content=True, _request_timeout=None, _host=None):
        self._get_or_refresh_token()
        return super(ApiClientWithOIDC, self).call_api(resource_path, method,
                                                       path_params=path_params, query_params=query_params,
                                                       header_params=header_params,
                                                       body=body, post_params=post_params, files=files,
                                                       response_type=response_type, auth_settings=auth_settings,
                                                       async_req=async_req,
                                                       _return_http_data_only=_return_http_data_only,
                                                       collection_formats=collection_formats,
                                                       _preload_content=_preload_content,
                                                       _request_timeout=_request_timeout, _host=_host)
