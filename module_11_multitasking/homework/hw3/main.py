import logging
import random
import threading
import time
from typing import List

TOTAL_TICKETS: int = 100
AVAILABLE_TICKETS: int = 10

logging.basicConfig(level=logging.INFO)
logger: logging.Logger = logging.getLogger(__name__)

class Director(threading.Thread):

    def __init__(self, semaphore: threading.Semaphore) -> None:
        super(Director, self).__init__()
        self.lock: threading.Semaphore = semaphore
        logger.info(f"Director {self.name} started work!")

    def run(self) -> None:
        global TOTAL_TICKETS, AVAILABLE_TICKETS
        while TOTAL_TICKETS:
            if AVAILABLE_TICKETS < 4:
                with self.lock:
                    tickets_to_print = 10 - AVAILABLE_TICKETS % 10
                    if tickets_to_print > TOTAL_TICKETS:
                        tickets_to_print = TOTAL_TICKETS
                    AVAILABLE_TICKETS += tickets_to_print
                    TOTAL_TICKETS -= tickets_to_print
                    logger.info(f'Director put {tickets_to_print} new tickets')
        logger.info(f'Director {self.name}  stop work, not more tickets left!')

class Seller(threading.Thread):

    def __init__(self, semaphore: threading.Semaphore) -> None:
        super().__init__()
        self.sem: threading.Semaphore = semaphore
        self.tickets_sold: int = 0
        logger.info(f'Seller {self.name} started work')

    def run(self) -> None:
        global AVAILABLE_TICKETS
        is_running: bool = True
        while is_running:
            self.random_sleep()
            with self.sem:
                if AVAILABLE_TICKETS <= 0:
                    break
                self.tickets_sold += 1
                AVAILABLE_TICKETS -= 1
                logger.info(f'{self.name} sold one;  {TOTAL_TICKETS} left')
        logger.info(f'Seller {self.name} sold {self.tickets_sold} tickets')

    def random_sleep(self) -> None:
        time.sleep(random.randint(0, 1))


def main() -> None:

    semaphore: threading.Semaphore = threading.Semaphore()
    director = Director(semaphore=semaphore)
    director.start()

    sellers: List[Seller] = [director]
    for _ in range(4):
        seller = Seller(semaphore)
        seller.start()
        sellers.append(seller)

    for seller in sellers:
        seller.join()


if __name__ == '__main__':
    main()
