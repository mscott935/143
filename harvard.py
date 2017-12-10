#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import irange,dumpNodeConnections
from mininet.log import setLogLevel
import sched, datetime, time

s = sched.scheduler(time.time, time.sleep)
profileR1 = dict(bw = 500, delay='5ms', loss = 10)
profileR2 = dict(bw = 350, delay='5ms', loss = 0)
profileS1 = dict(bw = 100, delay ='5ms', loss = 0)
profileS2 = dict(bw = 200, delay = '5ms', loss = 0)
profileS3 = dict(bw = 300, delay = '5ms', loss = 10)
profileS4 = dict(bw = 125, delay = '5ms', loss = 10)

class HarvardTopo(Topo):
    '''Create topology that mimics some Harvard locations and buildings, including Leverett House,
        Maxwell Dworkin, and Pierce Hall. Most infrastructure abstracted away.'''

    def build(self):
        self.buildings = {}
        # Initialize switches and default hosts. Switch is an instance variable for reference in other methods
        self.switch = self.addSwitch('s1')
        lev = self.addHost('h1')
        maxwell = self.addHost('h2')
        pierce = self.addHost('h3')

        self.buildings['Leverett'] = (lev, "R")
        self.buildings['Maxwell Dworkin'] = (maxwell, "S")
        self.buildings['Pierce'] = (pierce, "S")

        self.addLink(self.switch, lev)
        self.addLink(self.switch, maxwell)
        self.addLink(self.switch, pierce)

    def addBuilding(self, name, **opts):
        host = self.addHost(name)
        self.buildings[name] = host
        self.addLink(self.switch, host, **opts)

def simpleTest():
    "Create and test a simple network"
    print "Running simple test"
    topo = HarvardTopo()
    net = Mininet(topo)
    net.start()
    print "Dumping host connections"
    dumpNodeConnections(net.hosts)
    print "Testing network connectivity"
    net.pingAll()
    net.stop()

def updateLinks(profile, net, topo):
    "Update link bandwidth based on time of day and building profile."
    time = datetime.datetime.now()
    switch = net.get('s1')
    if profile == "R":
        # Gather all residential hosts
        resHosts = []
        for i, building in enumerate(topo.buildings):
            if building[i][1] == "R":
                resHosts.append(building[i][0])
        print(resHosts)
        # Downtime hours
        if time.hour > 5 && time.hour < 17:
            for host in resHosts:
                delLinkBetween(host, switch)
                addLink(host, switch, **profileR2)
        # Uptime hours
        else:
            for host in resHosts:
                delLinkBetween(host, switch)
                addLink(host, switch, **profileR1)
    elif profile == "S":
        sciHosts = []
        for i, building in enumerate(topo.buildings):
            if building[i][1] == "S":
                sciHosts.append(building[i][0])
        print(resHosts)
        if time.hour > 5 && time.hour < 13:
            for host in sciHosts:
                delLinkBetween(host, switch)
                addLink(host, switch, **profileS2)
        elif time.hour > 13 and time.hour < 17:
            for host in sciHosts:
                delLinkBetween(host, switch)
                addLink(host, switch, **profileS3)
        elif time.hour > 17 and time.hour < 22:
            for host in sciHosts:
                delLinkBetween(host, switch)
                addLink(host, switch, **profileS4)
        else:
            for host in sciHosts:
                delLinkBetween(host, switch)
                addLink(host, switch, **profileS1)
    else:
        print(f"No profiles exist for a {profile} type building!")

if __name__ == '__main__':
    # Tell mininet to print useful information
    setLogLevel('info')
    simpleTest()
    addTest()