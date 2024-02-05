import json
import os
import yagmail
from email.message import EmailMessage

def notification(message):
    """
    Sends an email notification using Yagmail.

    Args:
        message (str): JSON-formatted string containing message details.

    Returns:
        None
    """
    try:
        # Load JSON message
        message = json.loads(message)

        # Extract message details
        mp3_fid = message["mp3_fid"]
        sender_address = os.environ.get("GMAIL_ADDRESS")
        sender_password = os.environ.get("GMAIL_PASSWORD")
        receiver_address = message["username"]

        # Email content
        subject = "MP3 Download"
        content = f"mp3 file_id: {mp3_fid} is now ready!"

        # Send email using Yagmail
        yag = yagmail.SMTP(sender_address, sender_password)
        yag.send(to=receiver_address, subject=subject, contents=[content])

        print("Mail Sent")

    except Exception as err:
        print(err)
        return err