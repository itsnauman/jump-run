# Jumprun

[![Build Status](https://travis-ci.org/itsnauman/jumprun.svg?branch=master)](https://travis-ci.org/itsnauman/jumprun)

A command-line utility for creating shortcuts for running scripts.

#### Supported Interpreters:

 - Python
 - Ruby
 - Node.js
 - Perl
 - Shell
 - PHP
 - Java

#### Installation:

It can be installed using PyPi, `$ pip install jumprun`. Jumprun supports only Python 3 at the moment!

#### Example
Say I have a python file `test_hello.py` in the `~/Developer` directory and I want to make a shortcut for
running this script.

 - Run `jr add testhello test_hello.py` in `~/Developer` to make a shortcut.
 - Now you can run `jr testhello` from anywhere in terminal to execute the script.
 - You can get further details about a command using `jr show testhello`.
 - You can erase all shortcuts using `jr rm all`

#### Usage:
```
Usage:
    jr add <name> <command> [-d WORKDIR] [-f]
    jr rm all
    jr rm <name>
    jr show
    jr show all
    jr show <name>
    jr rename <old> <new>
    jr <name>
    jr -h
    jr -v

Commands:
    add         Add a new shortcut
    rm          Delete a shortcut
    rename      Rename a shortcut
    show        List all shortcuts

Options:
    -h, --help                  Show this screen.
    --version                   Show version.
    --workdir <dir>, -d <dir>   Working directory for the command
    --force, -f                 Overwrite existing shortcut
```

#### Tests:
`$ python test_jumprun.py`

#### License:
`Jumprun` is distributed under MIT license, see `LICENSE` for more details.
