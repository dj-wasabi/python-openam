Introduction
============

This module is a python wrapper for the OpenAM API. With this module you can easy make use of the OpenAM API. The goal is to fully configure an OpenAM instance via the API.

Github page: https://github.com/dj-wasabi/python-openam

OpenAM Versions
***************

This python module should work with the following versions of OpenAM:

* 12.0.0
* 13.0.0

Tests will validate that the module works on these versions.

What is working in the current version of this module.
The following (json/) endpoints work:

+--------------------+------------+-----------+
| endpoint           | OpenAM 12  | OpenAM 13 |
+====================+============+===========+
| /authenticate      |  √         |   √       |
+--------------------+------------+-----------+
| /users             |  √         |    √      |
+--------------------+------------+-----------+
| /groups            |  √         |    √      |
+--------------------+------------+-----------+
| /agents            |  √         |    √      |
+--------------------+------------+-----------+
| /realms            |  √         |    √      |
+--------------------+------------+-----------+
| /dashboard         |  .         |    .      |
+--------------------+------------+-----------+
| /sessions          |  .         |    .      |
+--------------------+------------+-----------+
| /serverinfo/*      |  √         |    √      |
+--------------------+------------+-----------+
| /applications      |  .         |    .      |
+--------------------+------------+-----------+
| /resourcetypes     |  .         |    .      |
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
