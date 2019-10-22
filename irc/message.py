import time

class Message:
    def __init__(self, raw_message):
        self.author = raw_message[0].split(':')[1].split('!')[0]
        self.channel = raw_message[2][1:]
        self.message = ' '.join(raw_message[2:]).split(':')[1]
        self.time = time.time()
