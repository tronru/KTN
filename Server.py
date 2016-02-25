# -*- coding: utf-8 -*-
import SocketServer
import json
from time import*
"""
Variables and functions that must be used by all the ClientHandler objects
must be written here (e.g. a dictionary for connected clients)
"""

connectedClients[]
usernamesTaken[]
log[]


class ClientHandler(SocketServer.BaseRequestHandler):
    """
    This is the ClientHandler class. Everytime a new client connects to the
    server, a new ClientHandler object will be created. This class represents
    only connected clients, and not the server itself. If you want to write
    logic for the server, you must write it outside this class
    """

    def handle(self):
        """
        This method handles the connection between a client and the server.
        """
        self.ip = self.client_address[0]
        self.port = self.client_address[1]
        self.connection = self.request
        self.username = ""

        # Loop that listens for messages from the client
        while True:
            received_string = self.connection.recv(4096)
            
            # TODO: Add handling of received payload from client
            data = json.loads(received_string);
            if data:
                now = gmtime()
                timestamp = str(now[3]) + ':' + str(now[4]) + ':' + str(now[5])
                if data["request"]=="login":
                    username = data["content"]

                    if username in usernamesTaken:                       
                        userNameTaken = {"timestamp": timestamp, "sender": "server",
                         "response": "Error", "content": "Username taken!"}
                        payload_userNameTaken = json.dumps(userNameTaken)
                        self.connection.send(payload_userNameTaken)

                    else:
                        if(not isValidUsername(username)):
                            loginFail = {"timestamp": timestamp, "sender": "server",
                                "response": "Error", "content": "Login failed"}
                            payload_loginFail = json.dumps(loginFail)
                            self.connection.send(payload_loginFail)
                        else:     
                            usernamesTaken.append(username)
                            connectedClients.append(self)
                            self.username = username
                            loginSucc = {"timestamp": timestamp, "sender": "server",
                            "response": "Info", "content": "Login successful"}
                            payload_loginSucc = json.dumps(loginSucc)
                            self.connection.send(payload_loginSucc)
                            #History object
                            loginSucc = {"timestamp": timestamp, "sender": "server",
                            "response": "Info", "content": "Login successful"}
                            payload_loginSucc = json.dumps(loginSucc)
                            self.connection.send(payload_loginSucc)

                elif data["request"] == "help":
                    if self.username in usernamesTaken:
                        help = {"timestamp": timestamp, "sender": "server",
                         "response": "Info", "content": "Useful commands: help, logout, names, msg"}
                        payload_help = json.dumps(help)
                        self.connection.send(payload_help)
                    else:
                        help = {"timestamp": timestamp, "sender": "server",
                         "response": "Info", "content": "Useful commands: help, login"}
                        payload_help = json.dumps(help)
                        self.connection.send(payload_help)

                

                elif data["request"] == "logout":
                    #Continue here!!
                    usernamesTaken.remove(username)
                    connectedClients.remove(self)
                    logoutSucc = {"timestamp": timestamp, "sender": "server",
                         "response": "Info", "content": "Logout successful"}
                    payload_logoutSucc = json.dumps(logoutSucc)
                    self.connection.send(payload_logoutSucc)
def isValidUsername(username):
    testString = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890"
        for letter in username:
            if letter not in testString:
                return False
        return True






class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    """
    This class is present so that each client connected will be ran as a own
    thread. In that way, all clients will be served by the server.

    No alterations are necessary
    """
    allow_reuse_address = True

if __name__ == "__main__":
    """
    This is the main method and is executed when you type "python Server.py"
    in your terminal.

    No alterations are necessary
    """
    HOST, PORT = 'localhost', 9998
    print 'Server running...'

    # Set up and initiate the TCP server
    server = ThreadedTCPServer((HOST, PORT), ClientHandler)
    server.serve_forever()
