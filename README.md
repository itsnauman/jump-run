`$ jumprun_`
=============
[![Build Status](https://travis-ci.org/itsnauman/jumprun.svg?branch=master)](https://travis-ci.org/itsnauman/jumprun)

A unix command-line tool for running scripts from any directory in terminal. Jumprun allows you to make shortcuts for scripts.

### Supported Interpreters:

 - Python
 - Ruby
 - Perl
 - Shell
 - PHP
 - Java

### Platform:

This tool is strictly for UNIX based OS's.

### Installation:

It can be installed using PyPi, `$ pip install jumprun`.

### Dependencies:

This tool makes use of `docopt` and `termcolor`

### Usage:
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

### Tests:
For running the unittests, `$ python test_jumprun.py` 

### License:
`Jumprun` is distributed under MIT license, see `LICENSE` for more details.
