"""Test script for python-openam"""

import sys
import os
import requests
import pytest

my_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, my_path + '/../')

import openam


@pytest.fixture
def openam_version(scope='function', params=None, autouse=False):
    url = 'http://openam.example.com:8080/version'
    version = requests.get(url, timeout=10)
    return int(version.text.rstrip())


def test___init__openam_url():
    """Test __init__ function if openam_url is provided.
    :return:
    """
    with pytest.raises(ValueError) as excinfo:
        openam.Openam()
    assert excinfo.value.message == 'This interface needs an OpenAM URL to work!'


def test__get():
    """Test the _get function with wrong_uri.
    :return:
    """
    am = openam.Openam(openam_url="http://openam.example.com:8080/openam")
    data = am._get(uri='wrong_uri')
    assert not data


def test__post():
    """Test the _post function with wrong_uri.
    :return:
    """
    am = openam.Openam(openam_url="http://openam.example.com:8080/openam")
    data = am._post(uri='wrong_uri', data='{}', headers={})
    assert not data


def test__post_wrong_port():
    """Test the _post function on wrong port.
    :return:
    """
    am = openam.Openam(openam_url="http://openam.example.com:880/opeam")
    data = am._post(uri='wrong_uri', data='{}', headers={})
    assert 'error' in data


def test__put():
    """Test the _put function with wrong_uri.
    :return:
    """
    am = openam.Openam(openam_url="http://openam.example.com:8080/openam")
    data = am._put(uri='wrong_uri', data='{}', headers={})
    assert not data


def test__put_wrong_port():
    """Test the _put function on wrong port.
    :return:
    """
    am = openam.Openam(openam_url="http://openam.example.com:880/opeam")
    data = am._put(uri='wrong_uri', data='{}', headers={})
    assert 'error' in data


def test__delete():
    """Test the _delete function with wrong_uri.
    :return:
    """
    am = openam.Openam(openam_url="http://openam.example.com:8080/openam")
    data = am._delete(uri='wrong_uri')
    assert not data


def test__delete_wrong_port():
    """Test the _delete function on wrong port.
    :return:
    """
    am = openam.Openam(openam_url="http://openam.example.com:880/opeam")
    data = am._delete(uri='wrong_uri')
    assert 'error' in data


def test__uri_realm_creator():
    """
    :return:
    """
    am = openam.Openam(openam_url="http://openam.example.com:8080/opeam")
    data = am._uri_realm_creator(uri='wrong_uri')
    assert data == 'json/wrong_uri'


def test__uri_realm_creator_test_realm():
    """
    :return:
    """
    am = openam.Openam(openam_url="http://openam.example.com:8080/opeam")
    data = am._uri_realm_creator(realm="test", uri='wrong_uri')
    assert data == 'json/test/wrong_uri'


def test__type_validator():
    """
    :return:
    """
    am = openam.Openam(openam_url="http://openam.example.com:8080/opeam")
    data = am._type_validator(type="groups")
    assert data == 'groups'


def test__type_validator_wrong_type():
    """
    :return:
    """
    am = openam.Openam(openam_url="http://openam.example.com:8080/opeam")
    data = am._type_validator(type="wrong")
    assert data == 'users'


def test__to_string_no_data():
    """Test the _to_string without any data.
    :return:
    """
    with pytest.raises(ValueError) as excinfo:
        am = openam.Openam(openam_url="http://openam.example.com:8080/openam/")
        data = am._to_string()
    assert excinfo.value.message == 'Please provide a correct data structure.'


def test__to_string_dict():
    """Test the _to_string with a dict.
    :return:
    """
    am = openam.Openam(openam_url="http://openam.example.com:8080/opeam")
    data = am._to_string(data={"sunOrganizationStatus": "Inactive"})
    assert data == '{"sunOrganizationStatus": "Inactive"}'


def test__to_string_list():
    """Test the _to_string with a list
    :return:
    """
    am = openam.Openam(openam_url="http://openam.example.com:8080/opeam")
    data = am._to_string(data=['my', 'list'])
    assert data == 'my list'


