Installation
============

The project targets Python 3 and is easiest to use from a virtual environment.

Install the package in editable mode from the repository root:

.. code-block:: bash

   python3 -m venv .venv
   source .venv/bin/activate
   python -m pip install --upgrade pip
   python -m pip install -e .

To install the test dependencies as well, use:

.. code-block:: bash

   python -m pip install -e ".[test]"

Documentation
-------------

The HTML documentation depends on the ``docs`` extra:

.. code-block:: bash

   python -m pip install -e ".[docs]"

Build the documentation with notebook execution disabled by default:

.. code-block:: bash

   sphinx-build -b html doc/source build/html

To force execution of the notebooks during a docs build, set:

.. code-block:: bash

   PYOPALTOOLS_NBSPHINX_EXECUTE=auto

Examples
--------

Example notebooks live in `opal/test`, `tests`, and `surrogate`. They can be
smoke-tested from the repository root with:

.. code-block:: bash

   python tests/smoke_notebooks.py
