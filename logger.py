import datetime

def log(message):
    timestamp = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    print(f"[{timestamp}] {message}")
