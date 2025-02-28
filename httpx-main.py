#https://github.com/jankrepl/mildlyoverfitted/blob/master/mini_tutorials/httpx_rate_limiting/script.py
import asyncio
import logging
import time
import httpx
from loguru import logger

logging.getLogger("httpx").setLevel(logging.WARNING)
logging.basicConfig(format="%(asctime)s %(name)s %(message)s", level=logging.INFO)

start_time = time.perf_counter()
async def send_request(client: httpx.AsyncClient, semaphore: asyncio.Semaphore) -> int:
    url = "https://pokeapi.co/api/v2/pokemon/ditto"
    async with semaphore:
        logger.info("Sending request")
        response = await client.get(url)
        logger.info("Response received")

    return response.status_code


async def main() -> int:
    semaphore = asyncio.Semaphore(20)
    async with httpx.AsyncClient() as client:
        tasks = [asyncio.create_task(send_request(client, semaphore)) for _ in range(1,151)]
        status_codes = await asyncio.gather(*tasks)

    logger.info("All work done")

    return 0 if all(c == 200 for c in status_codes) else 1


if __name__ == "__main__":
    asyncio.run(main())
    print("--- %s seconds ---" % (time.perf_counter() - start_time))