from . aws_utils import executeCommand, getRunningInstancesWithTag
from . config import mountFolder
from threading import Thread

def startRendering():
    threads = []
    for instance in getRunningInstancesWithTag("PreparedForRendering", "Yes"):
        threads.append(Thread(target = startRenderingOnInstance, args = (instance.id,)))
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

def startRenderingOnInstance(instanceID):
    command = ("~/{0}/blender/blender-2.79b-linux-glibc219-x86_64/blender "
               "-b ~/{0}/blends/scene_window_03_pack.blend "
               "-o ~/{0}/render/ "
               "-a").format(mountFolder)

    executeCommand(instanceID, command)