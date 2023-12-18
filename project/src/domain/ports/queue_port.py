from abc import ABC, abstractmethod

class TaskQueuePort(ABC):
    
    @abstractmethod
    def enqueue(self, task):
        pass
    
    @abstractmethod
    def dequeue(self):
        pass
    
    @abstractmethod
    def is_empty(self):
        pass
