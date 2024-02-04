import pika
import json
import os
import tempfile
from bson.objectid import ObjectId
import moviepy.editor

def start(message, fs_videos, fs_mp3s, channel):
    # Parse the incoming message as JSON
    message = json.loads(message)

    # Create a temporary file to store the video
    tf = tempfile.NamedTemporaryFile()

    # Retrieve the video file from GridFS and write it to the temporary file
    video_file = fs_videos.get(ObjectId(message["video_fid"]))
    tf.write(video_file.read())

    # Close the temporary file and create a named temporary file to store the MP3 audio
    tf.close()
    tf_path = tempfile.gettempdir() + f"/{message['video_fil']}.mp3"

    # Extract audio from the video using moviepy
    audio = moviepy.editor.VideoFileClip(tf.name).audio

    # Write the extracted audio to the temporary MP3 file
    audio.write_audiofile(tf_path)

    # Read the content of the temporary MP3 file
    with open(tf_path, "rb") as f:
        data = f.read()

    # Store the MP3 audio file in GridFS and obtain its ObjectId
    fid = fs_mp3s.put(data)

    # Remove the temporary MP3 file
    os.remove(tf_path)

    # Add the ObjectId of the MP3 audio file to the message
    message["mp3_fid"] = str(fid)

    try:
        # Publish the message with the MP3 audio ObjectId to the MP3 queue
        channel.basic_publish(
            exchange="",
            routing_key=os.environ.get("MP3_QUEUE"),
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ),
        )
    except Exception as err:
        # If an error occurs during publishing, delete the MP3 audio file from GridFS
        fs_mp3s.delete(fid)
        return "failed to publish"
