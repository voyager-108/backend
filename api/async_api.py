from concurrent.futures import ProcessPoolExecutor
from multiprocessing import cpu_count
import signal
import requests

pool = ProcessPoolExecutor(cpu_count())

def get(*args, json=True, **kwargs):
    response = requests.get(*args, **kwargs)
    if json:
        return response.json()
    return response

def post(*args, json=True, **kwargs):
    response = requests.post(*args, **kwargs)
    if json:
        return response.json()
    return response

def async_get(*args, **kwargs):
    return pool.submit(get, *args, **kwargs)

def async_post(*args, **kwargs):
    return pool.submit(post, *args, **kwargs)

def finish():
    pool.shutdown(wait=False)

def signal_handler(sig, frame):
    finish()
    exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)



