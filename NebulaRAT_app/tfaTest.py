import os
import pyotp
import smtplib
from email.mime.text import MIMEText


#this code needs to be implemented in the app.py file or the file that call this functions in general
#i dont think u need to pass the totp object as a parameter but it's to be tested
#------------------------------------------------
#     # Generate a secret key
#    secret_key = pyotp.random_base32()
#    
#    # Create a TOTP object
#    totp = pyotp.TOTP(secret_key)
#------------------------------------------------


def send_2fa(totp, receiver_email):    
    # Generate the code
    code = totp.now()
    
    # Send the code via email
    sender_email = os.environ.get('google_username')
    subject = '2FA Code'
    message = f'Your 2FA code is: {code}'
    
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email
    
    # Replace the SMTP server details with your own
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = os.environ.get('google_username')
    smtp_password = os.environ.get('google_password')
    print(f"smtp_username: {smtp_username}")
    print(f"smtp_password: {smtp_password}")
    
    # Send the email with the code to the user via Google's SMTP server
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(msg)
    
    return code

def check_2fa(totp):
    # Ask for the code from the user
    user_code = input("Enter the code: ")
    
    # Check if the code is correct
    if totp.verify(user_code, valid_window=1):
        print("Code is correct!")
        return True
    else:
        print("Code is incorrect or too old!")
        return False

def gen_2fa():
     # Generate a secret key
    secret_key = pyotp.random_base32()
    
    # Create a TOTP object
    totp = pyotp.TOTP(secret_key)
    return totp