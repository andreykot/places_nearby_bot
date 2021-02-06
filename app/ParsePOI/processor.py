import datetime
import json
from typing import Callable

import asyncio
import aiohttp
from aiohttp import ClientTimeout


async def post(url: str, data, custom_middleware: Callable = None):
    print('start', datetime.datetime.now())
    async with aiohttp.ClientSession() as session:
        async with session.post(url=url, data=data,
                                timeout=ClientTimeout(15)) as response:

            result = await response.read()
            if custom_middleware:
                result = custom_middleware(result)
            print(datetime.datetime.now(), json.loads(result))
            return result


async def test():
    async def test_query(lat, lon, radius):
        overpass_query = lambda lat, lon, radius: f"""
        [out:json][timeout:25];
        (
        node(around:{radius}, {lat}, {lon})["historic"];
        node(around:{radius}, {lat}, {lon})["tourism"];
        );
        out;
            """

        return await post(url=r"https://z.overpass-api.de/api/interpreter",
                          data={'data': overpass_query(lat, lon, radius)})

    task1 = asyncio.create_task(test_query(60.016, 30.258, 2000))
    task2 = asyncio.create_task(test_query(60.0, 30.258, 10000))
    task3 = asyncio.create_task(test_query(60.016, 30.158, 3000))
    res1 = await task1
    res2 = await task2
    res3 = await task3


if __name__ == "__main__":
    asyncio.run(test())
