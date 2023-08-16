####
# Modifications copyright 2023 burrizza
# Copyright 2014 Mateusz Harasymczuk, Gonchik Tsymzhitov (atlassian-api)
######
import logging
import urllib.parse
from json import dumps

import requests

logger = logging.getLogger(__name__)


class FedRepRestAPI(object):
    """
    FedRep API client constructor
    (mostly copied from atlassian-python-api see NOTICE)
    """
    default_headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }
    experimental_headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'X-ExperimentalApi': 'opt-in',
    }
    form_token_headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Atlassian-Token': 'no-check',
    }
    no_check_headers = {'X-Atlassian-Token': 'no-check'}
    safe_mode_headers = {
        'X-Atlassian-Token': 'nocheck',
        'Content-Type': 'application/vnd.atl.plugins.safe.mode.flag+json',
    }
    experimental_headers_general = {
        'X-Atlassian-Token': 'no-check',
        'X-ExperimentalApi': 'opt-in',
    }
    response = None

    def __init__(
            self,
            url,
            username=None,
            password=None,
            timeout=75,
            api_root='rest/api',
            api_version='latest',
            verify_ssl=True,
            session=None,
            oauth=None,
            oauth2=None,
            cookies=None,
            advanced_mode=None,
            kerberos=None,
            cloud=False,
            proxies=None,
            token=None,
    ):
        self.url = url
        self.username = username
        self.password = password
        self.timeout = int(timeout)
        self.verify_ssl = verify_ssl
        self.api_root = api_root
        self.api_version = api_version
        self.cookies = cookies
        self.advanced_mode = advanced_mode
        self.cloud = cloud
        self.proxies = proxies
        if session is None:
            self._session = requests.Session()
        else:
            self._session = session
        if username and password:
            self._create_basic_session(username, password)
        elif token is not None:
            self._create_token_session(token)
        elif oauth is not None:
            self._create_oauth_session(oauth)
        elif oauth2 is not None:
            self._create_oauth2_session(oauth2)
        elif kerberos is not None:
            self._create_kerberos_session(kerberos)
        elif cookies is not None:
            self._session.cookies.update(cookies)

    def close(self):
        return self._session.close()

    @property
    def session(self):
        """Providing access to the restricted field"""
        return self._session

    @staticmethod
    def url_joiner(url, path, trailing=None):
        url_link = '/'.join(str(s).strip('/') for s in [url, path] if s is not None)
        if trailing:
            url_link += '/'
        return url_link

    def resource_url(self, resource, api_root=None, api_version=None):
        if api_root is None:
            api_root = self.api_root
        if api_version is None:
            api_version = self.api_version
        return '/'.join(str(s).strip('/') for s in [api_root, api_version, resource] if s is not None)

    def log_curl_debug(self, method, url, data=None, headers=None, level=logging.DEBUG):
        """

        :param method:
        :param url:
        :param data:
        :param headers:
        :param level:
        :return:
        """
        headers = headers or self.default_headers
        message = "curl --silent -X {method} -H {headers} {data} '{url}'".format(
            method=method,
            headers=' -H '.join(['{0}: {1}'.format(key, value) for key, value in headers.items()]),
            data='' if not data else "--data '{0}'".format(dumps(data)),
            url=url,
        )
        logger.log(level=level, msg=message)

    def raise_for_status(self, response):
        """
        Checks the response for errors and throws an exception if return code >= 400
        Since different tools (Atlassian, Jira, ...) have different formats of returned json,
        this method is intended to be overwritten by a tool specific implementation.
        :param response:
        :return:
        """
        if 400 <= response.status_code < 600:
            try:
                j = response.json()
                if (j.get("errorMessages") is None):
                    error_msg = "\n".join([k + ": " + v for k, v in j.items()])
                else:
                    error_msg = "\n".join(
                        j.get("errorMessages", list())
                        + [
                            k.get("message", "") if isinstance(k, dict) else v
                            for k, v in j.get("errors", dict()).items()
                        ]
                    )
            except Exception as e:
                logger.error(e)
                response.raise_for_status()
            else:
                raise requests.HTTPError(error_msg, response=response)
        else:
            response.raise_for_status()

    def request(
            self,
            method='GET',
            path='/',
            data=None,
            json=None,
            flags=None,
            params=None,
            headers=None,
            files=None,
            trailing=None,
            absolute=False,
            advanced_mode=False,
    ):
        """

        :param method:
        :param path:
        :param data:
        :param json:
        :param flags:
        :param params:
        :param headers:
        :param files:
        :param trailing: bool
        :param absolute: bool, OPTIONAL: Do not prefix url, url is absolute
        :param advanced_mode: bool, OPTIONAL: Return the raw response
        :return:
        """
        url = self.url_joiner(None if absolute else self.url, path, trailing)
        params_already_in_url = True if '?' in url else False
        if params or flags:
            if params_already_in_url:
                url += '&'
            else:
                url += '?'
        if params:
            url += urllib.parse.urlencode(params or {})
        if flags:
            url += ('&' if params or params_already_in_url else '') + '&'.join(flags or [])
        json_dump = None
        if files is None:
            data = None if not data else dumps(data)
            json_dump = None if not json else dumps(json)
        # TODO: turned off curl output because of differing syntax between curl versions
        #self.log_curl_debug(
        #    method=method,
        #    url=url,
        #    headers=headers,
        #    data=data if data else json_dump,
        #)
        headers = headers or self.default_headers
        response = self._session.request(
            method=method,
            url=url,
            headers=headers,
            data=data,
            json=json,
            timeout=self.timeout,
            verify=self.verify_ssl,
            files=files,
            proxies=self.proxies,
        )
        response.encoding = 'utf-8'

        logger.debug(f'HTTP: {method} {path} -> {response.status_code} {response.reason}')
        logger.debug(f'HTTP: Response text -> {response.text}')
        if self.advanced_mode or advanced_mode:
            return response

        self.raise_for_status(response)
        return response

    def get(
            self,
            path,
            data=None,
            flags=None,
            params=None,
            headers=None,
            not_json_response=None,
            trailing=None,
            absolute=False,
            advanced_mode=False,
    ):
        """
        Get request based on the python-requests module. You can override headers, and also, get not json response
        :param path:
        :param data:
        :param flags:
        :param params:
        :param headers:
        :param not_json_response: OPTIONAL: For get content from raw request's packet
        :param trailing: OPTIONAL: for wrap slash symbol in the end of string
        :param absolute: bool, OPTIONAL: Do not prefix url, url is absolute
        :param advanced_mode: bool, OPTIONAL: Return the raw response
        :return:
        """
        response = self.request(
            'GET',
            path=path,
            flags=flags,
            params=params,
            data=data,
            headers=headers,
            trailing=trailing,
            absolute=absolute,
            advanced_mode=advanced_mode,
        )

        if self.advanced_mode or advanced_mode:
            return response
        if not_json_response:
            return response.content
        else:
            if not response.text:
                return None
            try:
                return response.json()
            except Exception as e:
                logger.error(e)
                return response.text
