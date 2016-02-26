# -*- coding: utf-8 -*-
import socket
import json
from MessageReceiver import MessageReceiver
from MessageParser import MessageParser

class Client:
    """
    This is the chat client class
    """

    def __init__(self, host, server_port):
        """
        This method is run when creating a new Client object
        """
        # Set up the socket connection to the server
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # TODO: Finish init process with necessary code
        self.host = host
        self.server_port = server_port
        self.receiver = MessageReceiver(self, self.connection)
        self.run()

    def run(self):
        # Initiate the connection to the server
        self.connection.connect((self.host, self.server_port))
        self.receiver.start()
        while True:
            print 'Waiting for your input'
            rawInput = raw_input()
            if rawInput:
                try: 
                    request, content = rawInput.split()

                except ValueError:
                    request = rawInput
                    content = ''

                payload = {'request': request.lower(), 'content': content}
                self.send_payload(payload)

    def disconnect(self):
        # TODO: Handle disconnection
        self.connection.close()
        print 'Connection ',connection, " closed"
        
    def receive_message(self, message):
        # TODO: Handle incoming message
        pass


    def send_payload(self, data):

        try:
            data = json.dumps({'request': request, 'content': content})
            self.connection.send(data)

        except Exception as e:
            print e
            print "Could not send payload"

            # TODO: Handle sending of a payload
        
    # More methods may be needed!


if __name__ == '__main__':
    """
    This is the main method and is executed when you type "python Client.py"
    in your terminal.

    No alterations are necessary
    """
    client = Client('localhost', 9998)
