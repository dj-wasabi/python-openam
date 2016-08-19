#!/usr/bin/python

import sys
import os

sys.path.insert(0, os.path.abspath('..'))

import openam

am = openam.Openam(openam_url="http://openam.example.com:8080/openam/")
auth_data = am.authenticate(username="amadmin", password="password_openam")
# print(am.token_validation(token=auth_data['tokenId']))
# print(am.token_validation(token="fau1tyt0ken"))
# print(am.get_serverinfo(property="cookieDomains"))


# data = am.get_serverinfo(property="cookieDomains")
# print data['domains']

print(am.session_information(action="getMaxTime", token=auth_data['tokenId']))
print(am.logout())
