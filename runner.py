import asyncio
from datetime import datetime, timedelta, timezone

from osir import collect_task
from storage import GroupDataStorage


"""TODO: wait until timestamp?"""



async def collect_and_save(storage):
    data = await collect_task()
    await storage.save(data)


async def scrape_forever(storage, minutes):
    
    
    while True:
        await collect_and_save(storage)
        now = datetime.utcnow().replace(tzinfo=timezone.utc)
        delta = timedelta(minutes=minutes)
        print(f'Next request scheduled at {now + delta}')
        # timer_handle = loop.call_later(delta, callback)
        await asyncio.sleep(minutes * 60)


async def main(filename: str, delay: int):
    background_tasks = set()
    storage = GroupDataStorage(filename)
    
    task = asyncio.create_task(scrape_forever(storage, delay))
    background_tasks.add(task)  # this creates a strong reference
    task.add_done_callback(background_tasks.discard)  # Make the task remove itself by destroying the reference
    
    # ale to chyba nie zadziała, jak one zespawnują nowe taski w trakcie
    # bo nie będzie ich w secie w tym momencie    
    await asyncio.gather(*list(background_tasks))


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    
    
    loop.run_until_complete(main('./hoho.csv', 5))
    # loop.run_until_complete(waiting_task(1))
