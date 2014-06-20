#!/usr/bin/python3

"""
Jumprun, your command line companion.
Use the commands to manage your shortcuts.

Usage:
    jr add <name> [--dir <dir>] <command>
    jr rm (<name> | all)
    jr show (<name> | all)
    jr rename <old> <new>
    jr <name>
    jr --help
    jr --version

Commands:
    add         Add a new shortcut
    rm          Delete a shortcut
    rename      Rename a shortcut
    show        List all shortcuts

Options:
    -h, --help              Show this screen.
    --version               Show version.
    --dir <dir>, -d <dir>   Specify working directory for the command
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
    print_colored(string, 'red')



def print_msg(string):
    """
    Print info message
    """
    print_colored(string, 'cyan')


class JumpRun:
    """
    JumpRun main class
    """


    def __init__(self):
        """
        Prepare database & init the object
        """

        self.args = docopt(__doc__, version=0.80)

        print("<ARGS>\n" + str(self.args) + "\n</ARGS>")

        #creates a data folder in home dir
        path    = os.path.expanduser('~/.jumprun')
        path    = os.path.abspath(path)

        os.makedirs(path, exist_ok=True)
        self.dir = path

        # connect to db
        self.init_db()



    def run(self):
        """
        Perform the specified action
        """

        if self.args['add']:
            self.action_add()

        elif self.args['rm']:
            self.action_rm()

        elif self.args['show']:
            self.action_show()

        elif self.args['rename']:
            self.action_rename

        else:
            self.action_run_command()



    def data_file(self, name):
        """
        Get path to a file in the data directory
        """
        return os.path.join(self.dir, name)



    def init_db(self):
        """
        Init database and prepare tables
        """

        # database file
        db_path = self.data_file("data.sqlite")

        # comect and create cursor
        self.db     = sqlite3.connect(db_path)
        self.cursor = self.db.cursor()

        # prep tables
        self.db_exec('''
            CREATE TABLE IF NOT EXISTS shortcuts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                path TEXT NOT NULL,
                command TEXT NOT NULL
            )
            ''')



    def db_query(self, query, args=None):
        """
        Execute a query in the DB
        """
        if args is None:
            self.cursor.execute(query)
        else:
            self.cursor.execute(query, args)



    def db_exec(self, query, args=None):
        """
        Execute a query in the DB
        """
        if args is None:
            self.db_query(query)
            self.db.commit();
        else:
            self.db_query(query, args)



    def db_fetch_one(self):
        """
        Fetch a results of last query
        """
        return self.cursor.fetchone()



    def db_fetch_all(self):
        """
        Fetch a results of last query
        """
        return self.cursor.fetchall()



    def db_affected_rows(self):
        """
        Get number of affected rows
        """
        return self.cursor.rowcount



    def shortcut_exists(self, name):
        """
        Check if a shortcut of given name already exists in the DB
        """

        self.db_query('''
            SELECT * FROM path WHERE name=?
            ''', (name,))

        pth = self.db_fetch_one()

        if pth is None or len(pth) == 0:
            return False
        else:
            return True



    def action_add(self):
        """
        Add a new shortcut
        """

        # prepare values for new shortcut
        path    = self.args['--dir'] or os.getcwd()
        name    = self.args['<name>']
        cmd     = self.args['<command>']

        # check for conflicts in DB
        if self.shortcut_exists(name):
            print_err('The shortcut "%s" already exists' % name)
            return

        # if cmd has arguments, extract the command only
        cmd_parts   = [x.strip() for x in cmd.split(' ')]
        cmd_real    = cmd_parts[0]
        cmd_tail    = ' '.join(cmd_parts[1:])

        # if cmd_real starts with ./, remove that
        if cmd_real.startswith('./'):
            cmd_real = cmd_real[2:]


        # path to the file (if it's in the folder)
        localfile = os.path.abspath( os.path.join(path, cmd_real) )

        # check if the file is present at the path given
        if os.path.isfile(localfile):

            # check for exacutable bit
            if os.access(localfile, os.X_OK):
                # file is executable
                cmd = './' + cmd_real + ' ' + cmd_tail

            else:
                # not executable
                # try to find interpreter for the file

                ext = os.path.splitext(cmd_real)[1]

                interpreter = {
                    '.py': 'python',
                    '.rb': 'ruby',
                    '.pl': 'perl',
                    '.sh': 'sh',
                    '.php': 'php',
                    '.jar': 'java -jar',
                }.get(ext, None)

                # check if interpreter was found
                if interpreter is None:

                    msg = ('Could not determine how to run %s:\n'
                           'not executable & unknown extension.') % cmd_real;

                    print_err(msg)

                cmd = interpreter + ' ' + cmd_real + ' ' + cmd_tail
        else:
            # use cmd, as given.
            pass

        # save to DB
        self.db_exec('''
            INSERT INTO shortcuts (name, path, command)
            VALUES (?, ?, ?)
            ''', (str(name), str(path), str(cmd)))

        # show OK message
        msg = ('Shortcut "%s" has been created.\n'
               'dir = %s\n'
               'cmd = %s') % (name, path, cmd)

        print_msg(msg)



    def action_rm(self):
        """
        Delete a shortcut
        """

        if self.args['all']:
            # delete all
            self.db_exec(''' TRUNCATE TABLE shortcuts ''')
            print_msg("All shortcuts deleted.")

        else:
            # delete one
            name = self.args['<name>']

            self.db_exec('''
                DELETE FROM shortcuts WHERE name=?
                ''', (name,))

            if self.db_affected_rows() == 0:
                print_err('Shortcut "%s" does not exist!' % name)
            else:
                print_msg('Shortcut "%s" deleted.' % name)



    def action_rename(self):
        """
        Rename a shortcut
        """
        old = arg['<old>']
        new = arg['<new>']

        self.db_query('''
            SELECT id FROM shortcuts WHERE name=?
            ''', (old,))

        r = self.db_fetch_one()

        if r == None:
            print_err('Shortcut "%s" does not exist!' % old)
            return

        id = r['id']

        self.db_exec('''
            UPDATE shortcuts(name) SET (?) WHERE id=?
            ''', (new, id))

        print_msg('Shortcut "%s" renamed to "%s".' % (old, new))



    def action_show(self):
        """
        Show shortcut meaning
        """

        print('Action SHOW.')



    def action_run_command(self):
        """ Show an alias """
        print('Action DO STUFF.')





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
    jr.run()
