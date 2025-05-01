# SMTP server that recieves emails, pareses, then relays to backend

import asyncio
import email
import json
import requests
import os
from email.policy import default
from dotenv import load_dotenv
from aiosmtpd.controller import Controller

load_dotenv()

# API endpoint for the FastAPI backend
# Create your own .env file and add your open api endpoint url, name it `API_Endpoint`. ie. http://localhost:8000/receive-email/
API_ENDPOINT = os.getenv("API_Endpoint")

class CustomHandler:

    async def handle_DATA(self, server, session, envelope):

        # Parse the email
        msg = email.message_from_bytes(envelope.content, policy=default)

        mailfrom = envelope.mail_from
        rcpttos = envelope.rcpt_tos

        email_data = {
            "sender": mailfrom,
            "recipients": rcpttos,
            "subject": msg.get("subject", ""),
            "date": msg.get("date", ""),
            "cc": msg.get("cc", ""),
            "bcc": msg.get("bcc", ""),
            "headers": dict(msg.items()),
            "body": None,
        }

        # Handle body
        if msg.is_multipart():
            body_parts = []
            for part in msg.iter_parts():
                if part.get_content_type() == "text/plain":
                    body_parts.append(part.get_content().strip())
            email_data["body"] = "\n".join(body_parts)
        else:
            email_data["body"] = msg.get_content().strip()

        json_data = json.dumps(email_data, indent=4)
        print("Formatted JSON Data:\n", json_data)

        # Send to API
        try:
            response = requests.post(
                API_ENDPOINT, 
                json=email_data, 
                headers={"Content-Type": "application/json"}
            )
            if response.status_code in [200, 201]:
                print(f"Successfully sent to API: {API_ENDPOINT}")
            else:
                print(f"Failed to send. HTTP {response.status_code}, Response: {response.text}")
        except Exception as e:
            print(f"Error sending to API: {e}")

        # Return standard SMTP "OK" response
        return '250 Message accepted for delivery'

async def main():
    """
    Sets up and starts the aiosmtpd server on localhost:1025.
    The server runs until interrupted (Ctrl+C).
    """
    controller = Controller(CustomHandler(), hostname='localhost', port=1025)
    controller.start()
    print(f"aiosmtpd Server started on localhost:1025...\nSending parsed emails to: {API_ENDPOINT}")

    try:
        await asyncio.Event().wait()
    except KeyboardInterrupt:
        pass
    finally:
        controller.stop()

if __name__ == '__main__':
    asyncio.run(main())
