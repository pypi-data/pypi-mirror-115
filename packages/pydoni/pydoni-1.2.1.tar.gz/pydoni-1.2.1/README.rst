######
pydoni
######

   A Python module for custom-built tools designed and maintained by Andoni Sooklaris.

Getting Started
===============

``pydoni`` is a multi-functional Python package that contains tools for handling OS/system operations, Python object operations, verbosity, shell command wrappers, prompting for user input, Postgres database interaction and webscraping utilities.

Prerequisites
-------------

* ``pip``

Installation
------------

.. code-block:: bash

   pip install pydoni

Releasing
---------

``pydoni`` utilizes `versioneer <https://pypi.org/project/versioneer/>`_ for versioning. This requires the ``versioneer.py`` in the project's top-level directory, as well as some lines in the package's ``setup.cfg`` and ``__init__.py``.

1. Make your changes locally and push to ``develop`` or a different feature branch.

2. Tag the new version. This will be the version of the package once publication to PyPi is complete.

   .. code-block:: bash

      git tag {major}.{minor}.{patch}

3. Publish to PyPi.

   .. code-block:: bash

      rm -rf ./dist && python3 setup.py sdist && twine upload -r pypi dist/*

4. Install the new version of ``pydoni``.

   .. code-block:: bash

      pip install pydoni=={major}.{minor}.{patch}

5. Create a `pull request <https://github.com/tsouchlarakis/pydoni/pulls>`_.

Changelog
=========

See `changelog <Changelog.rst>`_.

License
=======

See `license <LICENSE>`_.

.. raw:: html

   <div style="display: flex; justify-content: center;">
     <img src="img/logo.png" style="width: 300px; height: 300px;" />
   </div>
