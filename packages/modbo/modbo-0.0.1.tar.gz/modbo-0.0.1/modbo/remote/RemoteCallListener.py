import pickle

class RemoteCallListener:
    def __init__(self, connection, address, exposed_modules):
        self.__connection = connection
        self.__address = address
        self.__exposed_modules = exposed_modules

    def poll(self):
        try:
            while True:
                serialized_data = self.__connection.recv(4096)
                call_data = pickle.loads(serialized_data)

                print(call_data)
        except KeyboardInterrupt:
            self.__connection.close()