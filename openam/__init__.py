"""python-openam is an python wrapper for the OpenAM Rest API."""
import requests
import json

__author__ = 'Werner Dijkerman'
__version__ = '0.0.1'
__license__ = "Apache License 2.0"
__email__ = "ikben@werner-dijkerman.nl"


class Openam(object):
    """OpenAM Rest Interface."""

    def __init__(self, openam_url='', resource=1.0, protocol=1.0, timeout=10, cookiename="iplanetDirectoryPro"):
        """Will initialize the openam module.

        :param openam_url: The complete URL to the OpenAM server.
        :type openam_url: str
        :param resource: The username to login.
        :type resource: str
        :param protocol: The password for the user configured in username.
        :type protocol: str
        :param timeout: HTTP requests timeout in seconds.
        :type timeout: int
        :param cookiename: The name of the cookie.
        :type cookiename: String
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
        """Will do an 'GET' request to get information.

        :param uri: The uri you want to get.
        :type uri: str
        :param headers: The http headers that are needed for the request.
        :type headers: dict
        :return: A dict with information that is retrieved from OpenAM
        """
        if self.openam_url[-1:] == '/':
            openam_path = self.openam_url + uri
        else:
            openam_path = self.openam_url + "/" + uri

        return requests.get(openam_path, headers=headers, timeout=self.timeout)

    def _post(self, uri, data=None, headers=None):
        """Post information to the API.

        :param uri: The uri that is used for posting the data.
        :type uri: str
        :param data: The data that is posted to the API.
        :type data: dict
        :param headers: The http headers that are needed for the request.
        :type headers: dict
        :rtype: dict
        :return: A dict with information that is retrieved from OpenAM
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
        """Will authenticate the configured user on OpenAM. When successful, a http header is added to the current headers with the the value of the 'cookiename' (Default is set to 'iplanetDirectoryPro') name and has the value from the retrieved tokenId.

        :param realm: The name of the realm on which the user needs to auhtenticate on. (Optional, when realms are used.)
        :type realm: str
        :param username: The username which is used to authenticate against OpenAM.
        :type username: str
        :param password: The password for the user configured on 'username'
        :type password: str
        :rtype: dict
        :return: A dict with the keys 'succesUrl' and 'tokenId'.

        :Example:
            >>> import openam
            >>> am = openam.Openam(openam_url="http://openam.example.com:8080/openam/")
            >>> am.authenticate(username="amadmin", password="password_openam")
            >>> am.logout()
            {u'successUrl': u'/openam/console', u'tokenId': u'AQIC5wM2LY4SfcxpamATDDJ7bGltWGY0fjfPO12mGFymFk8.*AAJTSQACMDEAAlNLABMyODU1MTgzNzIyNDI1MDA3OTE1AAJTMQAA*'}
            >>> am.logout()
        """
        if not username:
            raise ValueError("You will need to provide a username to login.")

        if not password:
            raise ValueError("You will need to provide a password to login.")

        post_data = {}
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
        """Will logout the current user from OpenAM.

        :param realm: The name of the realm.
        :type realm: str
        :rtype: bool
        :return: True if logout was successful, False when won't.
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
        """Get all - or when provided with the property - server related information.

        :param property: The type of information needed. When none is provided, all available configuration is returned (*).
        :type property: str
        :rtype: dict
        :return: Server specific information from OpenAM.
        :Example:
            >>> import openam
            >>> am = openam.Openam(openam_url="http://openam.example.com:8080/openam/")
            >>> am.authenticate(username="amadmin", password="password_openam")
            >>> am.get_serverinfo(property="cookieDomains")
            {u'domains': [u'.example.com']}
            >>> am.logout()
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
        """Validate if the session is active.

        :param realm: The name of the realm.
        :type realm: str
        :param token: The token id.
        :type token: str
        :rtype: dict
        :return: Information if token is active or not.
        :Example:
            >>> import openam
            >>> am = openam.Openam(openam_url="http://openam.example.com:8080/openam/")
            >>> auth_data = am.authenticate(username="amadmin", password="password_openam")
            >>> am.token_validation(token=auth_data['tokenId'])
            {u'valid': True, u'realm': u'/', u'uid': u'amadmin'}
            >>> am.logout()
        """
        if realm is not None:
            uri = 'json/' + realm + '/sessions/' + token + '?_action=validate'
        else:
            uri = 'json/sessions/' + token + '?_action=validate'

        data = self._post(uri=uri, data={}, headers=self.headers)
        if data.status_code == 200:
            return data.json()
        else:
            return False

    def session_information(self, action=None, token=None):
        """Will give information about the provided session.

        :param action:
        :type action: str
        :param token: The token id.
        :type token: str
        :rtype: dict
        :return: Information
        :Example:
            >>> import openam
            >>> am = openam.Openam(openam_url="http://openam.example.com:8080/openam/")
            >>> auth_data = am.authenticate(username="amadmin", password="password_openam")
            >>> am.session_information(action="getMaxTime", token=auth_data['tokenId'])
            {u'maxtime': 7199}
            >>> am.logout()
        """
        if not action:
            raise ValueError("Please provide a correct action you want to take.")
        if not token:
            raise ValueError("Please provide a token.")

        uri = 'json/sessions/?_action=' + action + '&tokenId=' + token
        data = self._post(uri=uri, data={}, headers=self.headers)
        if data.status_code == 200:
            return data.json()
        else:
            return False
