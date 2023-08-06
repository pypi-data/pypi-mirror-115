from drewsTools.l0 import proxmox
import time
import logging
logger = logging.getLogger(__name__)

def migrateVm(vm, allowedNodes=[], essentialVms=[]):
    Proxmox=proxmox.Proxmox()
    candidateList = getNodeCandidateList(allowedNodes)
    
    candidate=None
    for nodeName in candidateList['candidateList']:
        result=validateVmToCandidate(vm, nodeName, essentialVms)
        if result==1:
            candidate=nodeName
            break
        if result==2:
            logger.info("Candidate node %s for vm %s is good, just need to clear some disk space." % (nodeName, vm['name']))
            continue
            # migrate some VMs off this node
    
    if not candidate:
        logger.warning("No valid node candidate for vm %s" % vm['name'])
        return -1

    logger.info("Migrating %s to %s" % (vm['name'], candidate))
    upid=Proxmox.migrateVm(vm, candidate)
    
    done=False
    while not done:
        for task in Proxmox.getClusterTasks():
            if task['upid'] != upid:
                continue
            if 'endtime' in task:
                logger.info("Migrate is done!")
                done=True
            else:
                logger.info("Migrate still in progress, will retry in 60 seconds.")
                time.sleep(60)


def migrateVmDisksToStorage(vm, targetStorageName):
    Proxmox=proxmox.Proxmox()
    
    logger.info("Migrating vm (%s) disks to storage %s" % (vm['name'], targetStorageName))
    # Check if a migrate task is already in progress
    upid=None
    for task in Proxmox.getClusterTasks():
        if vm['vmid'] == task['id'] and vm['node'] == task['node'] and task['type'] == 'qmmove' and 'endtime' not in task:
            upid=task['upid']

    vmConfig    = Proxmox.getVmConfig(vm)
    bootdisk    = vmConfig['bootdisk']
    storageName = vmConfig[bootdisk].split(":")[0]
    if storageName == targetStorageName:
        return 1

    if not upid:
        upid=Proxmox.migrateVmDisks(vm, targetStorageName, bootdisk)
    
    done=False
    while not done:
        for task in Proxmox.getClusterTasks():
            if task['upid'] != upid:
                continue
            if 'endtime' in task:
                logger.info("Migrate is done!")
                done=True
            else:
                logger.info("Migrate still in progress, will retry in 60 seconds.")
                time.sleep(60)

# returns node stats and candidate list
# {
#     'nodeName' :{
#         'availablecpu': 7.997061127069271, 
#         'maxcpu': 8, 
#         'percentFreecpu': 0.9996326408836589, 
#         'availablemem': 15209676800, 
#         'maxmem': 16649740288,
#         'percentFreemem': 0.913508351296152, 
#         'availabledisk': 25744662528, 
#         'maxdisk': 29194506240, 
#         'percentFreedisk': 0.8818324350602205, 
#         'averageFreePercent': 0.9316578090800105
#     },
#     'candidateList' : ['mostFreeNode', 'notAsFreeNode']
# }
def getNodeCandidateList(allowedNodes=[]):
    Proxmox=proxmox.Proxmox()

    # First get usage stats + percent Free on all + average percent Free per node
    nodeStats={}
    for node in Proxmox.getNodes():
        if node['node'] not in allowedNodes:
            continue
            
        sysType=['cpu','mem','disk']
        percentFreeList=[]
        nodeStats[node['node']] = {}
        for type in sysType:
            nodeStats[node['node']]['available'+type]  = node['max'+type]  - node[type]
            nodeStats[node['node']]['max'+type]  = node['max'+type]
            nodeStats[node['node']]['percentFree'+type]  = (node['max'+type] - node[type]) / node['max'+type]
            percentFreeList.append( nodeStats[node['node']]['percentFree'+type] )
        
        nodeStats[node['node']]['averageFreePercent'] = sum(percentFreeList) / len(percentFreeList)
    
    # Sort candidate list with most Free resources first
    candidateList= list(nodeStats.keys())
    swapped=True
    while swapped:
        swapped=False
        for i in range(len(candidateList) - 1):
            if nodeStats[ candidateList[i] ]['averageFreePercent'] < nodeStats[ candidateList[i + 1] ]['averageFreePercent']:
                candidateList[i], candidateList[i+1] = candidateList[i+1], candidateList[i]
                swapped=True

    nodeStats['candidateList'] = candidateList
    return nodeStats 


# Do some checks to see if we can migrate a VM to this node
def validateVmToCandidate(vm, nodeName, essentialVms=[]):
    Proxmox=proxmox.Proxmox()
    node=None
    for nodeBuff in Proxmox.getNodes():
        if nodeBuff['node'] == nodeName:
            node=nodeBuff
            break

    logger.info('Testing if %s is a valid migrate candidate for %s' % (nodeName, vm['name']))
    if len(essentialVms) < 1:
        essentialVms = [vm['name']]

    #check vm maxmem won't take node over maxmem
    if (node['mem'] + vm['maxmem']) > node['maxmem']:
        logger.info("%s is not a valide node candidate for %s. Memory usage would be too high node mem %s maxmem %s vm maxmem %s." 
            % (node['node'], vm['name'], node['mem'], node['maxmem'], vm['maxmem']))
        return -1

    # Check locallvm has room
    localLvm=None
    for storage in Proxmox.getNodeStorageList(node['node']):
        if storage['storage'] == 'local-lvm':
            localLvm=storage
            break
    if (localLvm['used'] + node['maxdisk']) > localLvm['total']:
        return 2

    return 1