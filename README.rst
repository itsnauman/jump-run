.. image:: https://pypip.in/download/jumprun/badge.png
    :target: https://pypi.python.org/pypi//jumprun/
    :alt: Downloads
jumprun
=======
    
A unix command-line tool for running scripts from any directory in
terminal, I actually developed this tool for myself as I hate to cd into
successive directories to run python scripts - jumprun allows me to do
it from any directory buy making shortcuts. Currently only python and
ruby interpreter are supported but you can add support for others like
Perl or PHP. I hope you guys find this useful :D

Platform:
~~~~~~~~~

This tool is made for unix based OS’s because I hate windows :3

Installation:
~~~~~~~~~~~~~

jumprun can be installed using PyPi, ``pip install jumprun``

Dependencies:
~~~~~~~~~~~~~

This tool makes use of docopt - for command line parsing, termcolor -
for colorful outputs and sqlite3 - for db.

Usage:
~~~~~~

cd to the directory where the python script is present, then run
``jr add SHORTCUT-NAME python-scripts-name.py --python or --ruby``. This
makes an entry in the db - the db is created in documents under the name
``.jumprun``. Now you can simply run the script from any dir by
``jr SHORTCUT-NAME`` to execute the script. You can refresh the db by
running ``jr rm --all`` or delete one specific name by
``jr rm SHORTCUT-NAME``. You can also rename an existing shortcut by
running ``jr rename OLD-NAME NEW-NAME``. You can also get the list of all shortcuts with ``jr show`` or ``jr show --f`` to show the file name as well. Run ``jr --help`` for more :)

.. code:: python

  Usage:
  jr add <name> <filename> (--python | --ruby)
  jr rm [<name>] [--all]
  jr show [--f]
  jr rename <oldname> <newname>
  jr <name>
  jr -h | --help
  jr --version

  Arguments:
    name        The name of the command
    filename    The name of the file you want to execute
    oldname     The name of the old shortcut
    newname     The name of the new shortcut

  Commands:
    add         Add a new shortcut
    rm          Delete shortcuts from the database
    rename      Rename the shortcut already created
    show        Display the names of all shorcuts added

  Options:
  -h --help     Show this screen.
  --version     Show version.
  --all         Delete all shortcuts from the database
  --python      Specifies a Python interpreter
  --ruby        Specifies a ruby interpreter
  --f           Fetch all names along with file names
License:
~~~~~~~~

MIT, see LICENSE for more details.
