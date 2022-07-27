#!/usr/bin/env python
import pika
import sys
import os
import logging
import json
import pprint
def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    # connection = pika.adapters.SelectConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    
    channel.queue_declare(queue='cpu_info')

    logging.basicConfig(filename="newfile.log",
                format='%(asctime)s %(message)s',
                filemode='w')
    logger = logging.getLogger()

    logger.setLevel(logging.DEBUG)

    def on_receive(ch, method, properties, body):
        pprint.pprint(body.decode('utf-8'))
        logger.debug(body.decode('utf-8'))

    channel.basic_consume(queue='cpu_info', on_message_callback=on_receive, auto_ack=True)

    print('Waiting for cpu information. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
