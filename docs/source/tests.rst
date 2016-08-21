Tests
-----

This module contains some tests. These tests will validate the correct usage of this module.

pep
***

At the moment, there are 2 pep validation tests:

* pep8
* pep257


pep8
====

pep8 Is for validating the python style guide.

pep257
======
Pep257 is used for docstrings


PyTest
******

When the pep tests are completed, PyTest is executed.
First a OpenAM docker container is started. This container boots up an OpenAM instance and configured a basic site with an embedded OpenDJ. When this is booted correctly (It checks every 5 seconds when the isAlive.jsp returns a '200'.)
