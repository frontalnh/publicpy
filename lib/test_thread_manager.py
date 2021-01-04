from lib.thread_manager import ThreadManager
import time

manager = ThreadManager()


def wait(sec):
    print('Start waiting')
    time.sleep(sec)
    print('Waited for 3 seconds')


manager.start_worker_thread(
    'worker', [(wait, [3]), (wait, [3])], lambda: print('terminated!!!!'))
time.sleep(2)
manager.stop_worker('worker')
manager.threads['worker'].join()
