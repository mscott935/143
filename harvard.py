#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import irange,dumpNodeConnections
from mininet.log import setLogLevel
import sched, datetime, time

s = sched.scheduler(time.time, time.sleep)

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

        self.buildings['h1'] = lev
        self.buildings['h2'] = maxwell
        self.buildings['h3'] = pierce

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

def addTest():
    print "Running add test"
    topo = HarvardTopo()
    topo.addBuilding("Leverett")
    net = Mininet(topo)
    net.start()
    print "Dumping host connections"
    dumpNodeConnections(net.hosts)
    print "Testing network connectivity"
    net.pingAll()
    net.stop()

def bump():
    "Increase bandwidth by small, predetermined amount"
    # TODO

def updateLinks(profile):
    "Update link bandwidth based on time of day and building profile."
    time = datetime.datetime.now()
    if profile == "R":
        if time.hour > 5 && time.hour < 17:
            # Update links to downtime bandwidth
        else:
            # Update links to uptime bandwidth
    elif profile == "S":
        # TODO

def runNetwork():
    topo = HarvardTopo()
    net = Mininet(topo)
    net.start()


if __name__ == '__main__':
    # Tell mininet to print useful information
    setLogLevel('info')
    simpleTest()
    addTest()