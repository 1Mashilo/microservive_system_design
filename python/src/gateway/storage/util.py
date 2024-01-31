import pika
import json

def upload(f, fs, channel, access):
    try:
        # Store the file in the MongoDB GridFS
        fid = fs.put(f)
    except Exception as err:
        # Handle internal server error if file storage fails
        return "Internal server error", 500

    # Create a message to be sent to RabbitMQ
    message = {
        "video_fid": str(fid),
        "mp3_fid": None,
        "username": access.get("username"),
    }

    try:
        # Publish the message to the 'video' queue in RabbitMQ
        channel.basic_publish(
            exchange="",
            routing_key="video",
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ),
        )
    except:
        # Delete the file from MongoDB GridFS if publishing to RabbitMQ fails
        fs.delete(fid)
        return "Internal server error", 500

    # Return success message if upload and message publishing are successful
    return "Upload successful", 200
