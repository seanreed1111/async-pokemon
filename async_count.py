#!/usr/bin/env python3
# countasync.py

import asyncio

async def count():
    print("One")
    await asyncio.sleep(1)
    print("Two")

async def main():
    await asyncio.gather(count(), count(), count())

if __name__ == "__main__":
    import time
    start_time  = time.perf_counter()
    asyncio.run(main())
    elapsed = time.perf_counter() - start_time
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")