def test__to_string_string():
    """Test the _to_string with a string
    :return:
    """
    am = openam.Openam(openam_url="http://openam.example.com:8080/opeam")
    data = am._to_string(data='my list')
    assert data == 'my list'


def test_authenticate():
    """Test the authentication function.
    :return:
    """
    am = openam.Openam(openam_url="http://openam.example.com:8080/openam/")
    auth_data = am.authenticate(username="amadmin", password="password_openam")
    am.logout()
    assert auth_data['successUrl'] == '/openam/console'


def test_authenticate_wrong_realm():
    """Test the authentication function with a wrong realm.
    :return:
    """
    am = openam.Openam(openam_url="http://openam.example.com:8080/openam/")
    auth_data = am.authenticate(realm="wrong", username="amadmin", password="wrong_password")
    am.logout()
    assert not auth_data


def test_authenticate_wrong_password():
    """Test the authentication function with a wrong password.
    :return:
    """
    am = openam.Openam(openam_url="http://openam.example.com:8080/openam/")
    auth_data = am.authenticate(username="amadmin", password="wrong_password")
    am.logout()
    assert not auth_data


def test_authenticate_no_username():
    """ Will test authenticate function if no username is provided.
    :return:
    """
    with pytest.raises(ValueError) as excinfo:
        am = openam.Openam(openam_url="http://openam.example.com:8080/openam/")
        am.authenticate(password="password_openam")
    assert excinfo.value.message == 'You will need to provide a username to login.'


def test_authenticate_no_password():
    """ Will test authenticate function if no password is provided.
    :return:
    """
    with pytest.raises(ValueError) as excinfo:
        am = openam.Openam(openam_url="http://openam.example.com:8080/openam/")
        am.authenticate(username="amadmin")
    assert excinfo.value.message == 'You will need to provide a password to login.'


def test_logout():
    """Test if a user can logout.
    :return:
    """
    am = openam.Openam(openam_url="http://openam.example.com:8080/openam/")
    am.authenticate(username="amadmin", password="password_openam")
    assert am.logout()


def test_logout_realm_wrong():
    """Test if a user can logout with a wrong realm.
    :return:
    """
    am = openam.Openam(openam_url="http://openam.example.com:8080/openam/")
    am.authenticate(username="amadmin", password="password_openam")
    assert not am.logout(realm="wrong")


def test_get_serverinfo():
    """Test to get all server information.
    :return:
    """
    am = openam.Openam(openam_url="http://openam.example.com:8080/openam/")
    am.authenticate(username="amadmin", password="password_openam")
    data = am.get_serverinfo()
    am.logout()
    assert data['selfRegistration'] == 'false'


def test_get_serverinfo_with_property():
    """Test to get the cookieDomains configuration.
    :return:
    """
    am = openam.Openam(openam_url="http://openam.example.com:8080/openam/")
    am.authenticate(username="amadmin", password="password_openam")
    data = am.get_serverinfo(property="cookieDomains")
    am.logout()
    assert data['domains'] == ['.example.com']


def test_get_serverinfo_with_wrong_property():
    """Test with a wrong property to get server information.
    :return:
    """
    am = openam.Openam(openam_url="http://openam.example.com:8080/openam/")
    am.authenticate(username="amadmin", password="password_openam")
    data = am.get_serverinfo(property="wrong")
    am.logout()
    assert not data


def test_token_validation():
    """Test if a token is validated.
    :return:
    """
    am = openam.Openam(openam_url="http://openam.example.com:8080/openam/")
    auth_data = am.authenticate(username="amadmin", password="password_openam")
    data = am.token_validation(token=auth_data['tokenId'])
    am.logout()
    assert data


def test_token_validation_wrong():
    """Test a wrong token to validate.
    :return:
    """
    am = openam.Openam(openam_url="http://openam.example.com:8080/openam/")
    auth_data = am.authenticate(username="amadmin", password="password_openam")
    data = am.token_validation(token="wrong")
    am.logout()
    assert not data['valid']


