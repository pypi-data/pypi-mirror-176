import utilum
# import subprocess
import time
import requests


def getContainerIdFromPort(port):
    cmdPublish = f'docker ps -f "publish={port}" -q'
    (out, err) = utilum.system.shellRead(cmdPublish)
    containerId = out.decode("utf-8").replace("\n","")
    return containerId

def isPortAvailable(PROTOCOL, HOSTNAME, port, callCount = 1):
    MAX_GET_RETRY_COUNT = 30
    GET_WAIT_CHUNK_TIME = 2
    
    if(callCount >= MAX_GET_RETRY_COUNT):
        return False
    else:
        rgs = 400
        url = PROTOCOL + "://" + HOSTNAME + ":" + str(port)

        try:
            rg = requests.get(url)
            rgs = rg.status_code
        except:
            rgs = 400

        if(rgs == 200):
            return True
        else:
            callCount +=1
            time.sleep(GET_WAIT_CHUNK_TIME)
            return isPortAvailable(PROTOCOL, HOSTNAME, port, callCount)