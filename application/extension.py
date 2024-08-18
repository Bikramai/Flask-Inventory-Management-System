import os
from datetime import datetime

from flask import current_app
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()


def log_message(username, message):
    # Define the path to the log file
    log_folder = os.path.join(current_app.root_path, 'static', 'logs')
    log_file = os.path.join(log_folder, f'{username}.log')

    print(log_file)

    # Ensure the log folder exists
    os.makedirs(log_folder, exist_ok=True)

    # Get the current date and time
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Open the log file in write mode and write the message with the timestamp
    with open(log_file, 'a') as f:
        f.write(f"{timestamp} - {message}\n")
