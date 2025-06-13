import os
import base64
from tkinter import Tk, Label, Entry, Text, Button, messagebox
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from email.mime.text import MIMEText
from encrypt import encrypt_msg  # Your encryption function

# Constants
SCOPES = ["https://www.googleapis.com/auth/gmail.send"]
EMAIL_FROM = "amcfoss@gmail.com"
EMAIL_TO = "harishpraveenk1001@gmail.com"

# Function to handle Gmail authentication
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

# Function to send the email using Gmail API
def send_email(message_text):
    creds = authenticate()
    service = build("gmail", "v1", credentials=creds)

    encrypted_msg = encrypt_msg(message_text)

    msg = MIMEText(encrypted_msg)
    msg["to"] = EMAIL_TO
    msg["from"] = EMAIL_FROM
    msg["subject"] = "Encrypted Message"

    raw_msg = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    message = {"raw": raw_msg}

    service.users().messages().send(userId="me", body=message).execute()
    messagebox.showinfo("Success", "Encrypted message sent successfully!")

# UI function using tkinter
def open_ui():
    def on_send_click():
        user_msg = msg_input.get("1.0", "end-1c").strip()
        if not user_msg:
            messagebox.showwarning("Empty Message", "Please enter a message to send.")
        else:
            send_email(user_msg)

    window = Tk()
    window.title("Secure Email Sender")
    window.geometry("400x300")

    Label(window, text="Enter your message below:", font=("Arial", 12)).pack(pady=10)

    msg_input = Text(window, height=10, width=45)
    msg_input.pack(padx=10)

    send_btn = Button(window, text="Send Encrypted Email", command=on_send_click, bg="blue", fg="white")
    send_btn.pack(pady=15)

    window.mainloop()

# Run the app
if __name__ == "__main__":
    authenticate()  # Do auth first before opening UI
    open_ui()
