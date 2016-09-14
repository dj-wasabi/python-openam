
python-openam
=============

.. image:: https://readthedocs.org/projects/python-openam/badge/?version=latest
    :target: http://python-openam.readthedocs.org/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://travis-ci.org/dj-wasabi/python-openam.svg?branch=master
    :target: https://travis-ci.org/dj-wasabi/python-openam
    :alt: Build Status

.. image:: https://badge.fury.io/py/python-openam.svg
    :target: https://badge.fury.io/py/python-openam

.. image:: https://cdn.rawgit.com/dj-wasabi/python-openam/master/coverage.svg

This module is a python wrapper for the OpenAM API. With this module you can easy make use of the OpenAM API. The goal is to fully configure an OpenAM instance via the API.

Information:

* Github page: https://github.com/dj-wasabi/python-openam
* PyPi page: https://pypi.python.org/pypi/python-openam
* Docker container: https://hub.docker.com/r/wdijkerman/openam/


OpenAM Versions
***************

This python module should work with the following versions of OpenAM:

* 12.0.0
* 13.0.0

Tests will validate that the module works on these versions. There is no plan yet to update the module so it can also handle older "legacy" versions.

What is working in the current version of this module.
The following (json/) endpoints work:

+--------------------+------------+-----------+
| endpoint           | OpenAM 12  | OpenAM 13 |
+====================+============+===========+
| /authenticate      |  V         |    V      |
+--------------------+------------+-----------+
| /users             |  V         |    V      |
+--------------------+------------+-----------+
| /groups            |  V         |    V      |
+--------------------+------------+-----------+
| /agents            |  V         |    V      |
+--------------------+------------+-----------+
| /realms            |  V         |    V      |
+--------------------+------------+-----------+
| /dashboard         |  .         |    .      |
+--------------------+------------+-----------+
| /sessions          |  V         |    V      |
+--------------------+------------+-----------+
| /serverinfo/*      |  V         |    V      |
+--------------------+------------+-----------+
| /applications      |  .         |    .      |
+--------------------+------------+-----------+
| /resourcetypes     |  n.a.      |    V      |
+--------------------+------------+-----------+
| /policies          |  .         |    .      |
+--------------------+------------+-----------+
| /applicationtypes  |  .         |    .      |
+--------------------+------------+-----------+
| /conditiontypes    |  .         |    .      |
+--------------------+------------+-----------+
| /subjecttypes      |  .         |    .      |
+--------------------+------------+-----------+
| /subjectattributes |  .         |    .      |
+--------------------+------------+-----------+
| /decisioncombiners |  .         |    .      |
+--------------------+------------+-----------+
| /subjectattributes |  .         |    .      |
+--------------------+------------+-----------+

V = Works

. = Not working (yet)


The following (xacml/) endpoints work:

+--------------------+------------+-----------+
| endpoint           | OpenAM 12  | OpenAM 13 |
+====================+============+===========+
| /policies          |  .         |    .      |
+--------------------+------------+-----------+

The following (frrest/) endpoints work:

+--------------------+------------+-----------+
| endpoint           | OpenAM 12  | OpenAM 13 |
+====================+============+===========+
| /token             |  .         |    .      |
+--------------------+------------+-----------+
| /client            |  .         |    .      |
+--------------------+------------+-----------+


Installation
************

Installation is very simple, execute the following command:

.. code:: bash

    pip install python-openam

Module is installed and can be used.

Example usage
*************

The following is a basic example for authenticating and doing an logout on OpenAM:

.. code:: python

    import openam

    am = openam.Openam(openam_url="http://openam.example.com:8080/openam/")
    am.authenticate(username="amadmin", password="password_openam")
    am.logout()

You'll have to update the 'openam_url' and both the 'username' and 'password' for your setup.


Creating an identity

.. code:: python

    import openam
    am = openam.Openam(openam_url="http://openam.example.com:8080/openam/")
    auth_data = am.authenticate(username="amadmin", password="password_openam")
    user_data = {"username": "bjensen", "userpassword": "secret12", "mail": "bjensen@example.com"}

    am.create_identity(user=user_data)
    {u'username': u'bjensen', u'dn': [u'uid=bjensen,ou=people,dc=openam,dc=forgerock,dc=org'], u'realm': u'/'..}
    am.create_identity(user=user_data)
    {u'reason': u'Conflict', u'code': 409, u'message': u'Resource already exists'}
    am.logout()


Issues
******

Of course there are issues, please let me know. Also if you want to help me add functionality to the module, let me know and create a Pull Request.

All help is welcome. :-)
