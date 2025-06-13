# Email-Encryption-using-BlowFish-Algorithm
A terminal-based email decryption tool using the Blowfish encryption algorithm. This Python project retrieves encrypted Gmail messages from a specific sender and decrypts them using Blowfish, displaying the results directly in the terminal.

# Blowfish Email Decryption (Terminal-Based) 🔐📧

This is a simple and secure terminal-based email decryption project using the **Blowfish encryption algorithm** with the **Gmail API**. It reads encrypted email content from a trusted sender's Gmail account, decrypts the message using a predefined secret key, and prints the result in the terminal.

---

## 🚀 Features

- 🔐 Blowfish encryption and decryption (ECB mode)
- 📬 Gmail API integration with OAuth2
- 📥 Fetches latest encrypted email from a specific sender
- 🧾 Base64-encoded message handling
- 🖥️ Fully terminal-based interface

---

## 📁 Project Structure

.
├── encrypt.py # Encryption and decryption functions using Blowfish
├── receive.py # Reads emails from Gmail and decrypts the message
├── credentials.json # Google API credentials for OAuth
└── token.json # Auto-generated token after first-time OAuth

Create a project on Google Cloud Console:

Enable the Gmail API

Download the credentials.json file
