"""Test script for python-openam"""

import sys
import os
import pytest

my_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, my_path + '/../')

import openam


def test___init__openam_url():
    """ Will test __init__ function if syncope_url is provided.
    :return:
    """
    with pytest.raises(ValueError) as excinfo:
        openam.Openam()
    assert excinfo.value.message == 'This interface needs an OpenAM URL to work!'


def test_authenticate():
    """
    :return:
    """
    am = openam.Openam(openam_url="http://openam.example.com:8080/openam/")
    auth_data = am.authenticate(username="amadmin", password="password_openam")
    am.logout()
    assert auth_data['successUrl'] == '/openam/console'


def test_authenticate_wrong_realm():
    """
    :return:
    """
    am = openam.Openam(openam_url="http://openam.example.com:8080/openam/")
    auth_data = am.authenticate(realm="wrong", username="amadmin", password="wrong_password")
    am.logout()
    assert not auth_data


def test_authenticate_wrong_password():
    """
    :return:
    """
    am = openam.Openam(openam_url="http://openam.example.com:8080/openam/")
    auth_data = am.authenticate(username="amadmin", password="wrong_password")
    am.logout()
    assert not auth_data


def test_authenticate_no_username():
    """ Will test __init__ function if syncope_url is provided.
    :return:
    """
    with pytest.raises(ValueError) as excinfo:
        am = openam.Openam(openam_url="http://openam.example.com:8080/openam/")
        am.authenticate(password="password_openam")
    assert excinfo.value.message == 'You will need to provide a username to login.'


def test_authenticate_no_password():
    """ Will test __init__ function if syncope_url is provided.
    :return:
    """
    with pytest.raises(ValueError) as excinfo:
        am = openam.Openam(openam_url="http://openam.example.com:8080/openam/")
        am.authenticate(username="amadmin")
    assert excinfo.value.message == 'You will need to provide a password to login.'


def test_logout():
    """
    :return:
    """
    am = openam.Openam(openam_url="http://openam.example.com:8080/openam/")
    am.authenticate(username="amadmin", password="password_openam")
    assert am.logout()


def test_logout_realm_wrong():
    """
    :return:
    """
    am = openam.Openam(openam_url="http://openam.example.com:8080/openam/")
    am.authenticate(username="amadmin", password="password_openam")
    assert not am.logout(realm="wrong")


def test_get_serverinfo():
    """
    :return:
    """
    am = openam.Openam(openam_url="http://openam.example.com:8080/openam/")
    am.authenticate(username="amadmin", password="password_openam")
    data = am.get_serverinfo()
    am.logout()
    assert data['selfRegistration'] == 'false'


def test_get_serverinfo_with_property():
    """
    :return:
    """
    am = openam.Openam(openam_url="http://openam.example.com:8080/openam/")
    am.authenticate(username="amadmin", password="password_openam")
    data = am.get_serverinfo(property="cookieDomains")
    am.logout()
    assert data['domains'] == ['.example.com']


def test_get_serverinfo_with_wrong_property():
    """
    :return:
    """
    am = openam.Openam(openam_url="http://openam.example.com:8080/openam/")
    am.authenticate(username="amadmin", password="password_openam")
    data = am.get_serverinfo(property="wrong")
    am.logout()
    assert not data


def test_token_validation():
    """
    :return:
    """
    am = openam.Openam(openam_url="http://openam.example.com:8080/openam/")
    auth_data = am.authenticate(username="amadmin", password="password_openam")
    data = am.token_validation(token=auth_data['tokenId'])
    am.logout()
    assert data


def test_token_validation_wrong():
    """
    :return:
    """
    am = openam.Openam(openam_url="http://openam.example.com:8080/openam/")
    auth_data = am.authenticate(username="amadmin", password="password_openam")
    data = am.token_validation(token="wrong")
    am.logout()
    assert not data['valid']


def test_session_information():
    """
    :return:
    """
    am = openam.Openam(openam_url="http://openam.example.com:8080/openam/")
    auth_data = am.authenticate(username="amadmin", password="password_openam")
    data = am.session_information(action="getMaxTime", token=auth_data['tokenId'])
    am.logout()
    assert data['maxtime'] == 7200


def test_session_information_wrong_action():
    """
    :return:
    """
    am = openam.Openam(openam_url="http://openam.example.com:8080/openam/")
    auth_data = am.authenticate(username="amadmin", password="password_openam")
    data = am.session_information(action="wrong", token=auth_data['tokenId'])
    am.logout()
    assert not data


def test_session_information_no_action():
    """ Will test __init__ function if syncope_url is provided.
    :return:
    """
    with pytest.raises(ValueError) as excinfo:
        am = openam.Openam(openam_url="http://openam.example.com:8080/openam/")
        auth_data = am.authenticate(username="amadmin", password="password_openam")
        am.session_information(token=auth_data['tokenId'])
    assert excinfo.value.message == 'Please provide a correct action you want to take.'


def test_session_information_no_token():
    """ Will test __init__ function if syncope_url is provided.
    :return:
    """
    with pytest.raises(ValueError) as excinfo:
        am = openam.Openam(openam_url="http://openam.example.com:8080/openam/")
        am.authenticate(username="amadmin", password="password_openam")
        am.session_information(action="getMaxTime")
    assert excinfo.value.message == 'Please provide a token.'
