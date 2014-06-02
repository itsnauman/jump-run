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
    This is the main function run by *entry_point*
    """
    arg = docopt(__doc__, version=0.2)
    db_path = os.path.expanduser("~/Documents")
    db_path = db_path + "/" + ".jumprun"
    db = sqlite3.connect(db_path)

    cursor = db.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS path(id INTEGER PRIMARY KEY, name TEXT,
        path TEXT, filename TEXT)
        ''')
    db.commit()

    if arg['add']:
        current_dir = subprocess.check_output('pwd')
        current_dir = current_dir.strip("\n")
        name = arg['<name>']
        filename = arg['<filename>']
        cursor.execute('''
            SELECT path,filename FROM path WHERE name=?
            ''', (name,))
        pth = cursor.fetchone()
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
        if pth is None:
            print colored("Invalid name, type jr --help for help", "red")
        else:
            file_path = str(pth[0])
            file_name = str(pth[1])
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

    if arg['rm']:
        if arg['--all']:
            os.remove(db_path)
            print colored("The database has been refreshed :)", "red")
        else:
            name = arg['<name>']
            cursor.execute('''
                DELETE FROM path WHERE name=?
                ''', (name,))
            db.commit()
            print colored("%s has been deleted" % (name), "red")
