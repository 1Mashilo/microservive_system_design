import pika
import sys
import os
from pymongo import MongoClient
from gridfs import GridFS
from convert import to_mp3
from dotenv import load_dotenv

def main():
    # Connect to MongoDB
    client = MongoClient("host.minikube.internal", 27017)
    db_videos = client.videos
    db_mp3s = client.mp3s

    # Set up GridFS for storing files
    fs_videos = GridFS(db_videos)
    fs_mp3s = GridFS(db_mp3s)
   
    #rabbitmq connection config
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="rabbitmq") # our service name is rabbitmq
    )
    channel = connection.channel()


    def callback(ch, method, properties, body):
        # Call function to convert video to mp3
        err = to_mp3.start(body, fs_videos, fs_mp3s, ch)
        if err:
            # If error, reject message and request re-delivery
            ch.basic_nack(delivery_tag=method.delivery_tag)
        else:
            # If successful, acknowledge message
            ch.basic_ack(delivery_tag=method.delivery_tag)

    # Start consuming messages from the video queue
    channel.basic_consume(
        queue=os.environ.get("VIDEO_QUEUE"),
        on_message_callback=callback
    )

    # Print a message indicating that the program has started consuming messages
    print("Waiting for messages. To exit, press CTRL+C")

    # Keep consuming messages until program is terminated
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

if __name__ == "__main__":
    main()

        

