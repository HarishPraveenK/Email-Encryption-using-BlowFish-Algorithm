import os
import base64
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from email.mime.text import MIMEText
from encrypt import encrypt_msg

SCOPES = ["https://www.googleapis.com/auth/gmail.send"]
EMAIL_FROM = "amcfoss@gmail.com"
EMAIL_TO = "harishpraveenk1001@gmail.com"

def authenticate():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return creds

def send_email():
    creds = authenticate()
    service = build("gmail", "v1", credentials=creds)

    message_text = input("Enter message to send: ").strip()
    encrypted_msg = encrypt_msg(message_text)

    msg = MIMEText(encrypted_msg)
    msg["to"] = EMAIL_TO
    msg["from"] = EMAIL_FROM
    msg["subject"] = "Encrypted Message"

    raw_msg = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    message = {"raw": raw_msg}

    service.users().messages().send(userId="me", body=message).execute()
    print("\nMessage sent successfully! ✅")

send_email()
