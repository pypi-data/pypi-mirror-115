import redis, json
from config import *
def process_message(message):
    print(message.decode('utf-8'))
def publish(host, port, password, channel):
    try:
        publisher = redis.Redis(
        host= host,
        port= port,
        password=password)
        publisher.publish(channel, json.dumps(message))
        
        subscriber_count = publisher.execute_command('PUBSUB', 'NUMSUB', channel)[1]
        if subscriber_count == 0:
            print("Not have subscribers, adding to unhandled queue...")
            queue_length = publisher.execute_command('rpush', queue_name, json.dumps(message))
            print("Queue length: {}".format(queue_length))
    finally:
        del publisher
def recieve(host, port, password, channel, message_callback):
    try:
        rec = redis.Redis(
            host = host,
            port = port,
            password = password
        )
        messages_to_handle = rec.lrange(queue_name,0, -1)
        for message in messages_to_handle:
            message_callback(message)
            rec.blpop(queue_name, 0)
        pubsub = rec.pubsub()
        pubsub.subscribe([channel])
        for message in pubsub.listen():
            if(type(message['data']) is not int):
                print(message['data'].decode('utf-8'))      
    finally:
        del rec