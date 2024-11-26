
from datetime import datetime

def format_message(sender, message):
    timestamp = datetime.now().strftime("%m-%d %I:%M %p")
    return f"{sender}: {message} [{timestamp}]"
