================
Readme: asmchip8
================

**asmchip8** is an assembler for CHIP-8.  It is free software under the GNU
AGPLv3+ license.

The author and maintainer is Mariano Street <mctpyt@proton.me>.


Dependencies
============

- Runtime dependency: Python 3.10 or later.
- Install dependency: Flit.
- Test dependencies: PyTest, PyEnv, Test.


Development
===========

How to run?
-----------

From the project directory, run::

	$ ./src/asmchip8/main.py <input>

For information on command-line options, see ``asmchip8(1)`` or run with
``-h`` or ``--help``.

How to install?
---------------

Part of the project can be installed via Flit::

	$ flit install

How to run the test suite?
--------------------------

From the project directory, run::

	$ PYTHONPATH=src pytest tests

If you want a more verbose output, add the ``-v`` option.

PyTest is required to be installed.  One way to handle this is via Tox: see
the next section.

How to test different Python versions?
--------------------------------------

Use PyEnv and Tox.

For example, to test 3.11::

	$ pyenv install 3.11-dev
	$ PATH=$PATH:$HOME/.pyenv/versions/3.11-dev/bin tox -e py311

When testing via Tox, it is not necessary to have PyTest installed on the
system.  Tox installs it automatically in an isolated environment.


Additional documentation
========================

Two manpages are provided with the project:

``asmchip8(1)``
	Located at ``doc/asmchip8.1``.  It documents the ``asmchip8`` command.
``asmchip8(5)``
	Located at ``doc/asmchip8.5``.  It documents the assembly language.

They can be read without installing like this, from the project directory::

	$ man -l doc/asmchip8.1
	$ man -l doc/asmchip8.5

In addition, the source code contains some comments and docstrings.
