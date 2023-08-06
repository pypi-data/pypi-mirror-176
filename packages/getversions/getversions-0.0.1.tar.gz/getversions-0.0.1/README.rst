get_versions
============

Get the versions of a package available in the repository via pip, and the installed
version.

Installation
------------

.. code-block:: shell

  pip install getversions

Usage
-----

.. code-block:: shell

  python -m getversions.getversions package_name

For instance,

.. code-block:: shell

  python -m getversions.getversions black

would produce output similar to

.. code-block:: shell

  *22.10.0
  22.8.0
  22.6.0
  22.3.0
  22.1.0

where `black 22.10.0` is installed for the current Python interpreter.
