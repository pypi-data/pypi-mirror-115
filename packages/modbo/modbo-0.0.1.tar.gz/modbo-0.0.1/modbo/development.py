from .modules_loading import _ModulesLoader

def dev_mode_on():
    return _ModulesLoader.get_instance().dev_mode_on()

def add_reroute_rule(original_module, replacement_module):
    return _ModulesLoader.get_instance().add_reroute_rule(original_module, replacement_module)

def register_mock_manager(module_name, mock_manager):
    return _ModulesLoader.get_instance().register_mock_manager(module_name, mock_manager)

def block_module(module_name):
    return _ModulesLoader.get_instance().block_module(module_name)