jumprun - for lazy people
==========================
A unix command-line tool for running scripts from any directory in terminal, I actually developed this tool for myself as I hate to cd into successive directories to run python scripts - jumprun allows me to do it from any directory buy making shortcuts. Currently only python and ruby interpreter are supported but you can add support for others like Perl or PHP. I hope you guys find this useful :D

###Platform:
This tool is made for unix based OS's because I hate windows :3

###Installation:
jumprun can be installed using PyPi, ```pip install jumprun```

###Dependencies:
This tool makes use of docopt - for command line parsing, termcolor - for colorful outputs and sqlite3 - for db.

###Usage:
cd to the directory where the python script is present, then run ```jr add SHORTCUT-NAME python-scripts-name.py --python or --ruby```. This makes an entry in the db - the db is created in documents under the name `.jumprun`. Now you can simply run the script from any dir by ```jr SHORTCUT-NAME``` to execute the script. You can refresh the db by running `jr rm --all` or delete one specific name by `jr rm SHORTCUT-NAME`. You can also rename an existing shortcut by running `jr rename OLD-NAME NEW-NAME`. Run `jr --help` for more :)

###License:
MIT, see LICENSE for more details.
