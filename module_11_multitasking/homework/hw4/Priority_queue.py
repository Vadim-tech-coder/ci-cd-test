import threading
import queue
import logging
import random
import time



logging.basicConfig(level = logging.INFO)
logger = logging.getLogger(__name__)

class Task:

    def __init__(self, priority: int, description: str):
        self.priority = priority
        self.description = description

TASKS = [Task(0, 'Task 1'), Task(100, 'Task 2'), Task(5, 'Task 3'), Task(89, 'Task 4'), Task(99, 'Task 5')]

def random_sleep():
    time.sleep(random.randint(1, 5))

class Producer(threading.Thread):

    def __init__(self, queue: queue.PriorityQueue):
        super().__init__()
        self.queue = queue

    def run(self):
        logger.info('Producer: Добавление задач в очередь')
        for task in TASKS:
            self.queue.put((task.priority, task))
        logger.info('Producer: Все задачи были добавлены в очередь! ')

class Consumer(threading.Thread):

    def __init__(self, queue: queue.PriorityQueue):
        super().__init__()
        self.queue = queue


    def run(self):
        logger.info('Consumer: Начало выполнения поставленных в очередь задач!')
        while True:
            start = time.time()
            priority, task = self.queue.get()
            random_sleep()
            logger.info(f'Выполняется задача {task.description} с приоритетом {task.priority}, sleep({time.time() - start})')
            if self.queue.empty():
                break
        logger.info("Consumer: Все задачи выполнены!")


if __name__ == '__main__':
    main_queue = queue.PriorityQueue()
    producer = Producer(main_queue)
    consumer = Consumer(main_queue)
    producer.start()
    consumer.start()
    producer.join()
    consumer.join()

