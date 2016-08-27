# python-openam

![Coverage](coverage.svg) [![Build Status](https://travis-ci.org/dj-wasabi/python-openam.svg?branch=master)](https://travis-ci.org/dj-wasabi/python-openam) [![PyPI version](https://badge.fury.io/py/python-openam.svg)](https://badge.fury.io/py/python-openam) [![Documentation](https://readthedocs.org/projects/python-openam/badge/?version=latest)](http://python-openam.readthedocs.org/en/latest/?badge=latest)

This is a python module for managing and configuring an OpenAM instance via the API.

## Installation

Installation is very simple:
```
pip install python-openam
```

## Basic usage

Import the module with the import command.
```
import openam
am = openam.Openam(openam_url="http://openam.example.com:8080/openam/")
am.authenticate(username="amadmin", password="password_openam")
am.logout()
```


## OpenAM Versions

The following is working with this OpenAM module.
The following (json/) endpoints work:

| endpoint           | OpenAM 12        | OpenAM 13        |
|--------------------|:----------------:|:----------------:|
| /authenticate      |:white_check_mark:|:white_check_mark:|
| /users             |:white_check_mark:|:white_check_mark:|
| /groups            |:white_check_mark:|:white_check_mark:|
| /agents            |:white_check_mark:|:white_check_mark:|
| /realms            |:white_check_mark:|:white_check_mark:|
| /dashboard         |     :x:          |      :x:         |
| /sessions          |     :x:          |      :x:         |
| /serverinfo/*      |:white_check_mark:|:white_check_mark:|
| /applications      |     :x:          |      :x:         |
| /resourcetypes     |     :x:          |      :x:         |
| /policies          |     :x:          |      :x:         |
| /applicationtypes  |     :x:          |      :x:         |
| /conditiontypes    |     :x:          |      :x:         |
| /subjecttypes      |     :x:          |      :x:         |
| /subjectattributes |     :x:          |      :x:         |
| /decisioncombiners |     :x:          |      :x:         |
| /subjectattributes |     :x:          |      :x:         |


The following (xacml/) endpoints work:

| endpoint           | OpenAM 12        | OpenAM 13        |
|--------------------|:----------------:|:----------------:|
| /policies          |     :x:          |      :x:         |

The following (frrest/) endpoints work:

| endpoint           | OpenAM 12        | OpenAM 13        |
|--------------------|:----------------:|:----------------:|
| /token             |     :x:          |      :x:         |
| /client            |     :x:          |      :x:         |

# Issues

Of course there are issues, please let me know. Also if you want to help me add functionality to the module, let me know and create a Pull Request.
All help is welcome. :-)

