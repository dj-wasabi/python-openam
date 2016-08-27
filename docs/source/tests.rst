Tests
-----

This module contains some tests. These tests will validate the correct usage of this module.

Coverage
********

Coverage tool is installed and checks what the coverage is of the tests against the code.
The test fails when the coverage is below 85%.

pep
***

At the moment, there are 2 pep validation tests:

* pep8
* pep257

pep8 Is for validating the python style guide. First test is validating if the module complies with this standard. Pep257 is used for validating the docstrings.

PyTest
******

When the pep tests are completed, PyTest is executed.
First a OpenAM docker container is started. This container boots up an OpenAM instance and configured a basic site with an embedded OpenDJ. When the docker container is booted correctly (It checks every 5 seconds when the isAlive.jsp returns a '200'.) all tests are executed.
