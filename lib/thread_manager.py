from threading import Thread, Event
from typing import Dict, List, Tuple
from collections.abc import Callable


class ThreadManager():
    def __init__(self):
        self.threads: Dict[str, Thread] = {}
        self.stop_events: Dict[str, Event] = {}

    def start_worker_thread(self, name: str,
                            tasks: List[Tuple[Callable, List]],
                            after_stop_cb: Callable
                            ):
        def stoppable_func(stop_event: Event, tasks: List[Tuple[Callable, List]]):
            ordered_tasks = tasks.copy()
            ordered_tasks.reverse()
            while not stop_event.isSet():
                if len(ordered_tasks) > 0:
                    print('not set')
                    task = ordered_tasks.pop()
                    task[0](*task[1])
            after_stop_cb()

        stop_event = Event()
        self.stop_events[name] = stop_event
        self.threads[name] = Thread(
            target=stoppable_func, daemon=True, args=(stop_event, tasks))
        self.threads[name].start()

    def stop_worker(self, name: str):
        print(f'Stopping Threading {name}')
        self.stop_events[name].set()
