#!/usr/bin/python3
from session import * 
from whisker_client import *
import asyncio

s = Session()

event_loop = asyncio.get_event_loop()
c = WhiskerClient(event_loop, 'localhost', port)
print(c.filename)

@asyncio.coroutine
def run():
    yield from c.setup(s.subject)

event_loop.run_until_complete(c.connect())
print('Client connected')
event_loop.run_until_complete(run())

try:
    event_loop.run_forever()
except KeyboardInterrupt:
    print(" Received Ctrl-C. Exiting.")






