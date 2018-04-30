from . aws_utils import createInstance, waitUntilInstanceRuns, executeCommand, createTag
from . config import efsID, mountFolder

commands = [
    "sudo yum install -y amazon-efs-utils",
    "mkdir {}".format(mountFolder),
    "sudo mount -t efs {}:/ {}".format(efsID, mountFolder),
    "sudo yum install --assumeyes mesa-libGLU",
    "sudo yum install --assumeyes libXi",
    "sudo yum install --assumeyes libXrender"
]

def setupRenderingInstance():
    instanceID = createInstance()
    waitUntilInstanceRuns(instanceID)

    for command in commands:
        executeCommand(instanceID, command)


    createTag(instanceID, "PreparedForRendering", "Yes")