from proxmoxer import ProxmoxAPI
from drewsTools.l0 import functions
import logging
logger = logging.getLogger(__name__)


proxmoxApiCreds = "secrets/proxmoxApi.json"

# Proxmox API https://pve.proxmox.com/pve-docs/api-viewer/index.html
class Proxmox():
    def __init__(self, **kwargs):
        creds = functions.getCreds(filename=proxmoxApiCreds)
        try:
            proxmoxHost = creds['proxmoxHost']
            user        = creds['user']
            secret      = creds['pass']
        except KeyError:
            proxmoxHost = kwargs.get("proxmoxHost", "pve")
            user        = kwargs.get("user", "root@pam")
            secret      = kwargs.get("secret")

        self.connection = ProxmoxAPI(proxmoxHost, user=user,
                            password=secret, verify_ssl=False)
    ######################
    # Cluster
    def getClusterTasks(self):
        return self.connection.cluster.tasks.get()

    ######################
    # Nodes
    def getNodes(self, node=""):
        return self.connection.nodes.get(node)

    def getNodeStatus(self, nodeName):
        node = self.connection.nodes(nodeName)
        return node.status()
    
    # reboot or shutdown
    def setNodeStatus(self, nodeName, status):
        node = self.connection.nodes(nodeName)
        print("Rebooting pve node %s" % nodeName)
        return node.status.post(command=status)

    ######################$
    # Nodes -> Storage
    def getNodeStorageList(self, nodeName, storageName=""):
        return self.connection.nodes(nodeName).storage.get(storageName)


    #######################
    # VMs

    def getVms(self):
        return self.connection.cluster.resources.get(type='vm')

    def getVmConfig(self, vm):
        return self.connection.nodes(vm['node']).qemu(vm['vmid']).config.get()

    # Status types:
    #   reboot reset resume shudown start stop suspend
    def setVmPowerStatus(self, node, vmId, status):
        return self.connection.nodes(node).qemu(vmId).status(status).post()

    def getVmPowerStatus(self, node, vmId):
        return self.connection.nodes(node).qemu(vmId).status.current.get()

    def migrateVm(self, vm, targetNodeName):
        params={
            'target':targetNodeName,
            'online':1,
            'with-local-disks':1,
        }
        return self.connection.nodes(vm['node']).qemu(vm['vmid']).migrate.post(**params)
    
    def migrateVmDisks(self, vm, targetStorageName, diskType):
        return self.connection.nodes(vm['node']).qemu(vm['vmid']).move_disk.post(storage=targetStorageName, disk=diskType, delete=1)
