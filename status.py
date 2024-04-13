from threading import Lock

_lock = Lock()
status = "idle"
ip = ""

def get_status():
    with _lock:
        return status

def set_status(new_status):
    global status
    with _lock:
        status = new_status

def get_ip():
    with _lock:
        return ip

def set_ip(new_ip):
    global ip
    with _lock:
        ip = new_ip
