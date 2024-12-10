import asyncio 
import asyncssh

#define async function , to be called later from by asyncio.run
async def connect_and_run(host,username,password,commands):
    #connect to a host 
    async with asyncssh.connect(host = host, username = username , password = password , known_hosts = None) as connection: 
        # result = await connection.run(command)
        # return result 
        results = []
        for cmd in commands:
            #send command to host , append the result to a list  
            result = await connection.run(cmd)
            results.append(result)
        # return a list of results of each command 
        return results

commands = ('ip addr', 'who -a' ,'username -a') 

#run the function connect_and_run
results = asyncio.run(connect_and_run('10.123.2.10','root','root',commands))

#print the result 
for result in results:
    print(f'STDOUT:\n {result.stdout}')
    print(f'STDERR:\n {result.stderr}')
    print ("#" * 30 )
