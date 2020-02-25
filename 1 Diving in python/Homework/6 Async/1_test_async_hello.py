import datetime as dt
import asyncio
import time


async def count():
    print(f"One: {dt.datetime.now()}")
    await asyncio.sleep(1)
    # time.sleep(1)
    print(f"Two: {dt.datetime.now()}")


async def main():
    await asyncio.gather(count(), count(), count())

if __name__ == "__main__":
    asyncio.run(main())
