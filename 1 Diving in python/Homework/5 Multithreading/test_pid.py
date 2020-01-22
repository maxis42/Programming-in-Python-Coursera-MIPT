import time
import os

pid = os.getpid()

while True:
    print(pid, time.time())
    time.sleep(2)
