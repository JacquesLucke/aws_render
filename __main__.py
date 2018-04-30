import sys
from threading import Thread

from . start_render import startRendering
from . setup_new_instance import setupRenderingInstance
from . aws_utils import terminateAllInstances

if len(sys.argv) < 2:
    print("at least one argument required")
    sys.exit()

argument = sys.argv[1].lower()

if argument == "new":
    if len(sys.argv) == 3:
        amount = int(sys.argv[2])
    else:
        amount = 1

    threads = []
    for _ in range(amount):
        threads.append(Thread(target = setupRenderingInstance))
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
elif argument == "terminate":
    terminateAllInstances()
elif argument == "render":
    startRendering()
else:
    print("unknown command line argument")
    sys.exit()