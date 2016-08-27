"""python-openam is an python wrapper for the OpenAM Rest API."""
import requests
import json

__author__ = 'Werner Dijkerman'
__version__ = '0.0.2'
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
        """Will do an 'GET' request to get information via the API.

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
        """Post information via the API.

        :param uri: The uri that is used for posting the data.
        :type uri: str
        :param data: The data that is posted to the API.
        :type data: str
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
            data = {'error': e}
        return data

    def _put(self, uri, data=None, headers=None):
        """Put information via the API.

        :param uri: The uri that is used for putting the data.
        :type uri: str
        :param data: The data that is put to the API.
        :type data: str
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
            data = requests.put(openam_path, headers=headers, data=data, timeout=self.timeout)
        except requests.exceptions.RequestException as e:
            data = {'error': e}
        return data

    def _delete(self, uri, headers=None):
        """Delete information via the API.

        :param uri: The uri that is used for deleting the data.
        :type uri: str
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
            data = requests.delete(openam_path, headers=headers, timeout=self.timeout)
        except requests.exceptions.RequestException as e:
            data = {'error': e}
        return data

    def _uri_realm_creator(self, realm=None, uri=None):
        """Creating the uri if there is a realm provided.

        :param realm: The name of the realm
        :type realm: str
        :param uri: The uri after the 'realm' part.
        :type uri: str
        :rtype: str
        :return:
        """
        if realm is not None:
            uri = 'json/' + realm + '/' + uri
        else:
            uri = 'json/' + uri

        return uri

    def _type_validator(self, type=None):
        """Validating if a type is set to one of the 3 possibilities. If not, 'users' will be used as type.

        :param type: The name of the type
        :type type: str
        :rtype: str
        :return: The type
        """
        if type not in ['agents', 'users', 'groups']:
            type = 'users'
        return type

    def authenticate(self, realm=None, username=None, password=None):
        """Will authenticate the configured user on OpenAM.

        When successful, a http header is added to the current headers with the the value of the 'cookiename'
        (Default is set to 'iplanetDirectoryPro') name and has the value from the retrieved tokenId.

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
            {u'successUrl': u'/openam/console', u'tokenId': u'AQIC5wM2LY4SfcxpamATDDJ7bGltWGY0fjfPO12mGFymFk8.*AAJTSQA.. '}
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
        uri = self._uri_realm_creator(realm=realm, uri="authenticate")

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
        uri = self._uri_realm_creator(realm=realm, uri="sessions/?_action=logout")
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
        token_url = 'sessions/' + token + '?_action=validate'
        uri = self._uri_realm_creator(realm=realm, uri=token_url)
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

    def create_identity(self, realm=None, type="users", user_data=None):
        """Create an identity. This can be one of the following types.

        * users
        * agents
        * groups

        It can be configured by using the correct value in **type**. When something else is used other than the 3
        mentioned types, **users** will be used.

        :param realm: The name of the realm.
        :type realm: str
        :param type: The type of identity you want to create.
        :type type: str
        :param user_data: All necessary information needed to create an identity.
        :type user_data: dict
        :rtype: json
        :return:
        :Example:
            >>> import openam
            >>> am = openam.Openam(openam_url="http://openam.example.com:8080/openam/")
            >>> auth_data = am.authenticate(username="amadmin", password="password_openam")
            >>> user_data = {"username": "bjensen", "userpassword": "secret12", "mail": "bjensen@example.com"}
            >>> am.create_identity(user=user_data)
            {u'username': u'bjensen', u'dn': [u'uid=bjensen,ou=people,dc=openam,dc=forgerock,dc=org'], u'realm': u'/'..}
            >>> am.create_identity(user=user_data)
            {u'reason': u'Conflict', u'code': 409, u'message': u'Resource already exists'}
            >>> am.logout()
        """
        if not user_data:
            raise ValueError("Please provide correct user information.")

        user_data = str(json.dumps(user_data))
        type = self._type_validator(type=type)
        uri = self._uri_realm_creator(realm=realm, uri=type + '/?_action=create')
        data = self._post(uri=uri, data=user_data, headers=self.headers)
        return data.json()

    def list_identities(self, realm=None, type="users", query=None):
        """List or search an identity. This can be one of the following types.

        * users
        * agents
        * groups

        :param realm: The name of the realm.
        :type realm: str
        :param type: The type of identity you want to search.
        :type type: str
        :param query: Search pattern for finding the correct username/agentname/groupname.
        :type query: str
        :rtype: json
        :return: Information of the found identity.
        :Example:
            >>> import openam
            >>> am = openam.Openam(openam_url="http://openam.example.com:8080/openam/")
            >>> auth_data = am.authenticate(username="amadmin", password="password_openam")
            >>> am.list_identities(query="demo")
            {u'totalPagedResultsPolicy': u'NONE', u'pagedResultsCookie': None, u'totalPagedResults': -1, u'result': [{u'username': u'demo', u'dn' ...
            >>> am.logout()
        """
        if query is None:
            query = '*'

        type = self._type_validator(type=type)
        uri = self._uri_realm_creator(realm=realm, uri=type + '/?_queryID=' + query)
        data = self._get(uri=uri, headers=self.headers)
        return data.json()

    def get_identity(self, realm=None, type="users", username=None, fields=None):
        """Get an identity. This can be one of the following types.

        * users
        * agents
        * groups

        :param realm: The name of the realm.
        :type realm: str
        :param type: The type of identity you want to search.
        :type type: str
        :param username: username/agentname/groupname to lookup.
        :type username: str
        :param fields: The fields you want to retrieve. When None is given, all information is returned.
        :type fields: str
        :rtype: json
        :return: False when no user is found, otherwise a dict with information about the user.
        :Example:
            >>> import openam
            >>> am = openam.Openam(openam_url="http://openam.example.com:8080/openam/")
            >>> auth_data = am.authenticate(username="amadmin", password="password_openam")
            >>> am.get_identity(username="demo")
            {u'username': u'demo', u'dn': [u'uid=demo,ou=people,dc=openam,dc=forgerock,dc=org'], u'realm': u'/',  ...
            >>> am.logout()
        """
        if not username:
            raise ValueError("Please provide a username.")

        type = self._type_validator(type=type)
        uri = self._uri_realm_creator(realm=realm, uri=type + '/' + username)
        if fields is not None:
            uri = uri + '?_fields=' + fields

        data = self._get(uri=uri, headers=self.headers)
        if data.status_code == 200:
            return data.json()
        else:
            return False

    def update_identity(self, realm=None, type="users", username=None, user_data=None):
        """Update an identity. This can be one of the following types.

        * users
        * agents
        * groups

        :param realm: The name of the realm.
        :type realm: str
        :param type: The type of identity you want to update.
        :type type: str
        :param username: The username/agentname/groupname that needs to be updated.
        :type username: str
        :param user_data: The information you want to update.
        :type user_data: dict
        :rtype: json
        :return: Json information.
        :Example:
            >>> import openam
            >>> am = openam.Openam(openam_url="http://openam.example.com:8080/openam/")
            >>> auth_data = am.authenticate(username="amadmin", password="password_openam")
            >>> user_data = { "mail": "demo@example.com" }
            >>> am.update_identity(username="demo", user_data=user_data)
            {u'username': u'demo', u'dn': [u'uid=demo,ou=people,dc=openam,dc=forgerock,dc=org'], u'realm': u'/',  ...
            >>> am.logout()
        """
        if not username:
            raise ValueError("Please provide a username.")

        if not user_data:
            raise ValueError("Please provide correct user information.")

        user_data = str(json.dumps(user_data))
        type = self._type_validator(type=type)
        uri = self._uri_realm_creator(realm=realm, uri=type + '/' + username)
        data = self._put(uri=uri, data=user_data, headers=self.headers)
        return data.json()

    def delete_identity(self, realm=None, type="users", username=None):
        """Delete an identity. This can be one of the following types.

        * users
        * agents
        * groups

        :param realm: The name of the realm.
        :type realm: str
        :param type: The type of identity you want to delete.
        :type type: str
        :param username: The username/agentname/groupname that needs to be deleted.
        :type username: str
        :rtype: json
        :return: Information if the deleting went successful.
        :Example:
            >>> import openam
            >>> am = openam.Openam(openam_url="http://openam.example.com:8080/openam/")
            >>> auth_data = am.authenticate(username="amadmin", password="password_openam")
            >>> am.delete_identity(username="bjensen")
            {u'success': u'true'}
            >>> am.logout()
        """
        if not username:
            raise ValueError("Please provide a username.")

        type = self._type_validator(type=type)
        uri = self._uri_realm_creator(realm=realm, uri=type + '/' + username)
        data = self._delete(uri=uri, headers=self.headers)
        return data.json()

    def change_password(self, username=None, user_data=None):
        """Change the password for the given user.

        :param username: The username of the identity.
        :type username: str
        :param user_data: The old and new password.
        :type user_data: dict
        :rtype: bool
        :return:
        :Example:
            >>> import openam
            >>> am = openam.Openam(openam_url="http://openam.example.com:8080/openam/")
            >>> auth_data = am.authenticate(username="amadmin", password="password_openam")
            >>> user_data = {"currentpassword": "secret12", "userpassword": "secret13"}
            >>> am.change_password(username="bjensen", user_data=user_data)
            True
            >>> am.logout()
        """
        if not username:
            raise ValueError("Please provide a username.")

        if not user_data:
            raise ValueError("Please provide correct user information.")

        user_data = str(json.dumps(user_data))
        uri = 'json/users/' + username + '?_action=changePassword'
        data = self._post(uri=uri, data=user_data, headers=self.headers)
        if data.status_code == 200:
            return True
        else:
            return False

    def create_realm(self, realm_data=None):
        """Creating a realm.

        :param realm_data: Realm data that is needed for creating the realm.
        :type realm_data: dict
        :rtype: dict
        :return: Name of the realm.
        :Example:
            >>> import openam
            >>> am = openam.Openam(openam_url="http://openam.example.com:8080/openam/")
            >>> auth_data = am.authenticate(username="amadmin", password="password_openam")
            >>> realm_data = {"realm": "myRealm"}
            >>> am.create_realm(realm_data=realm_data)
            {u'realmCreated': u'/myRealm'}
            >>> am.logout()
        """
        if not realm_data:
            raise ValueError("Please provide correct realm_data information.")

        realm_data = str(json.dumps(realm_data))
        uri = 'json/realms/?_action=create'
        data = self._post(uri=uri, data=realm_data, headers=self.headers)
        return data.json()

    def get_realm(self, realm=None):
        """Get information of the given realm.

        :param realm: The name of the realm.
        :type realm: str
        :rtype: dict
        :return: All information about the realm.
        :Example:
            >>> import openam
            >>> am = openam.Openam(openam_url="http://openam.example.com:8080/openam/")
            >>> auth_data = am.authenticate(username="amadmin", password="password_openam")
            >>> am.get_realm(realm="myRealm")
            {u'serviceNames': [u'sunAMDelegationService', u'iPlanetAMAuthService', u'iPlanetAMPolicyConfigService', .. }
            >>> am.logout()
        """
        if not realm:
            raise ValueError("Please provide correct realm name.")

        uri = 'json/realms/' + realm
        data = self._get(uri=uri, headers=self.headers)
        if data.status_code == 200:
            return data.json()
        else:
            return False

    def list_realms(self, realm=None):
        """Get information on all (sub) realms that are configured.

        :param realm: The name of the realm.
        :type realm: str
        :rtype: dict
        :return: Information with all realms.
        :Example:
            >>> import openam
            >>> am = openam.Openam(openam_url="http://openam.example.com:8080/openam/")
            >>> auth_data = am.authenticate(username="amadmin", password="password_openam")
            >>> am.list_realms()
            {u'totalPagedResultsPolicy': u'NONE', u'pagedResultsCookie': None, u'totalPagedResults': -1, u'result': [u'/', u'/myRealm']
            >>> am.logout()
        """
        uri = self._uri_realm_creator(realm=realm, uri='realms?_queryFilter=true')
        data = self._get(uri=uri, headers=self.headers)
        if data.status_code == 200:
            return data.json()
        else:
            return False

    def update_realm(self, realm=None, realm_data=None):
        """Updating a realm.

        :param realm: The name of the realm.
        :type realm: str
        :param realm_data: Realm data that is needed for updating the realm.
        :rtype: dict
        :return: Information if the update is successful.
        :Example:
            >>> import openam
            >>> am = openam.Openam(openam_url="http://openam.example.com:8080/openam/")
            >>> auth_data = am.authenticate(username="amadmin", password="password_openam")
            >>> realm_data = {"sunOrganizationStatus": "Inactive"}
            >>> am.update_realm(realm="myRealm", realm_data=realm_data)
            {u'realmUpdated': u'/myRealm'}
            >>> am.logout()
        """
        if not realm:
            raise ValueError("Please provide a realm.")

        if not realm_data:
            raise ValueError("Please provide correct realm_data information.")

        uri = 'json/realms/' + realm
        realm_data = str(json.dumps(realm_data))
        data = self._put(uri=uri, data=realm_data, headers=self.headers)
        return data.json()

    def delete_realm(self, realm=None):
        """Deleting a realm.

        :param realm: The name of the realm.
        :type realm: str
        :rtype: dict
        :return: Information if delete is successful.
        :Example:
            >>> import openam
            >>> am = openam.Openam(openam_url="http://openam.example.com:8080/openam/")
            >>> auth_data = am.authenticate(username="amadmin", password="password_openam")
            >>> am.delete_realm(realm="myRealm")
            {u'success': u'true'}
            >>> am.logout()
        """
        if not realm:
            raise ValueError("Please provide a realm.")

        uri = 'json/realms/' + realm
        data = self._delete(uri=uri, headers=self.headers)
        return data.json()
