# import sys
# import time

from . import config
from . import nginx
from . import instance

def printFile():
    print("I am Manger.py")

def run(argv1, rootName, remoteHostname, externalPort, externalPorts, framework):
    # rootName="two-deploy", remoteHostname="instance.two-deploy.com", externalPort=1288, externalPorts=[1281, 1282, 1283], framework = 'reactjs'
    cconfig = config.Config(rootName, remoteHostname, externalPort, externalPorts, framework)
    nconfig = nginx.Nginx(cconfig.NGINX, cconfig)
    ii = instance.Instance(cconfig, nconfig)

    # argl = len(sys.argv)
    # argv1 = sys.argv[1]
    if(argv1 == 'start'):
        ii.reloadDocker()

    if(argv1 == 'stop'):
        ii.stopDocker()
    

# if __name__ == '__main__':
#     None
