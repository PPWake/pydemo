import sys
import asyncio

async def execute_command(cmd:str, whichsh="/bin/bash", raiseException=False):
    if not cmd:
      return 1, "cmd is none!"

    try:
      # create is a conroutes
      create_coroutine = asyncio.create_subprocess_exec(whichsh, "-c", cmd, stderr=asyncio.subprocess.PIPE, 
                                              stdout=asyncio.subprocess.PIPE)

      # create a process
      proc = await create_coroutine
      (stdout, stderr)=  await proc.communicate()
      if stdout:
        stdout = stdout.decode()
        stdout = stdout.strip("\n")

      if stderr:
        stderr = stderr.decode()
        stderr = stderr.strip("\n")

      # wait for terminal and get status
      status = await proc.wait()
    except Exception as e:
      if raiseException:
        raise e
      return 1, None, str(e)
    return status, stdout, stderr


def test_command():
  if sys.platform == "win32":
      loop = asyncio.ProactorEventLoop()
      asyncio.set_event_loop(loop)
  else:
      loop = asyncio.get_event_loop()

  status, stdout, stderr = loop.run_until_complete(execute_command("ls -l"))
  print("show value status: %s \nstdout: %s \nstderr:%s"  % (str(status), stdout, stderr))
  loop.close()

if __name__ == "__main__":
    test_command()