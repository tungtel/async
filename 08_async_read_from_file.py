import asyncio
import asyncssh

async def connect_to_router(ip,user,password,cmds):
    async with asyncssh.connect(host = ip, username = user, password = password,known_hosts = None ) as connect:
        process = await connect.create_process()

        results = list()

        for cmd in cmds: 
            process.stdin.write(f'{cmd}\n')
            if cmd == 'show run':
                await asyncio.sleep(5)
            else:
                await asyncio.sleep(1)
            result = await process.stdout.read(100000)
            results.append(result)
        process.stdin.write('exit\n')
        return results

async def main(devices,command_list):
    with open (command_list ,'r') as f:
        commands = f.readlines()
        commands = [r[:-1] for r in commands]
        print(commands)

    tasks = []

    with open(devices ,'r') as f:
        devices = f.read()
        devices = devices.splitlines()
        print(devices)
    
    creds = ['u1','cisco']

    for device in devices:
        task = connect_to_router(ip = device,user = creds[0],password = creds[1],cmds = commands)
        tasks.append(task)

    results = await asyncio.gather(*tasks,return_exceptions = True)

    for result in results:
        for r in result: 
            print(r) 

asyncio.run(main(devices = 'devices.txt' ,command_list = 'command_list.txt'))