def test_token_validation_wrong_realm():
    """Test a wrong token to validate.
    :return:
    """
    am = openam.Openam(openam_url="http://openam.example.com:8080/openam/")
    auth_data = am.authenticate(username="amadmin", password="password_openam")
    data = am.token_validation(token=auth_data['tokenId'], realm="wrong")
    am.logout()
    assert not data


def test_session_information():
    """Validate if a token is Active.
    :return:
    """
    am = openam.Openam(openam_url="http://openam.example.com:8080/openam/")
    auth_data = am.authenticate(username="amadmin", password="password_openam")
    data = am.session_information(action="isActive", token=auth_data['tokenId'])
    am.logout()
    assert data['active']


def test_session_information_wrong_action():
    """Get the session information with a wrong action.
    :return:
    """
    am = openam.Openam(openam_url="http://openam.example.com:8080/openam/")
    auth_data = am.authenticate(username="amadmin", password="password_openam")
    data = am.session_information(action="wrong", token=auth_data['tokenId'])
    am.logout()
    assert not data


def test_session_information_no_action():
    """ Will test session_information function if no action is provided.
    :return:
    """
    with pytest.raises(ValueError) as excinfo:
        am = openam.Openam(openam_url="http://openam.example.com:8080/openam/")
        auth_data = am.authenticate(username="amadmin", password="password_openam")
        am.session_information(token=auth_data['tokenId'])
    assert excinfo.value.message == 'Please provide a correct action you want to take.'


def test_session_information_no_token():
    """ Will test session_information function if no token is provided.
    :return:
    """
    with pytest.raises(ValueError) as excinfo:
        am = openam.Openam(openam_url="http://openam.example.com:8080/openam/")
        am.authenticate(username="amadmin", password="password_openam")
        am.session_information(action="getMaxTime")
    assert excinfo.value.message == 'Please provide a token.'


def test_create_identity_no_user_data():
    """ Will create an identity if no user_data is provided.
    :return:
    """
    with pytest.raises(ValueError) as excinfo:
        am = openam.Openam(openam_url="http://openam.example.com:8080/openam/")
        am.authenticate(username="amadmin", password="password_openam")
        am.create_identity()
    assert excinfo.value.message == 'Please provide correct user information.'


def test_create_identity():
    """ Will create an identity.
    :return:
    """
    am = openam.Openam(openam_url="http://openam.example.com:8080/openam/")
    am.authenticate(username="amadmin", password="password_openam")
    user_data = {"username": "bjensen", "userpassword": "secret12", "mail": "bjensen@example.com"}
    data = am.create_identity(user_data=user_data)
    am.logout()

    assert data['dn'] == ['uid=bjensen,ou=people,dc=openam,dc=forgerock,dc=org']


def test_create_identity_with_wrong_type():
    """ Will create an identity with the wrong type. Will be set to 'users'
    :return:
    """
    am = openam.Openam(openam_url="http://openam.example.com:8080/openam/")
    am.authenticate(username="amadmin", password="password_openam")
    user_data = {"username": "bjensen", "userpassword": "secret12", "mail": "bjensen@example.com"}
    data = am.create_identity(user_data=user_data, type="wrong")
    am.logout()

    assert data['message'] == 'Resource already exists'


def test_list_identities():
    """Will list all users to find username bjensen
    :return:
    """
    am = openam.Openam(openam_url="http://openam.example.com:8080/openam/")
    am.authenticate(username="amadmin", password="password_openam")
    my_data = am.list_identities()
    am.logout()

    # OpenAM 13
    if 'username' in my_data['result'][0]:
        username = my_data['result'][0]['username']
    else:
        # OpenAM 12
        username = my_data['result'][0]

    assert username == "bjensen"


def test_list_identities_user_demo():
    """Find user named demo.
    :return:
    """
    am = openam.Openam(openam_url="http://openam.example.com:8080/openam/")
    am.authenticate(username="amadmin", password="password_openam")
    my_data = am.list_identities(query="demo")
    am.logout()

    # OpenAM 13
    if 'username' in my_data['result'][0]:
        username = my_data['result'][0]['username']
    else:
        # OpenAM 12
        username = my_data['result'][0]

    assert username == "demo"


