# Basic Honeypot
Listens to all ports and logs requests.
Sample run showed 200 attacks per minute which is huge on a DigitalOcean vm.
Why? Just a fun weekend project

## Requirements
- Python3.8
- asyncio
- logging
- fire

## How to run
python3.8 honeypot.py --port_start=0 --port_end=65535 --address=<insert-ip> --log=honeypot.log

## TODO
- Structured log
