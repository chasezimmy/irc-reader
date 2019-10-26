import os
import re
import json
import socket
import redis
from irc.message import extract_message


class IRCListener:
    def __init__(self, channel, redis_client):
        self.host = "irc.twitch.tv"
        self.port = int(os.environ['PORT'])
        self.irc_channel = f'#{channel}'
        self.channel = channel
        self.nickname = os.environ['NICKNAME']
        self.oauth = os.environ['OAUTH']
        self.redis_client = redis_client
        self.socket_connection = socket.socket()

        self.run()

    def __connect(self):
        self.socket_connection.connect((self.host, self.port))
        self.socket_connection.send(bytes('PASS %s\r\n' % self.oauth, 'utf-8'))
        self.socket_connection.send(bytes('NICK %s\r\n' % self.nickname, 'utf-8'))
        self.socket_connection.send(bytes('JOIN %s\r\n' % self.irc_channel, 'utf-8'))

    def part_channel(self):
        self.socket_connection.send(bytes('PART %s\r\n' % self.irc_channel, 'utf-8'))

    def run(self):
        self.__connect()
        while self.redis_client.hget('channels', self.channel) == b'1':
            try:
                
                data = self.socket_connection.recv(2056).decode('utf-8', 'replace')
                data_split = re.split(r"[~\r\n]+", data)
                data = data_split.pop()
                
                for line in data_split:
                    line = str.rstrip(line)
                    line = str.split(line)
                    
                    if len(line) > 1:
                        if line[0] == 'PING':
                            self.socket_connection.send(bytes('PONG %s\r\n' % line[1], 'utf-8'))
                        
                        if line[1] == 'PRIVMSG':
                            message = extract_message(line)
                            if message:
                                dump = json.dumps(message)
                                self.redis_client.rpush('5_min', dump)
                                self.redis_client.rpush('30_min', dump)
                                self.redis_client.rpush('1_hour', dump)

            except socket.error:
                print("Socket died")

            except socket.timeout:
                print("Socket timeout")
        
        self.part_channel()
        return