def test_list_identities_user_demo_wrong_type():
    """Find user named demo with wrong type.
    :return:
    """
    am = openam.Openam(openam_url="http://openam.example.com:8080/openam/")
    am.authenticate(username="amadmin", password="password_openam")
    my_data = am.list_identities(query="demo", type="wrong")
    am.logout()

    # OpenAM 13
    if 'username' in my_data['result'][0]:
        username = my_data['result'][0]['username']
    else:
        # OpenAM 12
        username = my_data['result'][0]

    assert username == "demo"


def test_get_identity_no_username():
    """ Will get an identity if no username is provided.
    :return:
    """
    with pytest.raises(ValueError) as excinfo:
        am = openam.Openam(openam_url="http://openam.example.com:8080/openam/")
        am.authenticate(username="amadmin", password="password_openam")
        am.get_identity()
    assert excinfo.value.message == 'Please provide a username.'


def test_get_identity():
    """ Will get an identity.
    :return:
    """
    am = openam.Openam(openam_url="http://openam.example.com:8080/openam/")
    am.authenticate(username="amadmin", password="password_openam")
    data = am.get_identity(username="demo")
    am.logout()

    assert data['dn'] == ['uid=demo,ou=people,dc=openam,dc=forgerock,dc=org']


def test_get_identity_wrong_user():
    """ Will get an identity that doesn't exists.
    :return:
    """
    am = openam.Openam(openam_url="http://openam.example.com:8080/openam/")
    am.authenticate(username="amadmin", password="password_openam")
    data = am.get_identity(username="wrong_user")
    am.logout()

    assert not data


def test_get_identity_wrong_type():
    """ Will get an identity with a wrong type.
    :return:
    """
    am = openam.Openam(openam_url="http://openam.example.com:8080/openam/")
    am.authenticate(username="amadmin", password="password_openam")
    data = am.get_identity(username="demo", type="wrong")
    am.logout()

    assert data['dn'] == ['uid=demo,ou=people,dc=openam,dc=forgerock,dc=org']


def test_get_identity_with_fields():
    """ Will get an identity for 1 field.
    :return:
    """
    am = openam.Openam(openam_url="http://openam.example.com:8080/openam/")
    am.authenticate(username="amadmin", password="password_openam")
    data = am.get_identity(username="demo", fields="dn")
    am.logout()

    assert data['dn'] == ['uid=demo,ou=people,dc=openam,dc=forgerock,dc=org']


def test_update_identity():
    """ Will update the identity.
    :return:
    """
    am = openam.Openam(openam_url="http://openam.example.com:8080/openam/")
    am.authenticate(username="amadmin", password="password_openam")
    user_data = {"mail": "demo@example.com"}
    data = am.update_identity(username="demo", user_data=user_data)
    am.logout()

    assert data['mail'] == ['demo@example.com']


def test_update_identity_no_username():
    """ Will update the identity when no username is provided.
    :return:
    """
    with pytest.raises(ValueError) as excinfo:
        am = openam.Openam(openam_url="http://openam.example.com:8080/openam/")
        am.authenticate(username="amadmin", password="password_openam")
        user_data = {}
        am.update_identity(user_data=user_data)
    assert excinfo.value.message == 'Please provide a username.'


def test_update_identity_no_user_data():
    """ Will update an identity when no user_data is provided.
    :return:
    """
    with pytest.raises(ValueError) as excinfo:
        am = openam.Openam(openam_url="http://openam.example.com:8080/openam/")
        am.authenticate(username="amadmin", password="password_openam")
        am.update_identity(username="demo")
    assert excinfo.value.message == 'Please provide correct user information.'


def test_change_password():
    """Will change a password.
    :return:
    """
    am = openam.Openam(openam_url="http://openam.example.com:8080/openam/")
    am.authenticate(username="amadmin", password="password_openam")
    user_data = {"currentpassword": "secret12", "userpassword": "secret13"}
    data = am.change_password(username="bjensen", user_data=user_data)
    am.logout()

    assert data


