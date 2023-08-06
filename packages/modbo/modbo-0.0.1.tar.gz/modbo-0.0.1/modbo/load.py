from .modules_loading import _ModulesLoader

def manager(module_name):
    return _ModulesLoader.get_instance().load_manager(module_name)

def get_module_content_folder(module_name):
    return _ModulesLoader.get_instance().get_module_content_folder(module_name)

def get_module_id(module_name):
    return _ModulesLoader.get_instance().get_module_id(module_name)
