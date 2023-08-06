import os

FRAMEWORKS = {
    "nextjs": "nextjs",
    "reactjs": "reactjs",
    "nodejs": "nodejs",
}


class Config:
    def __init__(self, rootName="two-deploy", remoteHostname="instance.two-deploy.com", externalPort=1288, externalPorts=[1281, 1282], framework = 'reactjs'):
        self.mode = 'development'
        # self.mode = 'production'
        self.ROOT_NAME = rootName
        self.REMOTE_HOSTNAME = remoteHostname
        self.IMAGE_NAME = f"{self.ROOT_NAME}-instance"
        
        self.BKP_IMAGE_NAME = f"{self.IMAGE_NAME}-backup"
        self.NGINX_IMAGE_NAME = f"{self.IMAGE_NAME}-nginx"
        self.framework = framework

        # Nginx External Port
        self.EXTERNAL_PORT = externalPort  # single, for all reverse-proxy hits
        # multiple, for running multiple instances of repo/code
        self.EXTERNAL_PORTS = externalPorts

        # CWD, code-repo
        self.CWD = os.getcwd()
        self.PON_PATH = os.path.join(self.CWD, "ponServer.sh")      

        # Nginx Paths (only on client side)

        self.NGINX = {
            "CWD": self.CWD,
            "READ": {
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
