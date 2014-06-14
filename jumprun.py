"""Jumprun, your command line companion

Usage:
  jr add <name> <filename> (--python | --ruby)
  jr rm [<name>] [--all]
  jr show [--f]
  jr rename <oldname> <newname>
  jr <name>
  jr -h | --help
  jr --version

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
"""

from docopt import docopt
import sqlite3
import subprocess
import os
from termcolor import colored

#Emoji's
S = "\xF0\x9F\x98\x83"
L = "\xF0\x9F\x8D\xAD"
B = "\xF0\x9F\x8D\xBA"


def main():
    """
    This is the main function run by *entry_point* in setup.py
    """
    arg = docopt(__doc__, version=0.6)
    #creates a hidden database in users/documents
    db_path = os.path.expanduser("~/")
    db_path = db_path + "/" + ".jumprun"
    db = sqlite3.connect(db_path)
    #Creates table if doesn't exist on the execution of the script
    cursor = db.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS path(id INTEGER PRIMARY KEY, name TEXT,
    path TEXT, filename TEXT)
        ''')
    db.commit()

#This condition handles the *add* command
    if arg['add']:
        #Get the path of the current dir
        current_dir = os.getcwd()
        name = arg['<name>']
        filename = arg['<filename>']
        cursor.execute('''
        SELECT path,filename FROM path WHERE name=?
            ''', (name,))
        pth = cursor.fetchone()
        #Checks for conflicts in the database
        if pth is None:
            cursor.execute('''
            INSERT INTO path(name, path, filename)
            VALUES (?, ?, ?)
                ''', (str(name), str(current_dir), str(filename)))
            db.commit()
            msg = "%s has been added %s" % (name, L)
            print colored(msg, "blue")
        else:
            print colored("The name %s already exists" % (name), "red")

    if not arg['add'] and not arg['rm'] and not arg['rename'] and not \
    arg['show']:
        get_name = arg['<name>']
        cursor.execute('''
        SELECT path,filename FROM path WHERE name=?
            ''', (get_name,))
        pth = cursor.fetchone()
        #Checks if the user has made an entry using jr add
        if pth is None:
            print colored("Invalid name, type jr --help for more... " + "B",
                          "red")
        else:
            file_path = str(pth[0])
            file_name = str(pth[1])
            #Handles the execution of python/ruby scripts in the terminal
            if arg['--python']:
                cmd = "python %s" % (file_name)
                os.chdir(file_path)
                print colored("Running Script.......", "yellow")
                subprocess.call(cmd, shell=True)
            else:
                cmd = "ruby %s" % (file_name)
                os.chdir(file_path)
                print colored("Running Script.......", "yellow")
                subprocess.call(cmd, shell=True)

#This condition handles the *rm* command
    if arg['rm']:
        #Code for refreshing the entire database
        if arg['--all']:
            os.remove(db_path)
            print colored("The database has been refreshed :) %s" % S, "red")
        else:
            #Code for deleteing a specific name from database
            name = arg['<name>']
            cursor.execute('''
            SELECT path,filename FROM path WHERE name=?
            ''', (name,))
            pth = cursor.fetchone()
            #Checks if the shortcut to be deleted exists?
            if pth is None:
                print colored("%s doesn't exist" % (name), "red")
            else:
                cursor.execute('''
                    DELETE FROM path WHERE name=?
                    ''', (name,))
                db.commit()
                print colored("%s has been deleted %s" % (name, L), "red")

#This condition handles the *rename* command
    if arg['rename']:
        old_name = arg['<oldname>']
        new_name = arg['<newname>']
        cursor.execute('''
        SELECT name, path, filename FROM path WHERE name=?
            ''', (old_name,))
        pth = cursor.fetchone()
        #Checks if the shortcut to be renamed exists?
        if pth is None:
            print colored("%s doesn't exist" % (old_name), "red")
        else:
            cursor.execute('''
            SELECT path,filename FROM path WHERE name=?
            ''', (new_name,))
            q = cursor.fetchone()
            #Checks if the new shortcut name is already present
            if q is not None:
                print colored("The name %s already exists", "red")
            else:
                old_path = pth[1]
                old_filename = pth[2]
                cursor.execute('''
                DELETE FROM path WHERE name=?
                    ''', (old_name,))
                cursor.execute('''
                INSERT INTO path(name, path, filename)
                VALUES (?, ?, ?)
                ''', (str(new_name), str(old_path), str(old_filename)))
                db.commit()
                msg = "%s has been renamed to %s %s" % (old_name, new_name, L)
                print colored(msg, "blue")

#This condition handles the *show* command
    if arg['show']:
        if arg['--f']:
            cursor.execute('''
            SELECT name, filename FROM path
                ''')
            all_records = cursor.fetchall()
            if all_records is None:
                print colored("No shortcuts present", "red")
            else:
                for each_name in all_records:
                    print colored(each_name[0] + " --> " + each_name[1], "red")
        else:
            cursor.execute('''
            SELECT name FROM path
                ''')
            all_names = cursor.fetchall()
            if all_names is None:
                print colored("No shorcuts present", "red")
            else:
                for each_name in all_names:
                    print colored(each_name[0], "yellow")
