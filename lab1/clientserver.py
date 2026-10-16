"""
Client and server using classes
"""

import logging
import socket

import const_cs
from context import lab_logging

# init loging channels for the lab
lab_logging.setup(stream_level=logging.INFO)

# pylint: disable=logging-not-lazy, line-too-long


class Server:
    """ The server """
    _logger = logging.getLogger("vs2lab.lab1.clientserver.Server")
    _serving = True
    _tel = {'jack': 4098, 'sape': 4139, 'guido': 4127, 'john': 4128,
            'mary': 4129, 'anne': 4130}  # telephone numbers

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # prevents errors due to "addresses in use"
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((const_cs.HOST, const_cs.PORT))
        self.sock.settimeout(3)  # time out in order not to block forever
        self._logger.info("Server bound to socket " + str(self.sock))

    def serve(self):
        """ Serve echo """
        self.sock.listen(1)
        # as long as _serving (checked after connections or socket timeouts)
        while self._serving:
            try:
                # pylint: disable=unused-variable
                # returns new socket and address of client
                (connection, address) = self.sock.accept()
                while True:  # forever
                    data = connection.recv(1024)  # receive data from client
                    if not data:
                        break  # stop if client stopped

                    tokens = data.decode('ascii').split(
                        " ")  # decode and split at whitespace
                    if tokens[0] == "GET":
                        name = tokens[1] if len(tokens) > 1 else ""
                        if name in self._tel:
                            data = str(self._tel[name]).encode('ascii')
                        else:
                            data = "Name not found".encode('ascii')
                    elif tokens[0] == "GETALL":
                        data = str(self._tel).encode('ascii')
                    else:
                        data = "Invalid command".encode('ascii')
                    connection.send(data)
                connection.close()  # close the connection
            except socket.timeout:
                pass  # ignore timeouts
        self.sock.close()
        self._logger.info("Server down.")


class Client:
    """ The client """
    logger = logging.getLogger("vs2lab.a1_layers.clientserver.Client")

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((const_cs.HOST, const_cs.PORT))
        self.logger.info("Client connected to socket " + str(self.sock))

    def call(self, msg_in="Hello, world"):
        """ Call server """
        self.sock.send(msg_in.encode('ascii'))  # send encoded string as data
        data = self.sock.recv(1024)  # receive the response
        msg_out = data.decode('ascii')
        print(msg_out)  # print the result
        self.sock.close()  # close the connection
        self.logger.info("Client down.")
        return msg_out

    def get(self, name=""):
        result = self.call("GET " + name)  # call server with GET command
        data = eval(result)  # convert string to dict
        print(f"{name}: {data}")
        return data

    def get_all(self):
        result = self.call("GETALL")  # call server with GETALL command
        data = eval(result)  # convert string to dict
        for name, number in data.items():
            print(f"{name}: {number}")
        return data

    def close(self):
        """ Close socket """
        self.sock.close()
