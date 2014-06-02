jumprun
=======
A command-line tool for running python scripts from any directory in terminal, I actually developed this tool for myself as I hate to cd into successive directories to run python scripts - jumprun allows me to do it from any directory. I hope you guys find this usefull :D

###Installation:
jumprun can be installed using PyPi, ```pip install jumprun```

###Usage:
cd to the directory where the python script is present, then run ```jr add NAME python-scripts-name.py --python```. This makes an entry in the db - the db is created in documents under the name `.jumprun`. Now you can simply run the script from any dir by ```jr NAME```. You can refresh the db by running `jr rm --all` or delete one specific name by `jr rm NAME`. You can add ruby scripts by ```jr add NAME ruby-script-name.rb --ruby``` :)

###License:
MIT, see LICENSE for more details
