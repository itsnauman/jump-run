jumprun
=======
A command-line tool for running python scripts from any directory in terminal.
<a href="http://imgur.com/6D03m56"><img src="http://i.imgur.com/6D03m56.png" title="Hosted by imgur.com" /></a>

###Installation:
jumprun can be installed using PyPi, ```pip install jumprun```

###Usage:
cd to the directory where the python script is present, then run ```jr add NAME python-scripts-name.py --python```. This makes an entry in the db - the db is created in documents under the name `.jumprun`. Now you can simply run the script from any dir by ```jr NAME```. You can refresh the db by running `jr rm --all` or delete one specific name by `jr rm NAME`. You can add ruby scripts by ```jr add NAME ruby-script-name.rb --ruby``` :)

###License:
MIT, see LICENSE for more details