def test_change_password_false():
    """Will change a password where new and old are same.
    :return:
    """
    am = openam.Openam(openam_url="http://openam.example.com:8080/openam/")
    am.authenticate(username="amadmin", password="password_openam")
    user_data = {"currentpassword": "secret12", "userpassword": "secret12"}
    data = am.change_password(username="bjensen", user_data=user_data)
    am.logout()

    assert not data


def test_change_password_no_username():
    """ Will delete an identity when no username is provided.
    :return:
    """
    with pytest.raises(ValueError) as excinfo:
        am = openam.Openam(openam_url="http://openam.example.com:8080/openam/")
        am.authenticate(username="amadmin", password="password_openam")
        user_data = {"currentpassword": "secret12", "userpassword": "secret13"}
        am.change_password(user_data=user_data)
    assert excinfo.value.message == 'Please provide a username.'


def test_change_password_no_user_data():
    """ Will delete an identity when no username is provided.
    :return:
    """
    with pytest.raises(ValueError) as excinfo:
        am = openam.Openam(openam_url="http://openam.example.com:8080/openam/")
        am.authenticate(username="amadmin", password="password_openam")
        user_data = {"currentpassword": "secret12", "userpassword": "secret13"}
        am.change_password(username="bjensen")
    assert excinfo.value.message == 'Please provide correct user information.'


def test_delete_identity():
    """ Will delete a identity.
    :return:
    """
    am = openam.Openam(openam_url="http://openam.example.com:8080/openam/")
    am.authenticate(username="amadmin", password="password_openam")
    data = am.delete_identity(username="bjensen")
    am.logout()

    assert data == {u'success': u'true'}


def test_delete_identity_no_username():
    """ Will delete an identity when no username is provided.
    :return:
    """
    with pytest.raises(ValueError) as excinfo:
        am = openam.Openam(openam_url="http://openam.example.com:8080/openam/")
        am.authenticate(username="amadmin", password="password_openam")
        am.delete_identity()
    assert excinfo.value.message == 'Please provide a username.'


def test_create_realm():
    """ Will create a realm.
    :return:
    """
    am = openam.Openam(openam_url="http://openam.example.com:8080/openam/")
    am.authenticate(username="amadmin", password="password_openam")
    realm_data = {"realm": "myRealm"}
    data = am.create_realm(realm_data=realm_data)
    am.logout()

    assert data == {u'realmCreated': u'/myRealm'}


def test_create_realm_no_realm_data():
    """ Will delete an identity when no username is provided.
    :return:
    """
    with pytest.raises(ValueError) as excinfo:
        am = openam.Openam(openam_url="http://openam.example.com:8080/openam/")
        am.authenticate(username="amadmin", password="password_openam")
        am.create_realm()
    assert excinfo.value.message == 'Please provide correct realm_data information.'


def test_get_realm():
    """ Will get a realm.
    :return:
    """
    am = openam.Openam(openam_url="http://openam.example.com:8080/openam/")
    am.authenticate(username="amadmin", password="password_openam")
    data = am.get_realm(realm="myRealm")
    am.logout()

    assert len(data['serviceNames']) == 9


def test_get_realm_wrong_realm():
    """ Will get a realm.
    :return:
    """
    am = openam.Openam(openam_url="http://openam.example.com:8080/openam/")
    am.authenticate(username="amadmin", password="password_openam")
    data = am.get_realm(realm="wrong")
    am.logout()

    assert not data


def test_get_realm_no_realm_data():
    """ Will delete an identity when no username is provided.
    :return:
    """
    with pytest.raises(ValueError) as excinfo:
        am = openam.Openam(openam_url="http://openam.example.com:8080/openam/")
        am.authenticate(username="amadmin", password="password_openam")
        am.get_realm()
    assert excinfo.value.message == 'Please provide correct realm name.'


def test_list_realms_wrong_realm():
    """
    :return:
    """
    am = openam.Openam(openam_url="http://openam.example.com:8080/openam/")
    am.authenticate(username="amadmin", password="password_openam")
    data = am.list_realms(realm="wrong")
    assert not data


