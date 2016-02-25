import json

class MessageParser():
    def __init__(self):

        self.possible_responses = {
            'error': self.parse_error,
            'info': self.parse_info,
            'message': self.parse_message,
            'history': self.parse_history	
        }

    def parse(self, payload):
        payload = json.loads(payload)

        if payload['response'] in self.possible_responses:
            return self.possible_responses[payload['response']](payload)
        else:
            print 'ERROR in parse(): response "', payload['response'], '" not supported.'

    def parse_error(self, payload):
        print 'ERROR:', payload['content']
    
    def parse_info(self, payload):
        print payload['timestamp'], 'SERVER:', payload['content']

    def parse_message(self, payload):
        print payload['timestamp'], payload['sender'], 'sendt:'
        print '   ', payload['content']

    def parse_history(self, payload):
        print payload['timestamp'], 'CHAT HISTORY:'
        print payload['content']
    
    # Include more methods for handling the different responses... 
