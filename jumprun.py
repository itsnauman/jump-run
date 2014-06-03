"""Jumprun

Usage:
  jr add <name> <filename> (--python | --ruby)
  jr rm [<name>] [--all]
  jr <name>
  jr -h | --help
  jr --version

Arguments:
    name        The name of the command
    filename    The name of the file you want to execute

Commands:
    add   Add a new command
    rm    Refresh the database

Options:
  -h --help     Show this screen.
  --version     Show version.
"""

from docopt import docopt
import sqlite3
import subprocess
import os
from termcolor import colored


def main():
    """
    This is the main function run by *entry_point* in setup.py
    """
    arg = docopt(__doc__, version=0.4)
    #creates a hidden database in users/documents
    db_path = os.path.expanduser("~/Documents")
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
            msg = "%s has been added" % (name)
            print colored(msg, "blue")
        else:
            print colored("The name %s already exists" % (name), "red")

    if not arg['add'] and not arg['rm']:
        get_name = arg['<name>']
        cursor.execute('''
            SELECT path,filename FROM path WHERE name=?
            ''', (get_name,))
        pth = cursor.fetchone()
        #Checks if the user has made an entry using jr add
        if pth is None:
            print colored("Invalid name, type jr --help for more...", "red")
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

#This condition the execution of *rm* command
    if arg['rm']:
        #Code for refreshing the entire database
        if arg['--all']:
            os.remove(db_path)
            print colored("The database has been refreshed :)", "red")
        else:
            #Code for deleteing a specific name from database
            name = arg['<name>']
            cursor.execute('''
            SELECT path,filename FROM path WHERE name=?
            ''', (name,))
            pth = cursor.fetchone()
            #Checks if the record to be deleted exists?
            if pth is None:
                print colored("%s doesn't exist" % (name), "red")
            else:
                cursor.execute('''
                    DELETE FROM path WHERE name=?
                    ''', (name,))
                db.commit()
                print colored("%s has been deleted" % (name), "red")
