# * greenland -- A Commandline Interface Into the Greenland Eco System         |
# * Copyright (C) 2020  M E Leypold  ------------------------------------------|
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.

# * Command line interface  ---------------------------------------------------|
#
# ** Global Usage  ------------------------------------------------------------|
#
#      See doc strings of sub-command below for usage of specific sub-commands.

"""greenland -- a commandline interface into the greenland eco system

Usage:
  greenland [--version] [--help] [--verbose] <command> [<args>...]

Options:
  -h --help      Show this screen.
  -V --version   Show version.
  -w --warranty  Show warranty.
  -c --verbose   Be verbose.

The most commonly used commands are:
   TBD

See 'greenland help <command>' for more information on a specific command or help topic.
See 'greenland help commands' for a complete list of subcommands.
"""

# TBD: add topical help pages (from various modules)

# ** Global Data and Runtime  -------------------------------------------------|

version    = "greenland 0.0.0"

import sys, os
import textwrap
from abc import abstractmethod
from docopt import docopt

from .. import bin
from .runtime import Panic, info

# ** Sub-Command Registry  ----------------------------------------------------|

class command(object):

    # Static class data is the command registry. Instances represent
    # single commands.

    registry = {}
    command_column_width = 10

    def __init__(self, name, help=None):
        self.name = name
        self.help = help
        if len(name)>self.command_column_width:
            self.__class__.command_column_width = len(name)


    def __call__(self, proc):
        self.proc = proc
        self.registry[self.name] = self
        return proc

    def run(self,gargs,args):
        cmd_args = docopt(textwrap.dedent(self.proc.__doc__), argv=[self.name]+args)
        del cmd_args[self.name]
        self.proc(gargs,cmd_args)

    @classmethod
    def dispatch(cls, name, gargs, args):

        # TBD: Here we could process the global arguments

        if name == "help":
            if len(args) == 0:
                docopt(__doc__, version=version, argv=['--help'])
            else:
                # TBD: here we can process the additional help pages, if any are available
                name = args[0]
                args=["--help"]
                if name == "commands":
                    print()
                    for cmd,obj in sorted(cls.registry.items()):
                        if obj.help == None:
                            print("{CMD:{WIDTH}} - {HELP}".format(
                                CMD   = cmd,
                                HELP  = "[undocumented]",
                                WIDTH = cls.command_column_width))
                        else:
                            print("{CMD:{WIDTH}} - {HELP}".format(
                                CMD   = cmd,
                                HELP  = obj.help,
                                WIDTH = cls.command_column_width))
                    print()
                    exit(0)


        if name not in cls.registry:
            exit("'{NAME}' is not a greenland command or help page. See 'greenland help'.".format(NAME=name))

        cls.registry[name].run(gargs,args)


# ** Sub-Command 'bist'  ------------------------------------------------------|

def discover_test_packages():
    import greenland
    import importlib
    subpackages = set()
    for p in greenland.__path__:
        subpackages.update([d for d in os.listdir(p) if (d[0] not in ('_','.') and d[-3:] != ".py")])
    testpackages = set()
    for name in subpackages:
        try:
            fullname = F"greenland.{name}.tests"
            m = importlib.import_module(fullname)
            testpackages.add(fullname)
        except ModuleNotFoundError:
            pass
    return testpackages

@command("bist", "run built-in self tests")
def bist(gargs,args):
    """
    Sub-command 'greenland bist' -- run built-in self tests.

    Usage:
      greenland bist [<test> ...]

    If tests are specified runs the specified test(s). If no tests are
    specified runs all currently installed tests.

    Use 'greenland list-bists' to show the available self tests.
    """

    import os, importlib, subprocess
    
    tests   = args['<test>']
    # markers = ["-m", "smoke"] # future exension    
    markers = []             

    if not tests:
        tests = discover_test_packages()

    print(F"=> Tests to be run: {tests}")
    
    for test in tests:
        print(F"\n=> Running: {test}")        
        try:
            i = test.index("greenland.")
        except ValueError:
            i = None
        if i != 0:
            test = "greenland."+test

        m = importlib.import_module(test)
        p = os.path.dirname(m.__file__)
        ini_file = os.path.join(p,"pytest.ini")

        assert os.path.exists(ini_file), "This package is not a package of tests -- pytest.ini is missing."

        subprocess.run(['pytest', *markers,'-c', ini_file], cwd=p, check=True)    

# ** main()  ------------------------------------------------------------------|

def main(name=sys.argv[0], argv=sys.argv[1:]):
    
    gargs    = docopt(__doc__, version=version, options_first=True, argv=argv)
    cmd      = gargs['<command>']
    cmd_args = gargs['<args>']

    del gargs['<command>']
    del gargs['<args>']

    try:
        command.dispatch(cmd,gargs,cmd_args)
    except Panic as p:
        from os import path
        print(path.basename(name)+": *** Error ***", p, file=sys.stderr)


