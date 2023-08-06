
Changelog
=========

All notable changes to this project will be documented in this file.

The format is based on `Keep a Changelog <https://keepachangelog.com/en/1.0.0/>`_\ ,
and this project adheres to `Semantic Versioning <https://semver.org/spec/v2.0.0.html>`_.


.. raw:: html


.. V.V.V (YYYY-MM-DD)
.. ------------------
.. **Added**

.. **Changed**

.. **Deprecated**

.. **Removed**

.. **Fixed**

.. **Security**

1.2.0 (2021-08-08)
------------------
**Added**
    - A few ``Postgres`` class methods
    - Tests for ``Postgres`` class methods

**Changed**
    - Consolidated ``if_exists``, ``if_not_exists`` and ``or_replace`` Postgres class methods

**Deprecated**

**Removed**

**Fixed**

**Security**

1.1.10 (2021-08-01)
------------------
**Added**

- iMessage dashboard tracking
- ``pydoni opsys du-by-filetype`` now handles multiple input directories
- A few keywords to instagram hashtags command

**Changed**

- Name of function ``delete_empty_subdirs()`` to ``remove_empty_subfolders()``
- Updated app defaults
- Updated some default CLI command behavior
- Renamed ``m4a_to_mp3()`` function to ``.to_mp3()`` class method
- iMessage QC view logic update

**Deprecated**

**Removed**

- Untracked raw manual contact name table data

**Fixed**

**Security**


1.1.9 (2021-06-02)
------------------
**Added**

**Changed**

**Deprecated**

**Removed**

- ``app_default_param_values.yaml``

**Fixed**

- Incorrect call to ``datetime`` module

**Security**


1.1.8 (2021-05-31)
------------------
**Added**

- Support for conditional CLI imports
- Releasing instructions in README.rst

**Changed**

- Requirements

**Deprecated**

**Removed**

- ``test_version()``
- More unnecessary files

**Fixed**

**Security**


1.1.4 (2021-05-31)
------------------
**Added**

- ``versioneer`` support

**Changed**

**Deprecated**

**Removed**

**Fixed**

**Security**


1.1.3 (2021-05-31)
------------------
**Added**

- Full click command support

**Changed**

- Requirements updates

**Deprecated**

**Removed**

- Unnecessary imports

**Fixed**

**Security**


1.1.2 (2021-05-31)
------------------
**Added**

**Changed**

**Deprecated**

**Removed**

**Fixed**

- Imports for ``imessage workflow-elt``
- View definition

**Security**


1.1.1 (2021-05-31)
------------------
**Added**

- Proper imports for ``imessage workflow-elt``

**Changed**

**Deprecated**

**Removed**

**Fixed**

**Security**


1.1.0 (2021-05-30)
------------------
**Added**

**Changed**

- Defualt logging level to ``ERROR``
- Moved CLI commands from pydoni-cli repo to ``cli_*.py`` files, simplifying imports

**Deprecated**

**Removed**

**Fixed**

- Parameter ``tmutil_bin`` in Time Machine functions

**Security**


1.0.0 (2021-05-24)
------------------
**Added**

- ``pytest`` suite support
- Type hints in __init__.py

**Changed**

- Project format modeled after ``cookiecutter``
- Markdown documentation converted to RST

**Deprecated**

- Package submodules - now all submodule functions and classes are stored in top-level package in __init__.py

**Removed**

**Fixed**

**Security**


0.2.5 (2021-05-13)
------------------
**Added**

- Sub-package compatibility with Pypi

**Changed**

**Deprecated**

**Removed**

**Fixed**

**Security**


0.2.4 (2021-05-12)
------------------
**Added**

**Changed**

- Requirements

**Deprecated**

**Removed**

**Fixed**

**Security**


0.2.3 (2021-05-11)
------------------
**Added**

- ``pip-tools`` integration
- Support on pypi

**Changed**

- Changelog version history format
- Minor changes to README

**Deprecated**

**Removed**

**Fixed**

**Security**


0.2.2 (2021-04-13)
------------------
**Added**

- New exists class methods for ``Postgres``

**Changed**

- Version format consistent with Pypi

**Deprecated**

**Removed**

**Fixed**

**Security**


0.2.1 (2020-10-21)
------------------
**Added**

- Function ``test_url()``
- Register for pydoni-cli

**Changed**

- Changelog template
- Versioning notation
- ``test_value()`` overhaul
- Colorized logger

**Deprecated**

**Removed**

**Fixed**

- #2

**Security**


0.2.0 (2020-04-29)
------------------
**Added**

- All scripts migrated from ``pydoni-scripts`` repository
- Backend support for updating Postgres database used in ``pydoni-cli`` application

**Changed**

- Refreshed requirements.txt
- Refreshed icon

**Deprecated**

**Removed**

**Fixed**

**Security**


0.1.0 (2020-04-29)
------------------
**Added**

- Initial release!
- All submodules in ``pydoni`` module up until April 29, 2020

**Changed**

**Deprecated**

**Removed**

**Fixed**

**Security**
