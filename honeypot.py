import utils.formatters as formatters
import utils.handlers as handlers
from datetime import datetime

import asyncio
import logging
import fire

logger = logging.getLogger(__name__)

async def smiley_protocol(reader, writer):
  try:
    data = await reader.read(1024)
    message = ""
    try:
      message = data.decode()
    except UnicodeDecodeError:
      message = data
    addr = writer.get_extra_info('peername')
    print([str(datetime.now().strftime("%m/%d/%Y, %H:%M:%S")),message, str(addr[0])+":"+str(addr[1])])
    logger.info([(f"{message!r}"), f"{addr[0]!r}", f"{addr[1]!r}"])
    writer.write(b":D")
    await writer.drain()
    writer.close()
  except ConnectionResetError:
    pass #do nothing, not useful for data collection

async def launch_pot(address='127.0.0.1',port=8888):
  server = await asyncio.start_server(
    smiley_protocol, address, port)

  async with server:
    await server.serve_forever()

async def main(address="127.0.0.1", port_start=1, port_end=2**16-1, log='honeypot.log'):

  logger.setLevel(logging.DEBUG)
  loggingStreamHandler = handlers.CSVTimedRotatingFileHandler(filename=log,
															  header=["time", "message", "from", "port"])  # to save to file
  loggingStreamHandler.setFormatter(formatters.CSVFormatter())
  logger.addHandler(loggingStreamHandler)
  tasks = []
  for i in range(port_start,port_end + 1):
    tasks.append(asyncio.create_task(launch_pot(address, i)))
  await asyncio.gather(*tasks)

if __name__ == '__main__':
  fire.Fire(main)