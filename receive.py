import os
import base64
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from encrypt import decrypt_msg
import tkinter as tk
from tkinter import messagebox, scrolledtext

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

def get_emails_and_display():
    creds = authenticate()
    service = build("gmail", "v1", credentials=creds)

    results = service.users().messages().list(userId="me", q=f"from:{EMAIL_ACCOUNT}").execute()
    messages = results.get("messages", [])

    if not messages:
        messagebox.showinfo("Info", "No messages found.")
        return

    for msg in messages[:1]:  # Get only the latest email
        msg_id = msg["id"]
        msg_data = service.users().messages().get(userId="me", id=msg_id).execute()

        subject = ""
        for part in msg_data["payload"]["headers"]:
            if part["name"] == "Subject":
                subject = part["value"]

        # Read encrypted body
        payload = msg_data["payload"]["body"]["data"]
        decoded_msg = base64.urlsafe_b64decode(payload).decode()

        try:
            decrypted_msg = decrypt_msg(decoded_msg)
        except Exception as e:
            decrypted_msg = f"Error during decryption: {e}"

        # Display in UI
        display_ui(subject, decoded_msg, decrypted_msg)

def display_ui(subject, encrypted_msg, decrypted_msg):
    window = tk.Tk()
    window.title("Email Decryption Viewer")
    window.geometry("500x600")

    tk.Label(window, text="Latest Email Retrieved", font=("Arial", 14, "bold")).pack(pady=10)

    tk.Label(window, text=f"Subject: {subject}", font=("Arial", 12)).pack(pady=5)

    tk.Label(window, text="Encrypted Message:", font=("Arial", 11, "bold")).pack(pady=5)
    enc_text = scrolledtext.ScrolledText(window, height=6, width=60, wrap=tk.WORD)
    enc_text.insert(tk.END, encrypted_msg)
    enc_text.config(state="disabled")
    enc_text.pack(pady=5)

    tk.Label(window, text="Decrypted Message:", font=("Arial", 11, "bold")).pack(pady=5)
    dec_text = scrolledtext.ScrolledText(window, height=6, width=60, wrap=tk.WORD)
    dec_text.insert(tk.END, decrypted_msg)
    dec_text.config(state="disabled")
    dec_text.pack(pady=5)

    tk.Button(window, text="Close", command=window.destroy, bg="red", fg="white").pack(pady=20)

    window.mainloop()

# Run
if __name__ == "__main__":
    get_emails_and_display()
