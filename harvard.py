#!/usr/bin/python
#coding: utf-8

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import irange,dumpNodeConnections
from mininet.log import setLogLevel

class HarvardTopo(Topo):
	'''Create topology that mimics some Harvard locations and buildings, including Leverett House, McKinlock Hall
		(a part of Leverett House), Maxwell Dworkin, and Pierce Hall. Most infrastructure abstracted away.'''
	
	def build(self, **opts):
		switch = self.addSwitch('Pre-Controller')
		mckin = self.addHost('McKinlock')
		lev = self.addHost('Leverett House')
		maxwell = self.addHost('G Tower')
		pierce = self.addHost('Pierce')

		self.addLink(switch, lev)
		self.addLink(lev, mckin)
		self.addLink(switch, maxwell)
		self.addLink(switch, pierce)

	def addBuilding(self, host):
		self.addLink(switch, host)

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

if __name__ == '__main__':
	# Tell mininet to print useful information
	setLogLevel('info')
	simpleTest()
