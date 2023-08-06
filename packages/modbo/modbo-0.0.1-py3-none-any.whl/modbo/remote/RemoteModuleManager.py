import pickle

from ..Manager import Manager

class _RemoteMethodCaller(object):
    def __init__(self, module_name, name, connection):
        self.__module_name = module_name
        self.__name = name
        self.__connection = connection

    def __call__(self, *args, **kwargs):
        print("Remote method call")
        serialized_call = pickle.dumps({
            "module": self.__module_name,
            "method": self.__name,
            "args": args,
            "kwargs": kwargs
        })

        self.__connection.send(serialized_call)

class RemoteModuleManager(Manager):
    def __init__(self, name, connection):
        self.__name = name
        self.__connection = connection

    def __getattr__(self, name):
        return _RemoteMethodCaller(self.__name, name, self.__connection)