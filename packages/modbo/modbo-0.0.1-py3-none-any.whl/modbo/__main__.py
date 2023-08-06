"""Modbo

Usage: 
    modbo (<command>) [<parameters>...] [options]

Options:
    --source-only                       Act on source files only (maintain content folder of a given module)
    --repo <repo-path>                  Choose a git repository as a source
    --folder <folder-path>              Choose a folder as a source
    --subfolder <subfolder-path>        Act on a specific subfolder of the chosen source
"""
import importlib

from docopt import docopt

if __name__ == '__main__':
    arguments = docopt(__doc__, version='0.1')

    command = arguments["<command>"]

    importlib.import_module(f"modbo.commands.{command}").exec()
