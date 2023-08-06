"""Modbo remove module utility

Usage:
    modbo remove_module [--source-only] (<name>)
"""
import shutil

from docopt import docopt

def exec():
    arguments = docopt(__doc__, version='0.1')

    name = arguments["<name>"]
    source_only = arguments["--source-only"]

    print(f"Removing module '{name}'...")

    # Remove source
    print("Removing source...")

    try:
        shutil.rmtree(f"modules/{name}")
    except FileNotFoundError:
        print("Couldn't remove source files, folder not found")

    # Remove content
    if not source_only:
        print("Removing content...")

        try:
            shutil.rmtree(f"content/{name}")
        except FileNotFoundError:
            print("Couldn't remove content files, folder not found")