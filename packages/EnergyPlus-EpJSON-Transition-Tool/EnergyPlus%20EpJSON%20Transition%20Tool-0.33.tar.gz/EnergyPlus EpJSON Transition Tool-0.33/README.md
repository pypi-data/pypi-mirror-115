# EpJSON Transition

[![GitHub release](https://img.shields.io/github/release/myoldmopar/epjsontransition.svg?style=for-the-badge)](https://github.com/myoldmopar/epjsontransition/releases/latest)

This tool provides a library, along with a command line interface, fully packaged binaries, and
PyPi distributed wheels, for doing conversion of EnergyPlus EpJSON files.  While EpJSON files may not change
significantly between versions, there are still changes required sometimes.  At a minimum the version number.

## Documentation

[![Documentation Status](https://readthedocs.org/projects/epjson-transition/badge/?version=latest&style=for-the-badge)](https://epjson-transition.readthedocs.io/en/latest/?badge=latest)

Documentation is built by Sphinx and automatically generated and hosted on ReadTheDocs.

## Testing

[![Unit Tests](https://img.shields.io/github/workflow/status/Myoldmopar/EpJSONTransition/Test?label=Unit%20Tests&style=for-the-badge)](https://github.com/Myoldmopar/EpJSONTransition/actions?query=workflow%3A%22Test%22)
[![Coverage Status](https://img.shields.io/coveralls/github/Myoldmopar/EpJSONTransition?label=Coverage&style=for-the-badge)](https://coveralls.io/github/Myoldmopar/EpJSONTransition?branch=main)
[![PEP8 Enforcement](https://img.shields.io/github/workflow/status/Myoldmopar/EpJSONTransition/Flake8?label=Flake8&style=for-the-badge)](https://github.com/Myoldmopar/EpJSONTransition/actions?query=workflow%3AFlake8)

The project is tested using standard Python unit testing practices.
Each commit is automatically tested with Github Actions on Windows, Mac, Ubuntu 18.04 and Ubuntu 20.04.
The code coverage across platforms is collected on Coveralls.
When a tag is created in the GitHub Repo, Github Actions builds downloadable packages.

To run the unit test suite, make sure to have nose and coverage installed via: `pip install nose coverage`.
Then execute `coverage run setup.py nosetests`.
Unit test results will appear in the console, and coverage results will be in a `htmlcov` directory.

## Releases

[![Releases](https://img.shields.io/github/workflow/status/Myoldmopar/EpJSONTransition/PyInstallerRelease?label=PyInstaller%20Release&style=for-the-badge)](https://github.com/Myoldmopar/EpJSONTransition/actions?query=workflow%3APyInstallerRelease)
[![Releases](https://img.shields.io/github/workflow/status/Myoldmopar/EpJSONTransition/PyInstallerRelease?label=PyPI%20Release&style=for-the-badge)](https://github.com/Myoldmopar/EpJSONTransition/actions?query=workflow%3APyPIRelease)
[![Releases](https://img.shields.io/pypi/wheel/EnergyPlus-EpJSON-Transition-Tool?label=PyPi%20Wheel&style=for-the-badge)](https://pypi.org/project/EnergyPlus-EpJSON-Transition-Tool/)

Releases will be made periodically at meaningful milestones.
Each release tag results in pyinstaller-based prebuilt binaries available on the release asset page, and an updated PyPi wheel.