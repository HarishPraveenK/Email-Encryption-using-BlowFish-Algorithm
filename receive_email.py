import os
import base64
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from encrypt import decrypt_msg
import email

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
EMAIL_ACCOUNT = "amcfoss@gmail.com"

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

def get_emails():
    creds = authenticate()
    service = build("gmail", "v1", credentials=creds)

    results = service.users().messages().list(userId="me", q=f"from:{EMAIL_ACCOUNT}").execute()
    messages = results.get("messages", [])

    if not messages:
        print("No messages found.")
        return

    for msg in messages[:1]:  # Get the latest email only
        msg_id = msg["id"]
        msg_data = service.users().messages().get(userId="me", id=msg_id).execute()

        for part in msg_data["payload"]["headers"]:
            if part["name"] == "Subject":
                print("\nSubject:", part["value"])

        payload = msg_data["payload"]["body"]["data"]
        decoded_msg = base64.urlsafe_b64decode(payload).decode()

        print("\nEncrypted Message:")
        print(decoded_msg)

        print("\nDecrypting ...")
        print("Decrypted Message:", u'\u2713')
        print(decrypt_msg(decoded_msg))

get_emails()
