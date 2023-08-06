import utilum
from halo import Halo
# import requests
import os

from . import utils
from .logger import controlledPrint
from .helpers import instance as helper
from .template import Production, Build, Dockerfile


class Instance:
    def __init__(self, config, nginx):
        self.config = config
        self.nginx = nginx
        # 2-way map
        self.TWO_MAP = dict()

        self.DockerfilePath = os.path.join(config.CWD, 'Dockerfile')
        utilum.file.createPath(self.DockerfilePath)

        # ponWriting
        ponContent = Production.read(self.config.framework)
        utilum.file.clearFile(config.PON_PATH)
        utilum.system.shell(f"chmod 777 {config.PON_PATH}")
        utilum.file.writeFile(config.PON_PATH, ponContent)

        GET_WAIT_CHUNK_TIME = 1  # 1 second
        MAX_GET_RETRY_COUNT = 160  # 160 times

    def dockerBuild(self, imageName, port):
        imageName = imageName + "-" + str(port)
        utilum.system.shell(f'docker build -t {imageName} .')
        return None

    def dockerBuildCheck(self, imageName):
        return utilum.system.shellRead(f'docker build -t {imageName} . ')

    def dockerRun(self, port, imageName, restartOnFailure=False):
        imageName = imageName + "-" + str(port)
        cmd = ''

        if (restartOnFailure):
            cmd = f'docker run --restart=on-failure -d -p {str(port)}:{str(port)} {imageName}'
        else:
            cmd = f'docker run -d -p {str(port)}:{str(port)} {imageName}'

        controlledPrint([cmd], 'dockerRun()', self.config.mode)
        utilum.system.shell(cmd)
        return None

    def dockerStopWithContainerId(self, containerId):
        utilum.system.shell(f"docker stop {containerId}")
        utilum.system.shell(f"docker rm {containerId}")
        return None

    def printer(self, params, actionName):
        if (params["iport"] != None):
            print(
                f"[{params['iport'] + 1 }/{len(params['EXTERNAL_PORTS'])}] {actionName}...")
        elif (params["port"] != None):
            print(f"Port: {params['port']}")
        elif (params["containerId"] != None):
            print(f"Container: {params['containerId']}")
        elif (params["IMAGE_NAME"] != None):
            print(f"Name: {params['IMAGE_NAME']}")
        return None

    def buildChecker(self):
        buildDocker = Build.read(self.config.framework)

        utilum.file.clearFile(self.DockerfilePath)
        utilum.file.writeFile(self.DockerfilePath, buildDocker)

        imageName = self.config.IMAGE_NAME + '-build-check'

        print(f"[{imageName}][Build] Checking...")
        out, err = self.dockerBuildCheck(imageName)
        if ("fail" in out.decode("utf-8").replace("\n", "")):
            print("[Build] Failed")
            return False
        else:
            print("[Build] Success")
            return True

    def reloadDocker(self):

        # 0) Build Checker
        if (self.buildChecker() == False):
            return

        # 1) Getting/Collecting Docker Info
        PORTS, CONTAINERS, TWO_MAP = helper.getAttributes(
            self, self.config.EXTERNAL_PORTS)
        self.PORTS = PORTS
        self.CONTAINERS = CONTAINERS
        self.TWO_MAP = TWO_MAP
        # controlledPrint([PORTS, CONTAINERS], 'self.TWO_MAP', self.config.mode)

        # params, useful for printing
        params = dict()
        params["EXTERNAL_PORTS"] = self.config.EXTERNAL_PORTS
        params["IMAGE_NAME"] = self.config.IMAGE_NAME

        # 2) Building Docker Images
        for iport, port in enumerate(self.config.EXTERNAL_PORTS):
            docker = Dockerfile.read(self.config.framework).replace(
                self.config.PORT_TEMPLATE, str(port))

            utilum.file.clearFile(self.DockerfilePath)
            utilum.file.writeFile(self.DockerfilePath, docker)

            print(
                f"PORT:{str(port)} [Building][{str(iport+1)}/{str(len(self.config.EXTERNAL_PORTS))}] Image...")

            # method:invoke
            self.dockerBuild(self.config.IMAGE_NAME, port)

            params["iport"] = iport
            params["port"] = port

            if (port in self.TWO_MAP):
                containerId = self.TWO_MAP[port]
            else:
                containerId = -1

            params["containerId"] = containerId

            backupImageId = False
            backupImageName = f"{self.config.IMAGE_NAME}-backup"
            newContainerId = False

            if (containerId != -1):
                dockerCommit = f"docker commit {containerId} {backupImageName}"
                backupImageId = utilum.system.shellRead(
                    dockerCommit)[0].decode("utf-8")
                if (":" in backupImageId):
                    backupImageId = backupImageId[backupImageId.index(
                        ":")+1:].replace("\n", "")

            # run nginx for all but this single external port
            self.nginx.runNginxForAllButThisPort(port)

            # 3) Running Docker Images
            controlledPrint([self.config.IMAGE_NAME, containerId, PORTS,
                            self.TWO_MAP], 'self.config.IMAGE_NAME', self.config.mode)
            if (port in PORTS):
                # i) port is currently occupied, stopping and then starting

                action = "Reloading"
                self.printer(params, action)
                spinner = Halo(text=action, spinner='dots')
                spinner.start()

                self.dockerStopWithContainerId(containerId)
                self.dockerRun(port, self.config.IMAGE_NAME, True)
                newContainerId = utils.getContainerIdFromPort(port)
            else:
                # ii) instance starting freshly
                action = "Starting"
                self.printer(params, action)
                spinner = Halo(text=action, spinner='dots')
                spinner.start()
                # print()

                # port is not occupied
                self.dockerRun(port, self.config.IMAGE_NAME, True)
                newContainerId = utils.getContainerIdFromPort(port)

            # sleeping while port comes up
            '''instanceStatus=> True:   port is up
                            => False:  port is still in sleep'''
            instanceStatus = utils.isPortAvailable(
                self.config.PROTOCOL, self.config.HOSTNAME, port)
            spinner.stop()

            if (instanceStatus):
                # i) Instance Started Succesfully
                print("[Done]")
            else:
                # ii) Instance Start Failed
                action = "Rolling Back"
                self.printer(params, action)

                print("newContainerId: ", newContainerId)
                print("backupImageName: ", backupImageName)

                spinner = Halo(text=action, spinner='dots')
                spinner.start()

                # rollback() and exit/break
                self.dockerStopWithContainerId(newContainerId)
                self.dockerRun(port, backupImageName, True)
                spinner.stop()
                break

        # run nginx for all ports
        print("[Start][Nginx][All]")
        self.nginx.runNginxForAllPort()
        print("\n", "[End][Nginx][All]")

    def stopDocker(self):

        # 1) Stopping Controller Instances

        # get port and container ids
        for iport, port in enumerate(self.config.EXTERNAL_PORTS):
            containerId = utilum.getContainerIdFromPort(port)
            self.config.PORTS.append(port)
            self.config.CONTAINERS.append(containerId)
            self.TWO_MAP[port] = containerId
            self.TWO_MAP[containerId] = port

        print()
        params = dict()
        params["EXTERNAL_PORTS"] = self.config.EXTERNAL_PORTS
        params["IMAGE_NAME"] = self.config.IMAGE_NAME

        for iport, port in enumerate(self.config.EXTERNAL_PORTS):
            params["iport"] = iport
            params["port"] = port

            if (port in self.TWO_MAP):
                containerId = self.TWO_MAP[port]
            else:
                containerId = -1

            params["containerId"] = containerId

            # run nginx for all but this port
            self.nginx.runNginxForAllButThisPort(port)

            if (port in self.config.PORTS):
                action = 'Stopping'
                self.printer(params, action)

                spinner = Halo(text=action, spinner='dots')
                spinner.start()
                # print()

                self.dockerStopWithContainerId(containerId)
                # port is currently occupied
                # print(port,containerId, 'Occupied Port')

                spinner.stop()

                print("[Done]")
                print()

        # 2) Stopping Nginx Instance
        self.nginx.stopNginxContainer()
        print("[Stopping] Done")
        print()
