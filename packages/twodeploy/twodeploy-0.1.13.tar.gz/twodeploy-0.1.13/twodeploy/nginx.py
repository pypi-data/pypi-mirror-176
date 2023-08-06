import os
# import time

from halo import Halo
import utilum

from . import utils
from .logger import controlledPrint
from .template import nginxt

class Nginx:
    def __init__(self, NGINX, config):

        self.config = config
        self.FILE_PATH_HERE = NGINX["FILE_PATH_HERE"] # two-deploy folder, mainly [READ]
        self.CWD = NGINX["CWD"] # code repo, mainly [WRITE]
        
        
        # Read Paths
        self.READ_FILE_PATH_HERE = os.path.join(self.FILE_PATH_HERE, NGINX["READ"]["folder"])
        utilum.file.createPath(self.READ_FILE_PATH_HERE)
        
        self.CONF = nginxt.read('conf')
        self.BASH = nginxt.read('sh')
        self.DOCKER = nginxt.read('Dockerfile')

        self.CRT_PATH = os.path.join(self.CWD, 'nginx', NGINX["READ"]["crt"])
        self.KEY_PATH = os.path.join(self.CWD, 'nginx', NGINX["READ"]["key"])

        self.CRT = utilum.file.readFile(self.CRT_PATH)
        self.KEY = utilum.file.readFile(self.KEY_PATH)

        
        # Write Paths
        self.WRITE = os.path.join(self.CWD, NGINX["WRITE"]["folder"])

        self.CONF_WRITE = os.path.join(self.WRITE, NGINX["WRITE"]["conf"])
        self.BASH_WRITE = os.path.join(self.WRITE, NGINX["WRITE"]["bash"])
        self.DOCKER_WRITE = os.path.join(self.WRITE, NGINX["WRITE"]["docker"])

        self.CRT_WRITE = os.path.join(self.WRITE, NGINX["WRITE"]["crt"])
        self.KEY_WRITE = os.path.join(self.WRITE, NGINX["WRITE"]["key"])



    def removeEntities(self):
        utilum.file.removeFile(self.CONF_WRITE)
        utilum.file.removeFile(self.BASH_WRITE)
        utilum.file.removeFile(self.DOCKER_WRITE)
        utilum.file.removeFile(self.CRT_WRITE)
        utilum.file.removeFile(self.KEY_WRITE)
        utilum.file.deleteFolder(self.WRITE)

    def templateRunner(self, port=None):
        utilum.file.createPath(self.WRITE)

        allExternalPorts = self.config.EXTERNAL_PORTS.copy()

        if(port != None and port in allExternalPorts):
            allExternalPorts.remove(port)

        portTemplates = [
            f'server {self.config.DOCKER_HOST}:{portAllowed};' for portAllowed in allExternalPorts]
        portTemplate = "\n".join(portTemplates)

        # print("port: ", port)
        # print("portTemplate: ", portTemplate)

        conf = self.CONF.replace(self.config.SERVER_URLS_TEMPLATE, portTemplate).replace(
            self.config.HOSTNAME_TEMPLATE, self.config.REMOTE_HOSTNAME)
        utilum.file.clearFile(self.CONF_WRITE)
        utilum.file.writeFile(self.CONF_WRITE, conf)

        bash = self.BASH.replace(self.config.NGINX_IMAGE_TEMPLATE, self.config.NGINX_IMAGE_NAME).replace(self.config.NGINX_BASE_TEMPLATE, self.WRITE).replace(
            self.config.DOCKER_TEMPLATE, self.DOCKER_WRITE).replace(self.config.EXTERNAL_PORT_TEMPLATE, str(self.config.EXTERNAL_PORT))
        # print("bash: ", bash)

        docker = self.DOCKER.replace(self.config.REMOTE_HOSTNAME_TEMPLATE, self.config.REMOTE_HOSTNAME)
        # .replace(KEY_PATH_TEMPLATE.replace(WRITE, ""), KEY_PATH).replace(CRT_PATH_TEMPLATE.replace(WRITE, ""), CRT_PATH)

        utilum.file.clearFile(self.BASH_WRITE)
        utilum.file.writeFile(self.BASH_WRITE, bash)

        utilum.file.clearFile(self.DOCKER_WRITE)
        utilum.file.writeFile(self.DOCKER_WRITE, docker)

        utilum.file.clearFile(self.CRT_WRITE)
        utilum.file.writeFile(self.CRT_WRITE, self.CRT)

        utilum.file.clearFile(self.KEY_WRITE)
        utilum.file.writeFile(self.KEY_WRITE, self.KEY)

        containerId = utils.getContainerIdFromPort(self.config.EXTERNAL_PORT)
        print("[Nginx][Start][Port-Internal]", port, containerId)

        action = f"Configuring Nginx for port: {self.config.EXTERNAL_PORT}"
        spinner = Halo(text=action, spinner='dots')
        spinner.start()

        # run build and run command here, after container id existence
        # controlledPrint([len(containerId)], 'len(containerId)', self.config.mode)
        if(len(containerId) == 12):
            # container already exists, so copy bash file inside this container
            CRT_CP_CMD = f"docker cp {self.CRT_PATH} {containerId}:/etc/nginx/conf.d/{self.config.REMOTE_HOSTNAME}.crt"
            KEY_CP_CMD = f"docker cp {self.KEY_PATH} {containerId}:/etc/nginx/conf.d/{self.config.REMOTE_HOSTNAME}.key"

            dockerCp = f"docker cp {self.CONF_WRITE} {containerId}:/etc/nginx/conf.d/default.conf"
            utilum.system.shell(dockerCp)
            utilum.system.shell(CRT_CP_CMD)
            utilum.system.shell(KEY_CP_CMD)

            dockerExec = f"docker exec -it {containerId} nginx -s reload"
            utilum.system.shell(dockerExec)
        else:
            # build new container
            controlledPrint([self.BASH_WRITE], 'self.BASH_WRITE', self.config.mode)
            utilum.system.shell(f"bash '{self.BASH_WRITE}'")
            newContainerId = utils.getContainerIdFromPort(self.config.EXTERNAL_PORT)

            # sleep while port comes up
            instanceStatus = utils.isPortAvailable(self.config.PROTOCOL, self.config.HOSTNAME, self.config.EXTERNAL_PORT)

            controlledPrint([newContainerId, instanceStatus], 'newContainerId,instanceStatus', self.config.mode)
            if(instanceStatus):
                CRT_CP_CMD = f"docker cp {self.CRT_PATH} {newContainerId}:/etc/nginx/conf.d/{self.config.REMOTE_HOSTNAME}.crt"
                KEY_CP_CMD = f"docker cp {self.KEY_PATH} {newContainerId}:/etc/nginx/conf.d/{self.config.REMOTE_HOSTNAME}.key"

                utilum.system.shell(CRT_CP_CMD)
                utilum.system.shell(KEY_CP_CMD)
                pass
            else:
                print()
                print("[Nginx] Failed")
                pass
                #  currently no error handling for failure case currently

        spinner.stop()
        print("[Nginx][End][Port-Internal]", port)
        self.removeEntities()
        return None

    def stopNginxContainer(self):
        containerId = utils.getContainerIdFromPort(self.config.EXTERNAL_PORT)
        if(len(containerId) >= 12):
            utilum.system.shell(f"docker stop {containerId}")
            utilum.system.shell(f"docker rm {containerId}")
        return None

    def runNginxForAllButThisPort(self, port):
        self.templateRunner(port)

    def runNginxForAllPort(self):
        self.templateRunner()


