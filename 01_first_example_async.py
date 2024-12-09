import asyncio
import time

def sync_fuction():
    print('one ', end = '')
    time.sleep(1)
    print('two ', end = '')

async def async_function():
    print('one ', end = '')
    await asyncio.sleep(1)
    print('two ', end = '')


async def main():
    # Note that there are 3 awaitable objects: coroutines, tasks and futures.
    task = [async_function() for _ in range(3)]

    #gather task 
    await asyncio.gather(*task)

s = time.time()

# The entrance point of any asyncio program is asyncio.run(main()), where main() is a top-level coroutine.
# asyncio.run() was introduced in Python 3.7, and calling it creates an event loop
# and runs a coroutine on it for you. run() creates the event loop.

asyncio.run(main())
print(f'execution time of async is {time.time() - s }')

print ('\n')

s = time.time()
for _ in range(3):
    sync_fuction()
print(f'execution time of async is {time.time() - s }')
# async def f():
#     pass
# #Python will call "f" function , suspend g() until f() return
# async def g():
#     await f()
