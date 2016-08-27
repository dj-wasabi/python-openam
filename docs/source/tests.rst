Tests
-----

This page is only for those who want to know more about this module instead of using it. On this page you'll find some information that is needed when you are about fixing issues or adding new functionality.

This module contain tests. These tests will validate the correct usage of this module.

Coverage
********

Coverage tool is installed and checks what the coverage is of the tests against the code.
An svg file is created with the command following command:

.. code:: bash

    python setup.py cov

The image is used in the documentation. There is no 'fail' command yet when it reaches below a certain percentage.

pep
***

At the moment, there are 2 pep validation tests:

* pep8
* pep257

`pep8` Is for validating the python style guide and `pep257` is used for validating the docstrings style guide.
The are executed with the following command:

.. code:: bash

    python setup.py pep


In `setup.cfg` a configuration is added to extend the max-line-length check.

.. code:: bash

    [pep8]
    max-line-length = 160

80 Chars is not from this time anymore.

The exit status of the previous mentioned pep command should be 0, otherwise the CI test fails.

PyTest
******

PyTest is used for testing this module.

Docker
~~~~~~

For correct usage of the tests, an OpenAM instance should be available to test on. A docker container is started with OpenAM to make sure there is an environment to test on.
This docker container can be found here: https://hub.docker.com/r/wdijkerman/openam/

The container has at the moment 2 tags:

* 12.0.0
* 13.0.0

First, the container is downloaded:

.. code:: bash

    TAG=${1:-13.0.0}

    # Start docker OpenAM ${TAG}
    docker pull wdijkerman/openam:${TAG}
    docker run -d -h openam.example.com --name openam -p 127.0.0.1:8080:8080 wdijkerman/openam:${TAG}

    until curl -Is http://127.0.0.1:8080/openam/isAlive.jsp | head -n 1 | grep "200 OK" >/dev/null; do
        sleep 5
    done

    echo "OpenAM with tag ${TAG} is started and is available"

The above snippet can be found in the python-openam repository in `scripts/start_docker.sh` and can be used in the following way:

.. code:: bash

    scripts/start_docker.sh 12.0.0

or:

.. code:: bash

    scripts/start_docker.sh 13.0.0

When the container is booted, Tomcat will be started with OpenAM. When start of Tomcat is successful, a script will configure a basic site in OpenAM. As backend, an embedded OpenDJ is used.
During boot, every 5 seconds the `isAlive.jsp` is requested to see if the OpenAM is configured. When the site is configured, the container is available to be used.

When you want to login via the GUI, please use the following credentials:

**OpenAM**

Username: amadmin

Password: password_openam

If you need access to OpenDJ, make sure you change the docker run command and add `-p 50389:50389` to the commandline. Now you can access OpenDJ on port 50389:

**OpenDJ**

Username: cn=Directory Manager

Password: password_opendj


PyTest
~~~~~~

The tests are executed with the following command:

.. code:: bash

    python setup.py test

**Hosts file**

The hosts file should be updated, so that the name `openam.example.com` is resolved to the host running the container.


.. code:: bash

    echo '127.0.0.1     openam.example.com' >> /etc/hosts

When host file is correct, you can execute the tests.
Example output of all correct tests:

