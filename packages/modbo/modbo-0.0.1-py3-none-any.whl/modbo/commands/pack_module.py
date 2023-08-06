"""Modbo pack module utility

Usage:
    modbo pack_module (<name>) [<destination-folder>]
"""
import shutil, argparse

from docopt import docopt

def exec():
    arguments = docopt(__doc__, version='0.1')

    name = arguments["<name>"]
    dest = arguments["<destination-folder>"]

    if not dest:
        dest = f"modbo-{name}"

    source_folder = f"modules/{name}"
    content_folder = f"content/{name}"

    print(f"Packing module '{name}' in folder {dest}...")

    # Copy source
    print("Copying source...")
    shutil.copytree(source_folder, f"{dest}/src")

    # Copy content
    print("Copying content...")

    try:
        shutil.copytree(content_folder, f"{dest}/dist_content")
    except FileNotFoundError:
        print("Couldn't copy content files, folder not found")