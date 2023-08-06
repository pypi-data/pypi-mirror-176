import os

FRAMEWORKS = {
    "nextjs": "nextjs",
    "reactjs": "reactjs",
}


class Config:
    def __init__(self, rootName="two-deploy", remoteHostname="instance.two-deploy.com", externalPort=1288, externalPorts=[1281, 1282], framework = 'reactjs'):
        self.mode = 'development'
        # self.mode = 'production'
        self.ROOT_NAME = rootName
        self.REMOTE_HOSTNAME = remoteHostname
        self.IMAGE_NAME = f"{self.ROOT_NAME}-instance"
        self.NGINX_IMAGE_NAME = f"{self.IMAGE_NAME}-nginx"
        self.framework = framework

        # Nginx External Port
        self.EXTERNAL_PORT = externalPort  # single, for all reverse-proxy hits
        # multiple, for running multiple instances of repo/code
        self.EXTERNAL_PORTS = externalPorts

        # CWD, code-repo
        self.CWD = os.getcwd()

        # Base Path, two-deploy folder
        self.FILE_PATH_HERE = os.path.dirname(os.path.abspath(__file__))
        self.APP_TEMPLATE_PATH = os.path.join(self.FILE_PATH_HERE, "template")

        # Dockerfile paths
        self.DOCKER_TEMPLATE_BASE_PATH = os.path.join(
            self.APP_TEMPLATE_PATH, "Dockerfile")
        
        
        self.DOCKER_TEMPLATE_PATH = os.path.join(self.DOCKER_TEMPLATE_BASE_PATH, FRAMEWORKS[self.framework])
        
        self.DOCKER_BUILD_CHECK_TEMPLATE_BASE_PATH = os.path.join(
            self.APP_TEMPLATE_PATH, "Build")
        self.DOCKER_BUILD_CHECK_TEMPLATE_PATH = os.path.join(self.DOCKER_BUILD_CHECK_TEMPLATE_BASE_PATH, FRAMEWORKS[self.framework])


        self.PON_TEMPLATE_PATH = os.path.join(
            self.APP_TEMPLATE_PATH, "Production", FRAMEWORKS[self.framework]+".sh")
        self.PON_PATH = os.path.join(self.CWD, "ponServer.sh")


        # Nginx Paths
        self.NGINX_CONF_FILE = os.path.join(
            self.FILE_PATH_HERE, "nginx", "nginx.conf")
        self.NGINX_BASH_FILE = os.path.join(
            self.FILE_PATH_HERE, "nginx", "nginx.sh")
        self.NGINX_DOCKER_FILE = os.path.join(
            self.FILE_PATH_HERE, "nginx", "Dockerfile")

        self.NGINX = {
            "CWD": self.CWD,
            "FILE_PATH_HERE": self.FILE_PATH_HERE,
            "READ": {
                "folder": "nginx/",
                "conf": "nginx.conf",
                "bash": "nginx.sh",
                "docker": "Dockerfile",
                "crt": f"{self.REMOTE_HOSTNAME}.crt",
                "key": f"{self.REMOTE_HOSTNAME}.key",
            },
            "WRITE": {
                "folder": "nginx.temp/",
                "conf": "nginx.conf",
                "bash": "nginx.sh",
                "docker": "Dockerfile",
                "crt": f"{self.REMOTE_HOSTNAME}.crt",
                "key": f"{self.REMOTE_HOSTNAME}.key",
            }
        }

        self.PROTOCOL = "http"
        self.HOSTNAME = "localhost"
        self.DOCKER_HOST = "172.17.0.1"
        self.PORT_TEMPLATE = "PORT_HERE"

        # TBDS
        self.NGINX_IMAGE_TEMPLATE = "NGINX_IMAGE_NAME_HERE"
        self.SERVER_URLS_TEMPLATE = "SERVER_URLS_HERE"
        self.EXTERNAL_PORT_TEMPLATE = "EXTERNAL_PORT_HERE"
        self.HOSTNAME_TEMPLATE = "HOSTNAME_HERE"

        self.NGINX_BASE_TEMPLATE = "NGINX_BASE_HERE"
        self.DOCKER_TEMPLATE = "DOCKER_PATH_HERE"

        self.REMOTE_HOSTNAME_TEMPLATE = "REMOTE_HOSTNAME_HERE"
        self.KEY_PATH_TEMPLATE = "KEY_PATH_HERE"
        self.CRT_PATH_TEMPLATE = "CRT_PATH_HERE"

        self.MAX_GET_RETRY = 160  # n times # 60 default value
        self.GET_WAIT_TIME = 1  # second
