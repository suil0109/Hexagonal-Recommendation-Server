import os, sys
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
sys.path.insert(0, parent_dir)


import unittest
from src.domain.ports.queue_port import TaskQueuePort

class MockTaskQueue(TaskQueuePort):
    def __init__(self):
        self.queue = []
    
    def enqueue(self, task):
        self.queue.append(task)
    
    def dequeue(self):
        if self.is_empty():
            raise IndexError("dequeue from empty queue")
        return self.queue.pop(0)
    
    def is_empty(self):
        return len(self.queue) == 0

class TestTaskQueuePort(unittest.TestCase):

    def test_enqueue_dequeue(self):
        task_queue = MockTaskQueue()
        task_queue.enqueue('task1')
        task_queue.enqueue('task2')
        
        self.assertFalse(task_queue.is_empty())
        self.assertEqual(task_queue.dequeue(), 'task1')
        self.assertEqual(task_queue.dequeue(), 'task2')
        
    def test_is_empty(self):
        task_queue = MockTaskQueue()
        self.assertTrue(task_queue.is_empty())
        
        task_queue.enqueue('task1')
        self.assertFalse(task_queue.is_empty())
        
        task_queue.dequeue()
        self.assertTrue(task_queue.is_empty())
    
    def test_dequeue_empty(self):
        task_queue = MockTaskQueue()
        with self.assertRaises(IndexError):
            task_queue.dequeue()

if __name__ == '__main__':
    unittest.main()
