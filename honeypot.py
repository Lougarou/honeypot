import asyncio
import logging
import fire

async def smiley_protocol(reader, writer):
  try:
    data = await reader.read(1024)
    message = ""
    try:
      message = data.decode()
    except UnicodeDecodeError:
      message = data
    addr = writer.get_extra_info('peername')
    logging.info(f"Received {message!r} from {addr!r}")
    writer.write(b":D")
    await writer.drain()
    writer.close()
  except ConnectionResetError:
    pass #do nothing, not useful for data collection

async def launch_pot(address='127.0.0.1',port=8888):
  server = await asyncio.start_server(
    smiley_protocol, address, port)

  addr = server.sockets[0].getsockname()
  logging.info(f'Serving on {addr}')

  async with server:
    await server.serve_forever()

async def main(address="127.0.0.1", port_start=1, port_end=2**16-1, log='honeypot.log'):
  logging.basicConfig(level=logging.INFO,
                      format='%(asctime)s %(levelname)-8s %(message)s',
                      filename=log,
                      filemode='a')
  tasks = []
  for i in range(port_start,port_end + 1):
    tasks.append(asyncio.create_task(launch_pot(address, i)))
  await asyncio.gather(*tasks)

if __name__ == '__main__':
  fire.Fire(main)