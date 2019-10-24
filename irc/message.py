import time

def extract_message(raw_message):

    message = {}

    try:
        author = raw_message[0].split(':')[1].split('!')[0]
        channel = raw_message[2][1:]
        spam = ' '.join(raw_message[2:]).split(':')[1]

        message['author'] = author
        message['channel'] = channel
        message['spam'] = spam
        message['time'] = time.time()

        return message
        
    except IndexError as e:
        print(e, raw_message)

    return None
