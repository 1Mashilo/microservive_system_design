"""
This script connects to RabbitMQ, consumes messages from a queue, 
and sends email notifications based on the message content.
"""

import pika
import sys
import os
import time
from send import send_email  # Assuming 'send_email' is a module defined in 'send.py'

def main():
    # RabbitMQ connection configuration
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="rabbitmq")  # Assuming the RabbitMQ service name is 'rabbitmq'
    )
    channel = connection.channel()

    # Define a callback function to process incoming messages
    def callback(ch, method, properties, body):
        # Process the message and send email notification
        err = send_email.notification(body)  # Assuming 'notification' is a function in 'send_email' module
        if err:
            ch.basic_nack(delivery_tag=method.delivery_tag)  # Message processing failed, negative acknowledgment
        else:
            ch.basic_ack(delivery_tag=method.delivery_tag)  # Message processed successfully, acknowledge and remove from queue

    # Start consuming messages from the queue
    channel.basic_consume(
        queue=os.environ.get("MP3_QUEUE"),  # Get the queue name from environment variable
        on_message_callback=callback
    )

    print("Waiting for messages. To Exit, Press CTRL+C")

    # Begin consuming messages indefinitely
    channel.start_consuming()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted!")
        try:
            sys.exit(0)
        except SystemExit:
            os.exit(0)
