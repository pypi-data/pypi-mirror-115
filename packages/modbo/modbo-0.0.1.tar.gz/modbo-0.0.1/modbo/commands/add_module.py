"""Modbo add module utility

Usage:
    modbo add_module (<package> | --folder <folder> | --repo <repo-path>) [--subfolder <subfolder-path>]
"""
from docopt import docopt

import logging, yaml, shutil

def exec():
    arguments = docopt(__doc__, version='0.1')

    package = arguments["<package>"]
    by_folder = arguments["--folder"]
    by_repo = arguments["--repo"] or package

    if not by_folder and not by_repo:
        print("No source template specified")
        return

    folder = arguments["<folder>"]

    print("Recognizing template...")

    if by_folder:
        source_folder = folder
    elif by_repo:
        from git import Repo

        if package:
            repo = f"git@github.com:modbo-project/{package}"
        else:
            repo = arguments["<repo-path>"]

        Repo.clone_from(repo, "repo_tmp/")
        if arguments["--subfolder"]:
            source_folder = "repo_tmp/{}".format(arguments["<subfolder-path>"])
        else:
            source_folder = "repo_tmp/"

    descriptor = yaml.safe_load(open("{}/descriptor.yaml".format(source_folder), "r"))

    logging.info("Adding module '{}' from template {}...".format(descriptor['module_name'], folder))

    src_destination_folder = "modules/{}".format(descriptor["module_name"])
    content_destination_folder = "content/{}".format(descriptor["module_name"])

    try:
        # Copy source
        logging.info("Copying source...")
        shutil.copytree("{}/src".format(source_folder), src_destination_folder)

        if "source_only" not in descriptor.keys() or not descriptor["source_only"]:
            logging.info("Copying content...")
            shutil.copytree("{}/dist_content".format(source_folder), content_destination_folder)
    except Exception as e:
        print(f"Unable to copy module files: {e}")

    if by_repo:
        shutil.rmtree("repo_tmp/")