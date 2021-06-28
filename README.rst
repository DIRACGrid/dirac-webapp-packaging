.. -*- mode: rst -*-

dirac-webapp-packaging
======================

.. image:: https://badge.fury.io/py/dirac-webapp-packaging.svg
    :target: https://badge.fury.io/py/dirac-webapp-packaging

Build tools for compiling javascript sources in DIRAC WebApp packages.

Usage
~~~~~

These instructions assume you are using a ``setup.cfg`` file to use ``setuptools`` to build your package with versioning being handled by ``setuptools-scm``.

In order to use this to automatically compile javascript sources as part of wheel generation the ``pyproject.toml``:

.. code-block:: toml

  [build-system]
  requires = ["dirac_webapp_packaging~=1.0", "WebAppDIRAC ~=4.3.0a0", "setuptools_scm[toml]>=3.4"]
  build-backend = "setuptools.build_meta"

  [tool.setuptools_scm]
  # Avoid letting setuptools_scm use old style tags (i.e. vXrYpZ)
  git_describe_command = "git describe --dirty --tags --long --match *[0-9]* --exclude v[0-9]r* --exclude v[0-9][0-9]r*"

and, assuming your other metadata is in a ``setup.cfg``, create a ``setup.py`` file containing:

.. code-block:: python

  from dirac_webapp_packaging import gen_extjs_cmdclass, find_data_files
  from setuptools import setup

  setup(
      cmdclass=gen_extjs_cmdclass(),
      # Replace PKG_NAME as appropriate
      data_files=find_data_files(
          source_dir="src/PKG_NAME/WebApp/static/extjs",
          dest_dir="share/dirac/PKG_NAME/static/extjs",
      )
  )

If you are building an extension to any of the pages in WebAppDIRAC ``pyproject.toml`` file the ``requires`` section under ``build-system`` must be modified slightly:

.. code-block:: toml

  [build-system]
  # NOTE: Make sure to keep the runtime requirement in setup.cfg in sync with this version
  requires = ["dirac_webapp_packaging~=1.0", "WebAppDIRAC ~=4.3.0a0", "setuptools_scm[toml]>=3.4"]

Additionally the ``dirac`` ``extension_metadata`` entrypoint should be modified to declare the static resources:

.. code-block:: python

  def extension_metadata():
      return {
          "priority": NNN,
          "web_resources": {
              "static": [Path(sys.prefix) / "share" / "dirac" / PKG_NAME / "static"],
          }
      }

Changelog
~~~~~~~~~

1.0.0
^^^^^

* Initial release
