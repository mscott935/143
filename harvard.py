#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import irange,dumpNodeConnections
from mininet.log import setLogLevel
from mininet.link import TCLink, TCIntf
from mininet.cli import CLI
import schedule, time, datetime

class HarvardTopo(Topo):
    '''Create topology that mimics some Harvard locations and buildings, including Leverett House,
        Maxwell Dworkin, and Pierce Hall. Most infrastructure abstracted away.'''

    def build(self):
        "Init"
        # Buildings are stored in a dict in the form {Name: (host, profile)}
        self.buildings = {}
        # Initialize switches and default hosts.
        switch = self.addSwitch('s1')
        lev = self.addHost('h1')
        maxwell = self.addHost('h2')
        pierce = self.addHost('h3')

        self.buildings['Leverett'] = (lev, "R")
        self.buildings['Maxwell Dworkin'] = (maxwell, "S")
        self.buildings['Pierce'] = (pierce, "S")

        self.addLink(switch, lev)
        self.addLink(switch, maxwell)
        self.addLink(switch, pierce)

    def getBuildings(self):
        return self.buildings

def updateLinks(profile, net, topo, time=datetime.datetime.now()):
    "Update link bandwidth based on time of day and building profile"
    switch = net.get('s1')
    buildings = topo.getBuildings()
    print "Updating " + profile + "-type host links..."
    if profile == "R":
        # Gather all residential hosts
        resHosts = [buildings[x][0] for x in buildings if buildings[x][1] == "R"]
        for hostname in resHosts:
            host = net.get(hostname)
            # Name source and destination links
            links = host.connectionsTo(switch)
            srcLink = links[0][1]
            dstLink = links[0][1]
            # Downtime profile (5am - 5pm)
            if time.hour >= 5 and time.hour < 17:
                srcLink.config(**{'bw' : 350, 'loss' : 0})
                dstLink.config(**{'bw' : 350, 'loss' : 0})
            # Uptime profile (5pm - 5am)
            elif time.hour >= 17 or time.hour < 5:
                srcLink.config(**{'bw' : 500, 'loss' : 0})
                dstLink.config(**{'bw' : 500, 'loss' : 10})
            else:
                print "Unsupported link update time at time " + time.hour + "!"
    elif profile == "S":
        # Gather all STEM lab hosts
        sciHosts = [buildings[x][0] for x in buildings if buildings[x][1] == "S"]
        for hostname in sciHosts:
            host = net.get(hostname)
            # Name source and destination links
            links = host.connectionsTo(switch)
            srcLink = links[0][1]
            dstLink = links[0][1]
            # Peak 1 profile (5am - 1pm)
            if time.hour >= 5 and time.hour < 13:
                srcLink.config(**{'bw' : 200, 'loss' : 0})
                dstLink.config(**{'bw' : 200, 'loss' : 0})
            # Peak 2 profile (1pm - 5pm)
            elif time.hour >= 13 and time.hour < 17:
                srcLink.config(**{'bw' : 300, 'loss' : 0})
                dstLink.config(**{'bw' : 300, 'loss' : 0})
            # Descent profile (5pm - 10pm)
            elif time.hour >= 17 and time.hour < 22:
                srcLink.config(**{'bw' : 125, 'loss' : 0})
                dstLink.config(**{'bw' : 125, 'loss' : 0})
            # Downtime profile (10pm - 5am)
            elif time.hour >= 22 or time.hour < 5:
                srcLink.config(**{'bw' : 100, 'loss' : 0})
                dstLink.config(**{'bw' : 100, 'loss' : 0})
            else:
                print "Unsupported link update time at time " + time.hour + "!"
    else:
        print "Unsupported building profile " + profile + "!"
    print profile + "-Type building links updated!"

def runNetwork():
    topo = HarvardTopo()
    net = Mininet(topo, link=TCLink)
    net.start()
    updateLinks("R", net, topo)
    updateLinks("S", net, topo)
    schedule.every().day.at("5:00").do(updateLinks, "R", net, topo)
    schedule.every().day.at("5:00").do(updateLinks, "S", net, topo)
    schedule.every().day.at("13:00").do(updateLinks, "S", net, topo)
    schedule.every().day.at("17:00").do(updateLinks, "R", net, topo)
    schedule.every().day.at("17:00").do(updateLinks, "S", net, topo)
    schedule.every().day.at("22:00").do(updateLinks, "S", net, topo)
    CLI(net)

def updateTest():
    midnight = datetime.datetime(2017, 1, 1, 0, 0, 0) # 00:00 Jan 1, 2017
    fiveam = datetime.datetime(2017, 1, 1, 5, 0, 0) # 05:00 Jan 1, 2017
    onepm = datetime.datetime(2017, 1, 1, 13, 0, 0) # 13:00 Jan 1, 2017
    fivepm = datetime.datetime(2017, 1, 1, 17, 0, 0) # 17:00 Jan 1, 2017
    topo = HarvardTopo()
    net = Mininet(topo, link=TCLink)
    net.start()

    # Midnight test
    print "*** EXECUTING MIDNIGHT TEST ***"
    updateLinks("R", net, topo, midnight)
    updateLinks("S", net, topo, midnight)
    net.iperf()
    time.sleep(5)

    # 5am test
    print "*** EXECUTING 5AM TEST ***"
    updateLinks("R", net, topo, fiveam)
    updateLinks("S", net, topo, fiveam)
    net.iperf()
    time.sleep(5)

    # 1pm test
    print "*** EXECUTING 1PM TEST ***"
    updateLinks("R", net, topo, onepm)
    updateLinks("S", net, topo, onepm)
    net.iperf()
    time.sleep(5)

    # 5pm test
    print "*** EXECUTING 5PM TEST ***"
    updateLinks("R", net, topo, fivepm)
    updateLinks("S", net, topo, fivepm)
    net.iperf()
    time.sleep(5)

    net.stop()

if __name__ == '__main__':
    # Tell mininet to print useful information
    setLogLevel('info')
    updateTest()
    runNetwork()