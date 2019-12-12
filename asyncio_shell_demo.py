import asyncio.subprocess
import sys

async def execute_command(cmd):
    if not cmd:
      return 1, "cmd is none!"
      
    try:
      # create is a conroutes
      create = asyncio.create_subprocess_shell(cmd, stderr=asyncio.subprocess.PIPE, 
                                                stdout=asyncio.subprocess.PIPE)
      # create a process
      proc = await create

      # avoid proc.wait block by the big output
      (stdout_data, stderr_data)=  await proc.communicate()
      output = stdout_data if stdout_data else stderr_data
      
      # 0 is success
      status = 1
      # wait for terminal and get status
      status = await proc.wait()
    except Exception as e:
      print("Get exception %s" % (str(e)))
      return 1, str(e)
    return status, output

if sys.platform == "win32":
    loop = asyncio.ProactorEventLoop()
    asyncio.set_event_loop(loop)
else:
    loop = asyncio.get_event_loop()

status, output = loop.run_until_complete(execute_command("ls -l"))
print("show value status: %s output: %s" % (str(status), output.decode()))
loop.close()