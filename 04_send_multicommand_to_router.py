import asyncio 
import asyncssh 

async def connect_to_router(host,username,password,commands):
    results = []
    try:
        #connect to router
        async with asyncssh.connect(host = host , username = username , password = password , known_hosts = None) as connect:            
           
           #Start an interactive shell process
           process = await connect.create_process()

           for command in commands:
                #send command to the process
                process.stdin.write(f'{command}\n')
                if command == 'show run':
                    await asyncio.sleep(5)
                else:
                    await asyncio.sleep(1)
                #Read the output 
                output = await process.stdout.read(100000)
                results.append(f'command: {command}\n{output}')

           #exit the session 
           process.stdin.write('exit\n')
           for result in results:
                print(result)

    except Exception as e:
        print(f'An error code occurred :{e}')
        return None

#List of commands 
commands = ['terminal length 0','enable','cisco','show version', 'show run']

#run the asyncio event loop 
asyncio.run(connect_to_router('10.123.2.1','u1','cisco',commands))
