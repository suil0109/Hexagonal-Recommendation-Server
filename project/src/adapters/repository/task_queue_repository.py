import queue
from src.domain.ports.queue_port import TaskQueuePort

class TaskQueueRepository(TaskQueuePort):
    
    def __init__(self):
        self._queue = queue.Queue()

    def enqueue(self, task):
        self._queue.put(task)

    def dequeue(self):
        return self._queue.get(block=False) if not self._queue.empty() else None

    def is_empty(self):
        return self._queue.empty()

    def task_done(self):
        self._queue.task_done()

