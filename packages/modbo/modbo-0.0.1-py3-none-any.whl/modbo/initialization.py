from .modules_loading import _ModulesLoader

def initialize_module(module_name, dev_module=False):
    _ModulesLoader.get_instance().initialize_module(module_name, dev_module)

def connect_module(module_name):
    _ModulesLoader.get_instance().connect_module(module_name)

def launch_main_module(module_name):
    _ModulesLoader.get_instance().launch_main_module(module_name)