jumprun
=======
.. image:: https://pypip.in/download/jumprun/badge.png
    :target: https://pypi.python.org/pypi//jumprun/
    :alt: Downloads
A unix command-line tool for running scripts from any directory in
terminal, I actually developed this tool for myself as I hate to cd into
successive directories to run scripts - jumprun allows me to do
it from any directory buy making shortcuts. At the current moment Perl5,
Ruby and Python interpreters are supported.

Platform:
~~~~~~~~~
This tool is strictly for UNIX based OS.

Installation:
~~~~~~~~~~~~~
jumprun can be installed using PyPi, ``pip install jumprun``.

Dependencies:
~~~~~~~~~~~~~
This tool makes use of docopt - for command line parsing and termcolor -
for colorful outputs.

Usage:
~~~~~~
* Add a python shortcut with ``jr add NAME file.py``
* Run the script from any dir in terminal using ``jr NAME``.
* Refresh the entire db with ``jr rm --all``
* Delete a specfic shortcut with ``jr rm NAME``
* Rename a shortcut with ``jr rename OLDNAME NEWNAME``
* List all shortcuts with ``jr show``
* ``jr --help`` for more details

Whats new in version 0.8 ?:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
In version 0.8, you don't need to specify the interpreter for running the script, eg previously it was ``jr add NAME file.py --python``. Now you only need to do ``jr add NAME file.py`` and the interpreter will automatically be selected.

TODO:
~~~~~~
Add support for shell scripts 

License:
~~~~~~~~
Jumprun is distributed under MIT license, see LICENSE for more details.
