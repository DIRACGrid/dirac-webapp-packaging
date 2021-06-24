.. -*- mode: rst -*-

dirac-webapp-packaging
======================

.. image:: https://badge.fury.io/py/dirac-webapp-packaging.svg
    :target: https://badge.fury.io/py/dirac-webapp-packaging

Build tools for compiling javascript sources in DIRAC WebApp packages.

Usage
~~~~~

In order to use this to automatically compile javascript sources as part of wheel generation the ``pyproject.toml``:

.. code-block:: toml

  [build-system]
  requires = ["dirac_webapp_packaging~=1.0"]
  build-backend = "setuptools.build_meta"

and, assuming your other metadata is in a ``setup.cfg``, create a ``setup.py`` file containing:

.. code-block:: python

  from dirac_webapp_packaging import extjs_cmdclass
  from setuptools import setup

  setup(cmdclass=extjs_cmdclass)

Changelog
~~~~~~~~~

1.0.0
^^^^^

* Initial release
