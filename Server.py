# -*- coding: utf-8 -*-
import SocketServer
import json
from time import*
"""
Variables and functions that must be used by all the ClientHandler objects
must be written here (e.g. a dictionary for connected clients)
"""

connectedClients = []
usernamesTaken = []
log = []




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
        self.possible_requests = {
        'names': self.reply_names,
        'help': self.reply_help,
        'msg': self.reply_msg, 
        'login': self.reply_login,
        'logout': self.reply_logout
            }

        self.ip = self.client_address[0]
        self.port = self.client_address[1]
        self.connection = self.request
        self.username = ""



        # Loop that listens for messages from the client
        while True:
            received_string = self.connection.recv(4096)

            # TODO: Add handling of received payload from client
            if received_string:
                self.reply(received_string)
                
               
 
    def reply(self, payload):
            payload = json.loads(payload)

            if payload['request'] in self.possible_requests:
                return self.possible_requests[payload['request']](payload)
            else:
                print 'ERROR in replpy(): response <<', payload['request'], '>> from SERVER not supported.'

    def reply_login(self, payload):
        if self in connectedClients:
            self.send("server", "error", "Invalid command.")

        else:
            username = payload["content"]

            if username in usernamesTaken:
                self.send("server", "error", "Username taken!")                       

            else:
                if(not isValidUsername(username)):
                    self.send("server", "error", "Login failed. Username not valid.")
                else:     
                    usernamesTaken.append(username)
                    connectedClients.append(self)
                    self.username = username
                    self.send("server", "info", "Login successful.")
                    #Send history object
                    #self.send("server", "history", log)

    def reply_logout(self, payload):
        if self in connectedClients:
            usernamesTaken.remove(self.username)
            connectedClients.remove(self)
            self.send("server", "info", "Logout successful.")
        else:
            self.send("server", "error", "Invalid command.")

    def reply_names(self, payload):
        if self in connectedClients:
            self.send("server", "info", usernamesTaken)
        else:
            self.send("server", "error", "Invalid command.")


    def reply_help(self, payload):
        if self in connectedClients:
            self.send("server", "info", "Useful commands: help, logout, names, msg.")
        else:
            self.send("server", "info", "Useful commands: help, login.")
            

    def reply_msg(self, payload):
        if self in connectedClients:
            log.append(received_string)
            broadcast(payload["content"])
        else:
            self.send("server", "error", "Invalid command.")


    def send(self, sender, response, content):
        now = gmtime()
        timestamp = str(now[3]) + ':' + str(now[4]) + ':' + str(now[5])
        command = {"timestamp": timestamp, "sender": sender,
            "response": response, "content": content}
        self.connection.send(json.dumps(command))



def isValidUsername(username):
    testString = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890"
    for letter in username:
        if letter not in testString:
            return False
    return True


def broadcast(msg):
    now = gmtime()
    timestamp = str(now[3]) + ':' + str(now[4]) + ':' + str(now[5])
    message = {"timestamp": timestamp, "sender": "server",
        "response": "message", "content": msg} 
    payload_message = json.dumps(message)
    for client in connectedClients:
        client.connection.send(payload_message)


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
