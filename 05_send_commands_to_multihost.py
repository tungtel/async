#import required library 
import asyncio 
import asyncssh

#Define asynchronous function run_client using async def syntax 
#Asynchronous function allow non-blocking execution
async def run_client(host,username,password,command):
    #asyncssh.connect is non-blocking coroutine to establish SSH to remote host 
    #async with syntax ensures that the SSH connection (connection) is automatically closed
    async with asyncssh.connect(host = host , username = username, password = password) as connection:
        #returns the result of await connection.run(command)
        #await ensures the program waits for the command to execute before proceeding.
        return await connection.run(command)

#declares an asynchronous function that will run multiple tasks concurrently

async def run_multiple_clients(hosts):
    tasks = []
    for host in hosts:
        #run_client is an async function, calling it returns a coroutine object (task)
        task = run_client(host['host'],host['username'],host['password'],host['command'])
        tasks.append(task)

    #asyncio.gather is used to run all the tasks in the tasks list concurrently.
    #\*tasks syntax unpacks the list of coroutines into individual arguments for asyncio.gather.
    #return_exceptions=True ensures that any exceptions raised by a task are returned as part of the results, instead of stopping execution
    results = await asyncio.gather(*tasks,return_exceptions = True)

    #task counter
    i = 0 

    #for each result in result list 
    for result in results: 
        #If the result is an exception, this block executes.
        #This ensures failures are reported without breaking the loop
        if isinstance(result,Exception):
            print(f'Task{i} failed')

        # If the task exited with a non-zero exit code, report the error
        elif result.exit_status != 0:
            print(f'task{i} existed with status :{result.exit_status}')
            print(result.stderr,end = '')
         # If the task succeeded, print the output
        else: 
            print(f'task{i} succeeded:')
            print(result.stdout,end = '')
        print('#')

        i += 1

hosts = [
    {'host':'10.123.2.10','username':'root','password':'root','command':'ifconfig' },
    {'host':'10.123.2.10','username':'root','password':'root','command':'who -a' },
    {'host':'10.123.2.10','username':'root','password':'root','command':'uname -a ' }
]

asyncio.run(run_multiple_clients(hosts))
