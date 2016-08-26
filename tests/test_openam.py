"""Test script for python-openam"""

import sys
import os
import pytest

my_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, my_path + '/../')

import openam


def test___init__openam_url():
    """Test __init__ function if openam_url is provided.
    :return:
    """
    with pytest.raises(ValueError) as excinfo:
        openam.Openam()
    assert excinfo.value.message == 'This interface needs an OpenAM URL to work!'


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
    user_data = '{"username": "bjensen", "userpassword": "secret12", "mail": "bjensen@example.com"}'
    data = am.create_identity(user_data=user_data)
    am.logout()

    assert data['dn'] == ['uid=bjensen,ou=people,dc=openam,dc=forgerock,dc=org']


def test_create_identity_with_wrong_type():
    """ Will create an identity with the wrong type. Will be set to 'users'
    :return:
    """
    am = openam.Openam(openam_url="http://openam.example.com:8080/openam/")
    am.authenticate(username="amadmin", password="password_openam")
    user_data = '{"username": "bjensen", "userpassword": "secret12", "mail": "bjensen@example.com"}'
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

    assert (my_data['result'][0]['username']) == 'bjensen'


def test_list_identities_user_demo():
    """Find user named demo.
    :return:
    """
    am = openam.Openam(openam_url="http://openam.example.com:8080/openam/")
    am.authenticate(username="amadmin", password="password_openam")
    my_data = am.list_identities(query="demo")
    am.logout()

    assert (my_data['result'][0]['username']) == 'demo'


def test_list_identities_user_demo_wrong_type():
    """Find user named demo with wrong type.
    :return:
    """
    am = openam.Openam(openam_url="http://openam.example.com:8080/openam/")
    am.authenticate(username="amadmin", password="password_openam")
    my_data = am.list_identities(query="demo", type="wrong")
    am.logout()

    assert (my_data['result'][0]['username']) == 'demo'


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
    user_data = '{ "mail": "demo@example.com" }'
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
        user_data = '{}'
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

