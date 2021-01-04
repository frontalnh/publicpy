import time
import unittest
from lib.stoppable_thread import StoppableThread


class TestStoppableThread(unittest.TestCase):
    def test_stop(self):
        def sleep_for(sec):
            raise Exception('hello')
            time.sleep(sec)
            print('Ended')

        thread = StoppableThread(target=sleep_for, args=(10,))
        thread.start()
        thread.stop()


if __name__ == '__main__':
    unittest.main()
