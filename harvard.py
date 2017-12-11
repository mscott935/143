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
        resHosts = [x[0] for x in topo.buildings if x[1] == "R"]
        print(resHosts)
        for host in resHosts:
            links = host.connectionsTo(switch)
            srcLink = links[0][1]
            dstLink = links[0][1]
            if time.hour == 5:
                srcLink.config(**{'bw' : 350, 'loss' : 0})
                dstLink.config(**{'bw' : 350, 'loss' : 0})
            elif time.hour == 17:
                srcLink.config(**{'bw' : 500, 'loss' : 0})
                dstLink.config(**{'bw' : 500, 'loss' : 10})
            else:
                print("Unsupported link update time at time!")
    elif profile == "S":
        sciHosts = [x[0] for x in topo.buildings if x[1] == "S"]
        for hosts in sciHosts:
            links = host.connectionsTo(switch)
            srcLink = links[0][1]
            dstLink = links[0][1]
            if time.hour == 5:
                srcLink.config(**{'bw' : 100, 'loss' : 0})
                dstLink.config(**{'bw' : 100, 'loss' : 0})
            elif time.hour == 13:
                srcLink.config(**{'bw' : 200, 'loss' : 0})
                dstLink.config(**{'bw' : 200, 'loss' : 0})
            elif time.hour == 17:
                srcLink.config(**{'bw' : 300, 'loss' : 0})
                dstLink.config(**{'bw' : 300, 'loss' : 0})
            elif time.hour == 22:
                srcLink.config(**{'bw' : 125, 'loss' : 0})
                dstLink.config(**{'bw' : 125, 'loss' : 0})
            else:
                print("Unsupported link update time at time!")
    else:
        print("Unsupported link update time at time!")

if __name__ == '__main__':
    # Tell mininet to print useful information
    setLogLevel('info')
    simpleTest()