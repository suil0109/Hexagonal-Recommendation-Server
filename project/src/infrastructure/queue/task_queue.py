from src.adapters.repository.sql_point_repository import SQLPointRepository
from src.domain.models.dto_point import PointInfo

import time
import queue

class TaskQueueRepository(SQLPointRepository):
    
    def __init__(self):
        super().__init__()  
        self._queue = queue.Queue()

    def enqueue(self, transaction, point_info: PointInfo):
        task = PointInfo(
            rec_id = point_info.rec_id,
            user_id = point_info.user_id,
            transaction= transaction,
            point= point_info.point,
        )
        self._queue.put(task)

    def dequeue(self):
        return self._queue.get(block=False) if not self._queue.empty() else None

    def is_empty(self):
        return self._queue.empty()

    def task_done(self):
        self._queue.task_done()
        print("finished")

def worker_task(queue_adapter):
    while 1:
        try:
            task = queue_adapter.dequeue()
            if task:
                # MySql History DB Insert
                # MySql Balance DB Update
                # Redis Update
                print("task update start!!!!!!!!")
                queue_adapter.update_db_from_queue(task)
                # queue_adapter.redis_update()
                queue_adapter.task_done()
            time.sleep(0.1)
        except Exception as e:
            print(e)


# Queue applicaiton for Point Service
print("[Task Queue Service] Task Queue Initalized!")
# global task_queue
task_queue = TaskQueueRepository()