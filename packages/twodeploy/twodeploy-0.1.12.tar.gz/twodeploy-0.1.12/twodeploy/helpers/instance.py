import utilum

def getAttributes(self, EXTERNAL_PORTS):
    PORTS = []
    CONTAINERS = []
    TWO_MAP = dict()

    for EXTERNAL_PORT in EXTERNAL_PORTS:
        
        portCmd = 'docker ps -f "expose=EXTERNAL_PORT_HERE" -q'.replace(
            "EXTERNAL_PORT_HERE", str(EXTERNAL_PORT))
        containerId = utilum.system.shellRead(
            portCmd)[0].decode("utf-8").replace("\n", "")

        # controlledPrint([containerId, EXTERNAL_PORT], 'EXTERNAL_PORT', self.config.mode)
        if(len(containerId) == 12):
            PORTS.append(EXTERNAL_PORT)
            CONTAINERS.append(containerId)
            TWO_MAP[EXTERNAL_PORT] = containerId
            TWO_MAP[containerId] = EXTERNAL_PORT

    return PORTS, CONTAINERS, TWO_MAP

# docker build -t two-deploy-instance-1282 .
# docker run --restart=on-failure -d -p 1281:1281 two-deploy-instance-1281
# docker run --restart=on-failure -d -p 1282:1282 two-deploy-instance-1282