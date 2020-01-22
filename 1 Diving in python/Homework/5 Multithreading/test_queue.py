from queue import Queue
from threading import Thread


def worker(q, n):
    while True:
        item = q.get()
        if item is None:
            break
        print(f"process data: thread #{n} / data #{item}")


data_q = Queue(maxsize=5)
th1 = Thread(target=worker, args=(data_q, 1))
th2 = Thread(target=worker, args=(data_q, 2))

th1.start()
th2.start()

for i in range(50):
    data_q.put(i)
data_q.put(None)
data_q.put(None)

th1.join()
th2.join()
