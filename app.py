import asyncio
import time
import aiohttp
import more_itertools
from get_inner_data import get_inner_data
from dict_template import template
from db_model import DbClass

URL = 'https://swapi.dev/api'


async def get_person(person_id: int) -> dict:
    session = aiohttp.ClientSession(
        connector=aiohttp.TCPConnector(ssl=False))  # connector=aiohttp.TCPConnector(ssl=False)
    response = await session.get(f'{URL}/people/{person_id}')
    if response.status != 200:
        return await session.close()

    response_json = await response.json()
    return await get_inner_data(session, response_json, template)


def format_none(request_list):
    format_results = []
    for task in request_list:
        if task is None:
            continue
        format_results.append(task)
    return format_results


async def main(db_url):
    db = DbClass(db_url)
    for person_id_chunck in more_itertools.chunked(range(1, 100), 10):
        list_of_task = []
        for person_id in person_id_chunck:
            task = asyncio.create_task(get_person(person_id))
            list_of_task.append(task)
        results = await asyncio.gather(*list_of_task)
        data_to_db = format_none(results)
        if not data_to_db:
            continue
        db.upload_to_db(data_to_db)


start = time.time()
PG_DSN = 'postgresql://admin:1234@127.0.0.1:5435/asyncio'
loop = asyncio.get_event_loop()
loop.run_until_complete(main(PG_DSN))
print('working time', time.time() - start)
