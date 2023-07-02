import asyncio
from datetime import datetime, timedelta, timezone
import sys

from scrapper import collect_task, right_now
from storage import Storage, CsvStorage


"""TODO: wait until timestamp?"""


async def collect_and_save(storage: Storage) -> None:
    data = await collect_task()
    await storage.save(data)


async def scrape_forever(storage: Storage, minutes) -> None:
    while True:
        await collect_and_save(storage)
        now = right_now()
        delta = timedelta(minutes=minutes)
        print(f'Next request scheduled at {now + delta}')
        # timer_handle = loop.call_later(delta, callback)
        await asyncio.sleep(minutes * 60)


async def main(filename: str, delay: int) -> None:
    background_tasks = set()
    storage = CsvStorage(filename)
    
    task = asyncio.create_task(scrape_forever(storage, delay))
    background_tasks.add(task)  # this creates a strong reference
    task.add_done_callback(background_tasks.discard)  # Make the task remove itself by destroying the reference
    
    await asyncio.gather(*background_tasks)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python runner.py [filename]')
        exit(1)

    loop = asyncio.get_event_loop()    
    loop.run_until_complete(main(sys.argv[1], 5))
