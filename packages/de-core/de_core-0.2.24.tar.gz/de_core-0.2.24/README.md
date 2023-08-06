# core portion of de namespace package

[![GitLab develop](https://img.shields.io/gitlab/pipeline/degroup/de_core/develop?logo=python)](
    https://gitlab.com/degroup/de_core)
[![GitLab release](https://img.shields.io/gitlab/pipeline/degroup/de_core/release?logo=python)](
    https://gitlab.com/degroup/de_core/-/tree/release)
[![PyPIVersion](https://img.shields.io/pypi/v/de_core)](
    https://pypi.org/project/de-core/#history)

>the portions (modules and sub-packages) of the Development Environment for Python are within
the `de` namespace and are providing helper methods and classes for your Python projects.

[![Coverage](https://degroup.gitlab.io/de_core/coverage.svg)](
    https://degroup.gitlab.io/de_core/coverage/de_core_py.html)
[![MyPyPrecision](https://degroup.gitlab.io/de_core/mypy.svg)](
    https://degroup.gitlab.io/de_core/lineprecision.txt)
[![PyLintScore](https://degroup.gitlab.io/de_core/pylint.svg)](
    https://degroup.gitlab.io/de_core/pylint.log)

[![PyPIImplementation](https://img.shields.io/pypi/implementation/de_core)](
    https://pypi.org/project/de-core/)
[![PyPIPyVersions](https://img.shields.io/pypi/pyversions/de_core)](
    https://pypi.org/project/de-core/)
[![PyPIWheel](https://img.shields.io/pypi/wheel/de_core)](
    https://pypi.org/project/de-core/)
[![PyPIFormat](https://img.shields.io/pypi/format/de_core)](
    https://pypi.org/project/de-core/)
[![PyPIStatus](https://img.shields.io/pypi/status/de_core)](
    https://libraries.io/pypi/de-core)
[![PyPIDownloads](https://img.shields.io/pypi/dm/de_core)](
    https://pypi.org/project/de-core/#files)


## installation

execute the following command to use the `de.core` module in your Python project. it will install `de.core` into your
Python (virtual) environment:
 
```shell script
pip install de-core
```

to contribute to this portion, fork the
[`de-core` repository at GitLab](https://gitlab.com/degroup/de_core "de.core code repository"),
pull it to your machine and finally execute the following command in the root folder of this repository (`de_core`):

```shell script
pip install -e .[dev]
```

the last command will install this module portion into your virtual environment, along with the tools you need to
develop and run tests or to extend the portion documentation. to contribute only to the unit tests, or the documentation
of this portion replace the setup extras key `dev` in the above command with `tests` or `docs` respectively.

the repository of this portion is using the `git-flow workflow` with the branch names `develop` and `release`. more
details on this workflow you find [here](https://nvie.com/posts/a-successful-git-branching-model/) and 
[here](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow).


## namespace portion documentation

more info on the features and usage of this portion is available at
[ReadTheDocs](https://de.readthedocs.io/en/latest/_autosummary/de.core.html#module-de.core
"de_core documentation").