.. code:: bash

    running test
    running egg_info
    writing requirements to python_openam.egg-info/requires.txt
    writing python_openam.egg-info/PKG-INFO
    writing top-level names to python_openam.egg-info/top_level.txt
    writing dependency_links to python_openam.egg-info/dependency_links.txt
    reading manifest file 'python_openam.egg-info/SOURCES.txt'
    writing manifest file 'python_openam.egg-info/SOURCES.txt'
    running build_ext
    =============================================== test session starts ================================================
    platform linux2 -- Python 2.7.5, pytest-3.0.1, py-1.4.31, pluggy-0.3.1 -- /usr/bin/python
    cachedir: .cache
    rootdir: /git/python/python-openam, inifile:
    plugins: cov-2.3.1, xdist-1.14, testinfra-1.4.1
    collected 61 items

    tests/test_openam.py::test___init__openam_url PASSED
    tests/test_openam.py::test__get PASSED
    tests/test_openam.py::test__post PASSED
    tests/test_openam.py::test__post_wrong_port PASSED
    tests/test_openam.py::test__put PASSED
    tests/test_openam.py::test__put_wrong_port PASSED
    tests/test_openam.py::test__delete PASSED
    tests/test_openam.py::test__delete_wrong_port PASSED
    tests/test_openam.py::test__uri_realm_creator PASSED
    tests/test_openam.py::test__uri_realm_creator_test_realm PASSED
    tests/test_openam.py::test__type_validator PASSED
    tests/test_openam.py::test__type_validator_wrong_type PASSED
    tests/test_openam.py::test_authenticate PASSED
    tests/test_openam.py::test_authenticate_wrong_realm PASSED
    tests/test_openam.py::test_authenticate_wrong_password PASSED
    tests/test_openam.py::test_authenticate_no_username PASSED
    tests/test_openam.py::test_authenticate_no_password PASSED
    tests/test_openam.py::test_logout PASSED
    tests/test_openam.py::test_logout_realm_wrong PASSED
    tests/test_openam.py::test_get_serverinfo PASSED
    tests/test_openam.py::test_get_serverinfo_with_property PASSED
    tests/test_openam.py::test_get_serverinfo_with_wrong_property PASSED
    tests/test_openam.py::test_token_validation PASSED
    tests/test_openam.py::test_token_validation_wrong PASSED
    tests/test_openam.py::test_token_validation_wrong_realm PASSED
    tests/test_openam.py::test_session_information PASSED
    tests/test_openam.py::test_session_information_wrong_action PASSED
    tests/test_openam.py::test_session_information_no_action PASSED
    tests/test_openam.py::test_session_information_no_token PASSED
    tests/test_openam.py::test_create_identity_no_user_data PASSED
    tests/test_openam.py::test_create_identity PASSED
    tests/test_openam.py::test_create_identity_with_wrong_type PASSED
    tests/test_openam.py::test_list_identities PASSED
    tests/test_openam.py::test_list_identities_user_demo PASSED
    tests/test_openam.py::test_list_identities_user_demo_wrong_type PASSED
    tests/test_openam.py::test_get_identity_no_username PASSED
    tests/test_openam.py::test_get_identity PASSED
    tests/test_openam.py::test_get_identity_wrong_user PASSED
    tests/test_openam.py::test_get_identity_wrong_type PASSED
    tests/test_openam.py::test_get_identity_with_fields PASSED
    tests/test_openam.py::test_update_identity PASSED
    tests/test_openam.py::test_update_identity_no_username PASSED
    tests/test_openam.py::test_update_identity_no_user_data PASSED
    tests/test_openam.py::test_change_password PASSED
    tests/test_openam.py::test_change_password_false PASSED
    tests/test_openam.py::test_change_password_no_username PASSED
    tests/test_openam.py::test_change_password_no_user_data PASSED
    tests/test_openam.py::test_delete_identity PASSED
    tests/test_openam.py::test_delete_identity_no_username PASSED
    tests/test_openam.py::test_create_realm PASSED
    tests/test_openam.py::test_create_realm_no_realm_data PASSED
    tests/test_openam.py::test_get_realm PASSED
    tests/test_openam.py::test_get_realm_wrong_realm PASSED
    tests/test_openam.py::test_get_realm_no_realm_data PASSED
    tests/test_openam.py::test_list_realms_wrong_realm PASSED
    tests/test_openam.py::test_list_realms PASSED
    tests/test_openam.py::test_update_realm PASSED
    tests/test_openam.py::test_update_realm_no_realm PASSED
    tests/test_openam.py::test_update_realm_no_realm_data PASSED
    tests/test_openam.py::test_delete_realm PASSED
    tests/test_openam.py::test_delete_realm_no_realm PASSED

    -------------------------- generated xml file: /git/python/python-openam/docs/results.xml --------------------------

    ---------- coverage: platform linux2, python 2.7.5-final-0 -----------
    Name                 Stmts   Miss  Cover   Missing
    --------------------------------------------------
    openam/__init__.py     197      0   100%

    ============================================ 61 passed in 1.80 seconds =============================================

All tests should have state `PASSED`. When there is a `FAILED` test, the CI stops and action should be taken to fix the issue.
The goal is to have a coverage of 100%.