def test_list_realms():
    """
    :return:
    """
    am = openam.Openam(openam_url="http://openam.example.com:8080/openam/")
    am.authenticate(username="amadmin", password="password_openam")
    data = am.list_realms()
    assert data['result'] == ['/', '/myRealm']


def test_update_realm():
    """ Will create a realm.
    :return:
    """
    am = openam.Openam(openam_url="http://openam.example.com:8080/openam/")
    am.authenticate(username="amadmin", password="password_openam")
    realm_data = {"sunOrganizationStatus": "Inactive"}
    data = am.update_realm(realm="myRealm", realm_data=realm_data)
    am.logout()

    assert data == {u'realmUpdated': u'/myRealm'}


def test_update_realm_no_realm():
    """ Will delete an identity when no username is provided.
    :return:
    """
    with pytest.raises(ValueError) as excinfo:
        am = openam.Openam(openam_url="http://openam.example.com:8080/openam/")
        am.authenticate(username="amadmin", password="password_openam")
        realm_data = {"sunOrganizationStatus": "Inactive"}
        am.update_realm(realm_data=realm_data)
    assert excinfo.value.message == 'Please provide a realm.'


def test_update_realm_no_realm_data():
    """ Will delete an identity when no username is provided.
    :return:
    """
    with pytest.raises(ValueError) as excinfo:
        am = openam.Openam(openam_url="http://openam.example.com:8080/openam/")
        am.authenticate(username="amadmin", password="password_openam")
        am.update_realm(realm="myRealm")
    assert excinfo.value.message == 'Please provide correct realm_data information.'


def test_delete_realm():
    """ Will delete a realm.
    :return:
    """
    am = openam.Openam(openam_url="http://openam.example.com:8080/openam/")
    am.authenticate(username="amadmin", password="password_openam")
    data = am.delete_realm(realm="myRealm")
    am.logout()

    assert data['success']


def test_delete_realm_no_realm():
    """ Will delete an identity when no realm is provided.
    :return:
    """
    with pytest.raises(ValueError) as excinfo:
        am = openam.Openam(openam_url="http://openam.example.com:8080/openam/")
        am.authenticate(username="amadmin", password="password_openam")
        am.delete_realm()
    assert excinfo.value.message == 'Please provide a realm.'


def test_list_resourcetypes(openam_version):
    if openam_version != 12:
        am = openam.Openam(openam_url="http://openam.example.com:8080/openam/")
        am.authenticate(username="amadmin", password="password_openam")
        data = am.list_resourcetypes()
        am.logout()

        assert data['result'][0]['name'] == 'Delegation Service'
    else:
        pass


def test_list_resourcetypes_wrong_query(openam_version):
    if openam_version != 12:
        am = openam.Openam(openam_url="http://openam.example.com:8080/openam/")
        am.authenticate(username="amadmin", password="password_openam")
        data = am.list_resourcetypes(query="wrong")
        am.logout()

        assert not data
    else:
        pass


def test_get_resourcetypes_no_uuid():
    """ Will delete an identity when no realm is provided.
    :return:
    """
    with pytest.raises(ValueError) as excinfo:
        am = openam.Openam(openam_url="http://openam.example.com:8080/openam/")
        am.authenticate(username="amadmin", password="password_openam")
        am.get_resourcetype()
    assert excinfo.value.message == 'Please provide a uuid for a resourcetype.'


def test_get_resourcetypes(openam_version):
    """Get an resourcetype.
    :return:
    """
    if openam_version != 12:
        am = openam.Openam(openam_url="http://openam.example.com:8080/openam/")
        am.authenticate(username="amadmin", password="password_openam")
        data = am.list_resourcetypes()
        data = am.get_resourcetype(uuid=data['result'][0]['uuid'])
        am.logout()

        assert data['name'] == 'Delegation Service'
    else:
        pass


