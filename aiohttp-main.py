# https://github.com/coderecode-com/async-await-demo
import asyncio 
import uvloop
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
import aiohttp
import time
from loguru import logger
start_time = time.perf_counter()

async def send_request(session: aiohttp.ClientSession, semaphore: asyncio.Semaphore) -> int:
    url = "https://pokeapi.co/api/v2/pokemon/ditto"
    async with semaphore:
        logger.info("Sending request")
        async with session.get(url) as response:
            logger.info("Response received")
            return response.status

async def main() -> int:
    semaphore = asyncio.Semaphore(200)
    async with aiohttp.ClientSession() as session:
        tasks = [asyncio.create_task(send_request(session, semaphore)) for _ in range(1,151)]
        status_codes = await asyncio.gather(*tasks)

    logger.info("All work done")
    if session:
        logger.info(f"{session=}")
    return 0 if all(c == 200 for c in status_codes) else 1

if __name__ == "__main__":
    asyncio.run(main())
    logger.info("--- %s seconds ---" % (time.perf_counter() - start_time))
