import time
import boto3
import paramiko

from . config import imageID, instanceType, keyName, keyPath, userName, efsID

ec2 = boto3.resource("ec2")

def createInstance():
    log("Start Instance")
    instance = ec2.create_instances(
        ImageId = imageID,
        MinCount = 1,
        MaxCount = 1,
        InstanceType = instanceType,
        KeyName = keyName
    )[0]
    log("Create Instance with ID {}.".format(instance.id))
    return instance.id

def executeCommand(instanceID, command):
    log("Execute '{}' on {}".format(command, instanceID))
    key = paramiko.RSAKey.from_private_key_file(keyPath)

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    client.connect(
        hostname = instanceFromID(instanceID).public_dns_name,
        username = userName,
        pkey = key
    )

    stdin, stdout, stderr = client.exec_command(command)

    while True:
        line = stdout.readline()
        if line == "":
            break
        else:
            print("    | " + line, end = "")

    stdOutText, stdErrText = stdout.read(), stderr.read()
    client.close()

    log("Done.")

    return stdOutText, stdErrText

def instanceFromID(instanceID):
    return ec2.Instance(instanceID)

def isRunning(instanceID):
    return instanceRuns(instanceFromID(instanceID))

def isTerminated(instanceID):
    return instanceFromID(instanceFromID).state["Name"] == "terminated"

def instanceRuns(instance):
    return instance.state["Name"] == "running"

def log(message):
    print(time.ctime(), "   ", message)

def waitUntilInstanceRuns(instanceID):
    log("wait until {} runs".format(instanceID))
    while not isRunning(instanceID):
        log("not yet running")
        time.sleep(3)
    log("instance is running")

def createTag(instanceID, key, value):
    log("try create tag on {}: {} -> {}".format(instanceID, key, value))
    instanceFromID(instanceID).create_tags(Tags = [{"Key" : key, "Value" : value}])
    log("Done.")

def getRunningInstancesWithTag(key, value):
    instances = []
    for instance in getRunningInstances():
        if instance.tags is not None:
            if any(tag["Key"] == key and tag["Value"] == value for tag in instance.tags):
                instances.append(instance)
    return instances

def getRunningInstances():
    return [inst for inst in ec2.instances.all() if instanceRuns(inst)]

def terminateAllInstances():
    for instance in ec2.instances.all():
        try:
            instance.terminate()
        except:
            print("could not terminate:", instance.id)