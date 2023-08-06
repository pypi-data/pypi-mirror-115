Installation
============

Brutal Maze should run on Python version 3.6 and above.
If you're using an Unix-like operating system, you're likely
to have Python installed on your computer.  Otherwise, you can
download it from python.org_.

The game also uses multiple third-party libraries, which is recommended to
be installed using ``pip``.  There is a detailed documentation about getting
this package manager on pypa.io_.

Install from PyPI
-----------------

For convenience reasons, every release of Brutal Maze is uploaded to the Python
Package Index.  To either install or upgrade, open your terminal (on Windows:
Command Prompt or PowerShell) and run::

   pip install --user --upgrade brutalmaze

This requires the `the user scheme`_ scripts directory to be
in your environmental variable ``$PATH``.

Install from Source
-------------------

If you want to tweak the game or contribute, clone the git repository::

   git clone https://git.sr.ht/~cnx/brutalmaze

Then install it using ``pip``, like so::

   pip install --user brutalmaze/

.. _python.org: https://www.python.org/downloads/
.. _pypa.io: https://pip.pypa.io/en/latest/installing/
.. _the user scheme: https://docs.python.org/3/install/index.html#alternate-installation-the-user-scheme
