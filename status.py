from threading import Lock

_lock = Lock()
status = "idle"

def get_status():
    with _lock:
        return status

def set_status(new_status):
    global status
    with _lock:
        status = new_status
