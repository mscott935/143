#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import irange,dumpNodeConnections
from mininet.log import setLogLevel

class HarvardTopo(Topo):
    '''Create topology that mimics some Harvard locations and buildings, including Leverett House,
        Maxwell Dworkin, and Pierce Hall. Most infrastructure abstracted away.'''

    def __init__(self, **opts):

        Topo.__init__(self, **opts)

        self.switch = self.addSwitch('s1')
        lev = self.addHost('h1')
        maxwell = self.addHost('h2')
        pierce = self.addHost('h3')

        self.addLink(self.switch, lev)
        self.addLink(self.switch, maxwell)
        self.addLink(self.switch, pierce)

    def addBuilding(self, name, **opts):
        host = self.addHost(name)
        self.addLink(self.switch, host, **opts)

    '''def removeBuilding(self, name):
        self.delLinkBetween(switch, host)
        self.delnode(host, nodes = self.hosts)

    def updateLink(self, host, linkopts):
        self.delLinkBetween(switch, host)
        self.addLink(switch, host, **linkopts)'''


def simpleTest():
    "Create and test a simple network"
    topo = HarvardTopo()
    net = Mininet(topo)
    net.start()
    print "Dumping host connections"
    dumpNodeConnections(net.hosts)
    print "Testing network connectivity"
    net.pingAll()
    net.stop()

def addTest():
    topo = HarvardTopo()
    topo.addBuilding("Leverett")
    net = Mininet(topo)
    net.start()
    print "Dumping host connections"
    dumpNodeConnections(net.hosts)
    print "Testing network connectivity"
    net.pingAll()
    net.stop()

if __name__ == '__main__':
    # Tell mininet to print useful information
    setLogLevel('info')
    simpleTest()
    addTest()