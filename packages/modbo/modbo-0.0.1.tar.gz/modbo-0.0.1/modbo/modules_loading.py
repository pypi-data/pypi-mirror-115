import importlib, logging, traceback

from .components.production.PathsRetriever import PathsRetriever
from .components.development.DevelopmentPathsRetriever import DevelopmentPathsRetriever

class _ModulesLoader():
    _instance = None

    @staticmethod
    def initialize(dev_mode = False):
        _ModulesLoader._instance = _ModulesLoader(dev_mode)

    @staticmethod
    def get_instance():
        return _ModulesLoader._instance

    def __init__(self, dev_mode):
        self.__managers = {}
        self.__dev_mode = dev_mode

        self.__logger = logging.getLogger("ModulesLoader")

        if self.__dev_mode:
            self.__paths_retriever = DevelopmentPathsRetriever()

            self.__mock_managers = {}
        else:
            self.__paths_retriever = PathsRetriever()
    
    def dev_mode_on(self):
        return self.__dev_mode

    def add_reroute_rule(self, original_module, replacement_module):
        if not self.__dev_mode:
            self.__logger.warning("Can't add reroute rule ({} := {}). Adding reroute rule while not in dev mode is not supported, skipping".format(original_module, replacement_module))
            return

        self.__paths_retriever.add_reroute_rule(original_module, replacement_module)

    def get_module_content_folder(self, module_name):
        return self.__paths_retriever.get_module_content_folder(module_name)

    def get_module_folder(self, module_name):
        return self.__paths_retriever.get_module_folder(module_name)

    def get_module_package(self, module_name):
        return self.__paths_retriever.get_module_package(module_name)

    def get_module_id(self, module_name):
        return id(self.__managers[module_name])

    def initialize_module(self, module_name, dev_module=False):
        if self.is_module_loaded(module_name):
            return

        if dev_module:
            self.__paths_retriever.add_dev_module(module_name)

        initializer = self.__get_module_initializer(module_name)
        if not initializer:
            return

        # Solve dependencies
        dependencies = self.get_module_dependencies(module_name)

        for dependency in dependencies:
            self.initialize_module(dependency)

        self.__managers[module_name] = initializer.initialize_manager()

    def initialize_remote_module(self, module_name, manager):
        self.__managers[module_name] = manager

    def is_module_loaded(self, module_name):
        return module_name in self.__managers.keys()

    def connect_module(self, module_name):
        initializer = self.__get_module_initializer(module_name)
        if not initializer:
            return

        try:
            initializer.connect()
        except AttributeError:
            pass

    def load_manager(self, module_name):
        if self.__dev_mode:
            if module_name in self.__mock_managers.keys():
                return self.__mock_managers[module_name]

        return self.__managers[module_name]

    def get_module_dependencies(self, module_name):
        initializer = self.__get_module_initializer(module_name)
        if not initializer:
            return []

        return initializer.depends_on() 

    def launch_main_module(self, module_name):
        initializer = self.__get_module_initializer(module_name)
        if not initializer:
            return

        initializer.main()

    def register_mock_manager(self, module_name, mock_manager):
        if not self.__dev_mode:
            self.__logger.warning("Can't register mock manager ({} := {}). Using mock managers while not in dev mode is not supported, skipping".format(module_name, mock_manager))
            return

        self.__mock_managers[module_name] = mock_manager

    def __get_module_initializer(self, module_name):
        try:
            return importlib.import_module(self.get_module_package(module_name))
        except Exception as e:
            self.__logger.warning("Couldn't find initializer in module {}".format(module_name))

            traceback.print_exc()