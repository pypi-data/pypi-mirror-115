import socket 

from .RemoteCallListener import RemoteCallListener
from .RemoteModuleManager import RemoteModuleManager

from modbo.modules_loading import _ModulesLoader

def expose(host, port, exposed_modules):
    accepting_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    accepting_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    accepting_socket.bind((host, port))
    accepting_socket.listen()

    connection, address = accepting_socket.accept()

    listener = RemoteCallListener(connection, address, exposed_modules)
    listener.poll()

def link(host, port, module_name):
    connection_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    connection_socket.connect((host, port))

    _ModulesLoader.get_instance().initialize_remote_module(module_name, RemoteModuleManager(module_name, connection_socket))

    return connection_socket