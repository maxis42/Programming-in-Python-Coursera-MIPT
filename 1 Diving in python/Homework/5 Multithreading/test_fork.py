import time
import os

pid = os.fork()

if pid == 0:
    # child process
    while True:
        print(f"child: {os.getpid()}")
        time.sleep(2)
else:
    # parent process
    print(f"parent: {os.getpid()}")

    # wait completion of child process
    os.wait()
