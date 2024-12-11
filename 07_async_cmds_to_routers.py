import asyncio
import asyncssh

#define fuction to connect to individual router and run set of command.

async def connect_to_router(hostname,username,password,commands):
    async with asyncssh.connect(host = hostname,username = username, password = password, known_hosts = None) as connect:
        process = await connect.create_process()

        results = list()

        for command in commands:
            process.stdin.write(f'{command}\n')
            await asyncio.sleep(1)
            result = await process.stdout.read(100000)
            results.append(result)

        process.stdin.write('exit\n')
        return results

#create function to SSH to list of routers . Each router will be run set of command 

async def main(router_list,command_list):
    with open (command_list ,'r') as f:
        commands = f.readlines()
        commands = [r[:-1] for r in commands]
        print(commands)

    tasks = []

    for router in router_list:
        task = connect_to_router(router['hostname'],router['username'],router['password'],commands)
        tasks.append(task)

    results = await asyncio.gather(*tasks,return_exceptions = True)

    for result in results:
        for r in result: 
            print(r)

router_list = [
    {'hostname':'10.123.2.1','username':'u1','password':'cisco'},
    {'hostname':'10.123.2.4','username':'u1','password':'cisco'},
    {'hostname':'10.123.2.5','username':'u1','password':'cisco'},
]

asyncio.run(main(router_list = router_list ,command_list = 'command_list.txt'))



