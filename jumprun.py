#!/bin/python3

"""Jumprun, your command line companion

Usage:
  jr add <name> <filename>
  jr rm [<name>] [--all]
  jr show [--f]
  jr rename <oldname> <newname>
  jr <name>
  jr -h | --help
  jr --version

Commands:
    add         Add a new shortcut
    rm          Delete a shortcut
    rename      Rename a shortcut
    show        List all shortcuts

Options:
  -h --help     Show this screen.
  --version     Show version.
  --all         Delete all shortcuts from the database
  --f           Fetch all shortcut names along with file names
"""

import sqlite3
import subprocess
import os
from termcolor import colored
from docopt import docopt


def print_colored(string, color):
    """
    Print text using given color
    """
    print(colored(string, color))



def print_err(string):
    """
    Print error message
    """
    print_colored(string, "red")



def print_msg(string):
    """
    Print info message
    """
    print_colored(string, "cyan")


class JumpRun:
    def __init__(self):

        self.arg = docopt(__doc__, version=0.80)

        #creates a hidden database in users/documents
        db_path = os.path.expanduser("~/")
        db_path = db_path + "/" + ".jumprun"
        self.db = sqlite3.connect(db_path)
        
        #Creates table if doesn't exist on the execution of the script
        self.cursor = self.db.cursor()

        self.create_table()

        print_msg("Hello.")
        

    def create_table():
        """
        Make sure the data table exists
        """

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS path(
                id INTEGER PRIMARY KEY NOT NULL AUTO_INCREMENT,
                name TEXT NOT NULL,
                path TEXT NOT NULL,
                command TEXT NOT NULL
            )
            ''')
        self.db.commit()








def main():
    """
    Main function
    """
    arg = docopt(__doc__, version=0.80)
    #creates a hidden database in users/documents
    db_path = os.path.expanduser("~/.jumprun")
    db = sqlite3.connect(db_path)
    #Creates table if doesn't exist on the execution of the script
    cursor = db.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS path(
            id INTEGER PRIMARY KEY NOT NULL AUTO_INCREMENT,
            name TEXT NOT NULL,
            path TEXT NOT NULL,
            command TEXT NOT NULL
        )
        ''')
    db.commit()

#This condition handles the *add* command
    if arg['add']:
        #Get the path of the current dir
        current_dir = os.getcwd()
        name = arg['<name>']
        filename = arg['<filename>']
        if os.path.isfile(os.getcwd() + "/" + filename):
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
                print_msg(msg)
            else:
                print_err("The name %s already exists" % (name))
        else:
            print_err("The File Doesn't Exist")

    if not arg['add'] and not arg['rm'] and not arg['rename'] and not arg['show']:
        get_name = arg['<name>']
        cursor.execute('''
            SELECT path,filename FROM path WHERE name=?
            ''', (get_name,))
        pth = cursor.fetchone()
        #Checks if the user has made an entry using jr add
        if pth is None:
            print_err("Invalid command, see help for moe info.")
        else:
            file_path = str(pth[0])
            file_name = str(pth[1])
            #Handles the execution of python/ruby scripts in the terminal
            if os.path.splitext(file_name)[1] == ".py":
                cmd = "python %s" % (file_name)
                os.chdir(file_path)
                print_msg("Running Script:")
                subprocess.call(cmd, shell=True)

            elif os.path.splitext(file_name)[1] == ".rb":
                cmd = "ruby %s" % (file_name)
                os.chdir(file_path)
                print_msg("Running Script:")
                subprocess.call(cmd, shell=True)

            elif os.path.splitext(file_name)[1] == ".pl":
                cmd = "perl %s" % (file_name)
                os.chdir(file_path)
                print_msg("Running Script:")
                subprocess.call(cmd, shell=True)

            else:
                ext = os.path.splitext(file_name)[1]
                print_err("The %s extension is not supported" % ext)

#This condition handles the *rm* command
    if arg['rm']:
        #Code for refreshing the entire database
        if arg['--all']:
            os.remove(db_path)
            print_msg("The database has been refreshed.")
        else:
            #Code for deleteing a specific name from database
            name = arg['<name>']
            cursor.execute('''
                SELECT path,filename FROM path WHERE name=?
                ''', (name,))
            pth = cursor.fetchone()
            #Checks if the shortcut to be deleted exists?
            if pth is None:
                print_err("%s doesn't exist" % name)

            else:
                cursor.execute('''
                    DELETE FROM path WHERE name=?
                    ''', (name,))

                db.commit()
                print_msg("%s has been deleted." % name)

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
            print_err("%s doesn't exist" % old_name)
        else:
            cursor.execute('''
                SELECT path,filename FROM path WHERE name=?
                ''', (new_name,))

            q = cursor.fetchone()

            #Checks if the new shortcut name is already present
            if q is not None:
                print_err("The name %s already exists", new_name)

            else:
                old_path = pth[1]
                old_filename = pth[2]

                cursor.execute('''
                    DELETE FROM path WHERE name=?
                    ''', (old_name,))

                cursor.execute('''
                    INSERT INTO path(name, path, filename)
                    VALUES (?, ?, ?)
                    ''', (
                        str(new_name),
                        str(old_path),
                        str(old_filename)
                    ))

                db.commit()
                msg = "%s has been renamed to %s" % (old_name, new_name)
                print_msg(msg)

#This condition handles the *show* command
    if arg['show']:
        if arg['--f']:
            cursor.execute('''
                SELECT name, filename FROM path
                ''')

            all_records = cursor.fetchall()
            if (all_records is None) or (len(all_records) == 0):
                print_err("No shortcuts present")
            else:
                for each_name in all_records:
                    print_msg(each_name[0] + " ---> " + each_name[1])
        else:
            cursor.execute('''
                SELECT name FROM path
                ''')

            all_names = cursor.fetchall()
            if all_names is None:
                print_err("No shorcuts present")
            else:
                for each_name in all_names:
                    print_msg(each_name[0])


# bootstrap
if __name__ == "__main__":
    jr = JumpRun()