def test_get_resourcetypes_wrong_uuid(openam_version):
    """Get a resourcetype when wrong uuid is given.
    :return:
    """
    if openam_version != 12:
        am = openam.Openam(openam_url="http://openam.example.com:8080/openam/")
        am.authenticate(username="amadmin", password="password_openam")
        data = am.get_resourcetype(uuid="wrong")
        am.logout()

        assert not data
    else:
        pass


def test_create_resourcetype(openam_version):
    """Create a resourcetype.
    :return:
    """
    if openam_version != 12:
        create_resourcetype = {
            "name": "My Resource Type",
            "actions": {
                "LEFT": "true",
                "RIGHT": "true",
                "UP": "true",
                "DOWN": "true"
            },
            "patterns": [
                "http://device/location/*"
            ]
        }
        am = openam.Openam(openam_url="http://openam.example.com:8080/openam/")
        am.authenticate(username="amadmin", password="password_openam")
        data = am.create_resourcetype(resource_data=create_resourcetype)
        am.logout()

        assert data['name'] == 'My Resource Type'
    else:
        pass


def test_create_resourcetypes_no_resource_data():
    """ Will create an resourcetype when no resource_data is provided.
    :return:
    """
    with pytest.raises(ValueError) as excinfo:
        am = openam.Openam(openam_url="http://openam.example.com:8080/openam/")
        am.authenticate(username="amadmin", password="password_openam")
        am.create_resourcetype()
    assert excinfo.value.message == 'Please provide correct resource_data information.'


def test_update_resourcetype(openam_version):
    """Update a resourcetype.
    :return:
    """
    if openam_version != 12:
        am = openam.Openam(openam_url="http://openam.example.com:8080/openam/")
        am.authenticate(username="amadmin", password="password_openam")
        for result in am.list_resourcetypes()['result']:
            if result['name'] == 'My Resource Type':
                uuid = result['uuid']

        resource_data = {
            "uuid": uuid,
            "name": "My Updated Resource Type",
            "actions": {
                "LEFT": "false",
                "RIGHT": "false",
                "UP": "false",
                "DOWN": "false"
            },
            "patterns": [
                "http://device/location/*"
            ]
        }

        data = am.update_resourcetype(uuid=uuid, resource_data=resource_data)
        assert data['name'] == 'My Updated Resource Type'
    else:
        pass


def test_update_resourcetypes_no_resource_data():
    """ Will create an resourcetype when no resource_data is provided.
    :return:
    """
    with pytest.raises(ValueError) as excinfo:
        am = openam.Openam(openam_url="http://openam.example.com:8080/openam/")
        am.authenticate(username="amadmin", password="password_openam")
        am.update_resourcetype(uuid="asas")
    assert excinfo.value.message == 'Please provide correct resource_data information.'


def test_update_resourcetypes_no_uuid():
    """ Will create an resourcetype when no resource_data is provided.
    :return:
    """
    with pytest.raises(ValueError) as excinfo:
        am = openam.Openam(openam_url="http://openam.example.com:8080/openam/")
        am.authenticate(username="amadmin", password="password_openam")
        am.update_resourcetype(resource_data={})
    assert excinfo.value.message == 'Please provide a uuid for a resourcetype.'


def test_delete_resourcetype(openam_version):
    """Will delete an resourcetype.
    :return:
    """
    if openam_version != 12:
        am = openam.Openam(openam_url="http://openam.example.com:8080/openam/")
        am.authenticate(username="amadmin", password="password_openam")
        for result in am.list_resourcetypes()['result']:
            if result['name'] == 'My Updated Resource Type':
                uuid = result['uuid']
        data = am.delete_resourcetype(uuid=uuid)

        assert data == {}
    else:
        pass


def test_delete_resourcetypes_no_uuid():
    """ Will delete an resourcetype when no uuid is provided.
    :return:
    """
    with pytest.raises(ValueError) as excinfo:
        am = openam.Openam(openam_url="http://openam.example.com:8080/openam/")
        am.authenticate(username="amadmin", password="password_openam")
        am.delete_resourcetype()
    assert excinfo.value.message == 'Please provide a uuid for a resourcetype.'
