import time

import rpc
import logging

from context import lab_logging

lab_logging.setup(stream_level=logging.INFO)

cl = rpc.Client()
cl.run()

def print_result(result):
    print(f"Result: {result.value}")

base_list = rpc.DBList({'foo'})
t = cl.append('bar', base_list, print_result)

while t.is_alive():
    print("Doing other work while waiting for the result...")
    time.sleep(1)
t.join()  # wait for the thread to finish

cl.stop()
