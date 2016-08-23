# Contributing

:+1::tada: First off, thanks for taking the time to contribute! :tada::+1:

The following is a set of guidelines for contributing to the `python-openam` python module.
These are just guidelines, not rules, use your best judgment and feel free to propose changes to this document in a pull request.

#### Table Of Contents

[What should I know before I get started?](#what-should-i-know-before-i-get-started)
  * [Tests on Docker](#tests-on-docker)

[How Can I Contribute?](#how-can-i-contribute)
  * [Reporting Bugs](#reporting-bugs)
  * [Suggesting Enhancements](#suggesting-enhancements)
  * [Pull Requests](#pull-requests)

## What should I know before I get started?

### Tests on Docker

The python tests are executed on a OpenAM docker container. When the docker container is booted, a basic site is configured so it can immediately used for the tests.

Travis CI downloads and starts several docker containers:

* wdijkerman/openam:12.0.0
* wdijkerman/openam:13.0.0

The tag represents the version of OpenAM installed in the container.

You can start these containers like this:
```
scripts/start_docker.sh 13.0.0
```

This will start an OpenAM container running version 13.0.0. You'll get the command prompt back when OpenAM is ready to be used.

The tests are executed on the fqdn `openam.example.com`, please make sure this is resolved to the container.

## How Can I Contribute?

### Reporting Bugs

Every piece of software has bugs and there is a really big chance that this module also have one or more bugs.

#### Before Submitting A Bug Report

* Check if there is already a bug reported
* Do you have the most recent version of the module? If not, please update and see if the problem still exists.
* Check the documentation.

#### How Do I Submit A (Good) Bug Report?

Bugs are tracked as [GitHub issues](https://guides.github.com/features/issues/).

Explain the problem and include additional details to help maintainers reproduce the problem:

* **Use a clear and descriptive title** for the issue to identify the problem.
* **Provide specific examples to demonstrate the steps**. Include links to files or GitHub projects, or copy/pasteable snippets, which you use in those examples. If you're providing snippets in the issue, use [Markdown code blocks](https://help.github.com/articles/markdown-basics/#multiple-lines).
* **Describe the behavior you observed after following the steps** and point out what exactly is the problem with that behavior.
* **Explain which behavior you expected to see instead and why.**
* **Please provide information in which version of the module you are using** same as for the python version and which OS.

#### Template For Submitting Bug Reports

    [Short description of problem here]

    **Reproduction Steps:**

    1. [First Step]
    2. [Second Step]
    3. [Other Steps...]

    **Expected behavior:**

    [Describe expected behavior here]

    **Observed behavior:**

    [Describe observed behavior here]

    **Module version:** [Enter python-openam version here]
    **OS and version:** [Enter OS name and python version here]

    **Additional information:**
    [Place some additional information that can help investigate/troubleshoot the problem]

### Suggesting Enhancements

This section guides you through submitting an enhancement suggestion for `python-openam`, including completely new features and minor improvements to existing functionality.

#### Before Submitting An Enhancement Suggestion

* Check if there isn't already an issue created for this and if so, please update the issue or add an :thumbsup:

#### How Do I Submit A (Good) Enhancement Suggestion?

Enhancement suggestions are tracked as [GitHub issues](https://guides.github.com/features/issues/).
Create an issue and provide the following information:

* **Use a clear and descriptive title** for the issue to identify the suggestion.
* **Provide a step-by-step description of the suggested enhancement** in as many details as possible.
* **Describe the current behavior** and **explain which behavior you expected to see instead** and why.

#### Template For Submitting Enhancement Suggestions

    [Short description of suggestion]

    **Steps which explain the enhancement**

    1. [First Step]
    2. [Second Step]
    3. [Other Steps...]

    **Current and suggested behavior**

    [Describe current and suggested behavior here]

### Pull Requests

Before creating the actual Pull Request, make sure the following applies:

* Proper document the code (In the functions and/of docs)
* End files with a newline.
* Avoid platform-dependent code
* validate your tests first

