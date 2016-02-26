# -*- coding: utf-8 -*-
from threading import Thread
import MessageParser

class MessageReceiver(Thread):
    """
    This is the message receiver class. The clas inherits Thread, something that
    is necessary to make the MessageReceiver start a new thread, and it allows
    the chat client to both send and receive messages at the same time
    """

    def __init__(self, client, connection):
        """
        This method is executed when creating a new MessageReceiver object
        """

        # Flag to run thread as a daemon
        self.daemon = True
        self.connection = connection
        self.client = client

        # TODO: Finish initialization of MessageReceiver

    def run(self):
        # TODO: Make MessageReceiver receive and handle payloads
        pass
