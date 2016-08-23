# Contributing

Of course you may help contributing to the `python-openam` package. I'm very happy if you do want to help.
There are some rules that needs to be following before your work is accepted. This work can be just fixing some typos, improve CI testing or adding new functions.

## Setup

### Fork

Fork on GitHub the `python-openam` repository. Checkout this forked repository on you computer and create a new branch.

### Branch

Branch name should be clear on what the purpose is of the change. (KISS)

```
git checkout -b add_policy_functions
```

### Commit

Make/do your changes.
Don't forget the following:

* Proper document the functions like the rest.
* Add if needed extra documentation, found in the `docs/source` directory.
* Make sure that each new function is tested properly.
* Code should be `pep8` and `pep257` compliant.
* Have fun with it. :-)


## Tests

This module does have tests configured.

### Docker

The python tests (Mentioned in next paragraph) are executed against an OpenAM docker container. When the docker container is booted, a basic site is configured so it can immediately used for the tests.

Travis CI downloads and starts several docker containers:

* wdijkerman/openam:12.0.0
* wdijkerman/openam:13.0.0

The tag represents the version of OpenAM installed.

You can start these containers like this:
```
scripts/start_docker.sh 12.0.0
```

This will start an OpenAM container running version 12.0.0. You'll get the command prompt back when OpenAM is ready to be used.

note:
Please make sure you have set the following in your hosts file:
`127.0.0.1  openam.example.com`

If hosts file is not correct, all tests will fail.

### PyTest

```
python setyp.py test
```

If all is running correctly (On all available OpenAM versions), you are done and you can push the code and create a Pull Request.

## Pull Request

Pull Request can be made. When a new PR is made, please fill in all necessary details.
When the Travis CI tests completes successfully, the PR will be accepted.

# Summary

Just have fun with coding. :-)
