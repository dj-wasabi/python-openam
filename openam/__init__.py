"""python-openam is an python wrapper for the OpenAM Rest API."""


__author__ = 'Werner Dijkerman'
__version__ = '0.0.1'
__license__ = "Apache License 2.0"
__email__ = "ikben@werner-dijkerman.nl"

import requests
import json


class Openam(object):

    """OpenAM Rest Interface."""

    def __init__(self, openam_url='', resource=1.0, protocol=1.0, timeout=10, cookiename="iplanetDirectoryPro"):
        """
        Will initialize the openam module.
        :param openam_url: The complete URL to the OpenAM server.
        :param resource: The username to login.
        :param protocol: The password for the user configured in username.
        :param timeout: HTTP requests timeout in seconds.
        :param cookiename: HTTP requests timeout in seconds.
        """
        if not openam_url:
            raise ValueError('This interface needs an OpenAM URL to work!')

        self.openam_url = openam_url
        self.resource = resource
        self.protocol = protocol
        self.cookiename = cookiename
        self.headers = {}
        self.headers['Content-Type'] = 'application/json'
        self.headers[cookiename] = None
        self.timeout = int(timeout)

    def _get(self, uri, headers=None):
        """

        :param uri:
        :param headers:
        :return:
        """
        if self.openam_url[-1:] == '/':
            openam_path = self.openam_url + uri
        else:
            openam_path = self.openam_url + "/" + uri

        return requests.get(openam_path, headers=headers, timeout=self.timeout)

    def _post(self, uri, data=None, headers=None):
        """

        :param uri:
        :param data:
        :param headers:
        :return:
        """

        if self.openam_url[-1:] == '/':
            openam_path = self.openam_url + uri
        else:
            openam_path = self.openam_url + "/" + uri

        try:
            data = requests.post(openam_path, headers=headers, data=data, timeout=self.timeout)
        except requests.exceptions.RequestException as e:
            data = e

        return data

    def authenticate(self, realm=None, username=None, password=None):
        """

        :param realm:
        :param username:
        :param password:
        :return:
        """

        if not username:
            raise ValueError("You will need to provide a username to login.")

        if not password:
            raise ValueError("You will need to provide a password to login.")

        post_data = '{}'
        headers = self.headers
        cookiename = self.cookiename
        headers['X-OpenAM-Username'] = username
        headers['X-OpenAM-Password'] = password

        if realm is not None:
            uri = 'json/' + realm + '/authenticate'
        else:
            uri = 'json/authenticate'

        data = self._post(uri=uri, data=post_data, headers=headers)
        if data.status_code == 200:
            json_data = data.json()
            self.headers[cookiename] = json_data['tokenId']
            return json_data
        else:
            return False

    def logout(self, realm=None):
        """

        :param realm:
        :return:
        :Example:
        >>> import openam
        >>> am = openam.Openam(openam_url="http://openam.example.com:8080/openam/")
        >>> am.authenticate(username="amadmin", password="password_openam")
        >>> am.logout()
        True
        """
        if realm is not None:
            uri = 'json/' + realm + '/sessions/?_action=logout'
        else:
            uri = 'json/sessions/?_action=logout'

        data = self._post(uri=uri, headers=self.headers)
        if data.status_code == 200:
            return True
        else:
            return False

    def get_serverinfo(self, property=None):
        """

        :param property:
        :return:
        :Example:
        >>> import openam
        >>> am = openam.Openam(openam_url="http://openam.example.com:8080/openam/")
        >>> am.authenticate(username="amadmin", password="password_openam")
        >>> am.get_serverinfo(property="cookieDomains")
        {u'domains': [u'.example.com']}
        """
        if property is None:
            property = '*'

        uri = 'json/serverinfo/' + property
        data = self._get(uri=uri, headers=self.headers)
        if data.status_code == 200:
            return data.json()
        else:
            return False

    def token_validation(self, realm=None, token=None):
        """

        :param realm:
        :param token:
        :return:
        :Example:
        >>> import openam
        >>> am = openam.Openam(openam_url="http://openam.example.com:8080/openam/")
        >>> auth_data = am.authenticate(username="amadmin", password="password_openam")
        >>> am.token_validation(token=auth_data['tokenId'])
        {u'valid': True, u'realm': u'/', u'uid': u'amadmin'}
        """

        if realm is not None:
            uri = 'json/' + realm + '/sessions/' + token + '?_action=validate'
        else:
            uri = 'json/sessions/' + token + '?_action=validate'

        data = self._post(uri=uri, data='{}', headers=self.headers)
        if data.status_code == 200:
            return data.json()
        else:
            return False

    def session_information(self, action=None, token=None):
        """

        :param action:
        :param token:
        :return:
        """

        if not action:
            raise ValueError("Please provide a correct action you want to take.")
        if not token:
            raise ValueError("Please provide a token.")

        uri = 'json/sessions/?_action=' + action + '&tokenId=' + token
        data = self._post(uri=uri, data='{}', headers=self.headers)
        if data.status_code == 200:
            return data.json()
        else:
            return False
