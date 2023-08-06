import logging, os

import queue

from modbo.modules_loading import _ModulesLoader

from modbo.development import dev_mode_on
from modbo.initialization import initialize_module, connect_module, launch_main_module

LOGGER = logging.getLogger(__name__)

def initialize_all_modules(ignored_modules=[]):
    # Initialize modules
    LOGGER.info("Dynamically loading all modules...")

    # Loading dev modules (if needed)
    if dev_mode_on():
        LOGGER.info("Dynamically loading development modules...")

        dev_modules = os.listdir("dev_modules") 
        for dev_module_name in dev_modules:
            if dev_module_name in ignored_modules:
                continue

            LOGGER.info("Dynamically loading development module {}...".format(dev_module_name))

            initialize_module(dev_module_name, dev_module = True)

    modules = os.listdir("modules")

    for module_name in modules: 
        if module_name in ignored_modules:
            continue

        LOGGER.info("Dynamically loading module {}...".format(module_name))

        initialize_module(module_name)

def connect_all_modules(ignored_modules=[]):
    # Connect modules
    LOGGER.info("Connecting modules...")

    modules = os.listdir("modules")

    for module_name in modules: 
        if module_name in ignored_modules:
            continue

        LOGGER.info("Dynamically connecting module {}...".format(module_name))

        connect_module(module_name)

def boot(dev_mode=False):
    _ModulesLoader.initialize(dev_mode)

def initialize(modules_blocklist=[]):
    initialize_all_modules(modules_blocklist)

def launch(main_module, modules_blocklist=[]):
    connect_all_modules(modules_blocklist)

    launch_main_module(main_module)