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
        "Init."
        # Buildings are stored in a dict in the form {Name: (host, profile)}
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

    def getBuildings(self):
        return self.buildings

def updateLinks(profile, net, topo):
    "Update link bandwidth based on time of day and building profile."
    time = datetime.datetime.now()
    switch = net.get('s1')
    buildings = topo.getBuildings()
    if profile == "R":
        # Gather all residential hosts
        resHosts = [buildings[x][0] for x in buildings if buildings[x][1] == "R"]
        for hostname in resHosts:
            host = net.get(hostname)
            links = host.connectionsTo(switch)
            srcLink = links[0][1]
            dstLink = links[0][1]
            if time.hour >= 5 and time.hour < 17:
                srcLink.config(**{'bw' : 350, 'loss' : 0})
                dstLink.config(**{'bw' : 350, 'loss' : 0})
            elif time.hour >= 17 or time.hour < 5:
                srcLink.config(**{'bw' : 500, 'loss' : 0})
                dstLink.config(**{'bw' : 500, 'loss' : 10})
                print("Time 17-5 done!")
            else:
                print("Unsupported link update time at time" + time.hour + "!")
    elif profile == "S":
        sciHosts = [buildings[x][0] for x in buildings if buildings[x][1] == "S"]
        for hostname in sciHosts:
            host = net.get(hostname)
            links = host.connectionsTo(switch)
            srcLink = links[0][1]
            dstLink = links[0][1]
            if time.hour >= 5 and time.hour < 13:
                srcLink.config(**{'bw' : 200, 'loss' : 0})
                dstLink.config(**{'bw' : 200, 'loss' : 0})
            elif time.hour >= 13 and time.hour < 17:
                srcLink.config(**{'bw' : 200, 'loss' : 0})
                dstLink.config(**{'bw' : 200, 'loss' : 0})
            elif time.hour >= 17 and time.hour < 22:
                srcLink.config(**{'bw' : 300, 'loss' : 0})
                dstLink.config(**{'bw' : 300, 'loss' : 0})
            elif time.hour >= 22 or time.hour < 5:
                srcLink.config(**{'bw' : 100, 'loss' : 0})
                dstLink.config(**{'bw' : 100, 'loss' : 0})
            else:
                print("Unsupported link update time at time" + time.hour + "!")
    else:
        print("Unsupported building profile" + profile + "!")

'''def updateLinks(profile, net, topo):
    "Update link bandwidth based on time of day and building profile."
    time = datetime.datetime.now()
    switch = net.get('s1')
    buildings = topo.getBuildings()
    if profile == "R":
        # Gather all residential hosts
        resHosts = [buildings[x][0] for x in buildings if buildings[x][1] == "R"]
        for hostname in resHosts:
            host = net.get(hostname)
            links = host.connectionsTo(switch)
            intf = host.intf()
            if time.hour >= 5 and time.hour < 17:
                intf.config(bw = 350)
            elif time.hour >= 17 or time.hour < 5:
                intf.config(bw = 500)
                print("Time 17-5 done!")
            else:
                print("Unsupported link update time at time" + time.hour + "!")
    elif profile == "S":
        sciHosts = [buildings[x][0] for x in buildings if buildings[x][1] == "S"]
        for hostname in sciHosts:
            host = net.get(hostname)
            links = host.connectionsTo(switch)
            srcLink = links[0][1]
            dstLink = links[0][1]
            if time.hour >= 5 and time.hour < 13:
                intf.config(bw = 500)
            elif time.hour >= 13 and time.hour < 17:
                intf.config(bw = 500)
            elif time.hour >= 17 and time.hour < 22:
                intf.config(bw = 500)
            elif time.hour >= 22 or time.hour < 5:
                intf.config(bw = 500)
            else:
                print("Unsupported link update time at time" + time.hour + "!")
    else:
        print("Unsupported building profile" + profile + "!")'''

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

if __name__ == '__main__':
    # Tell mininet to print useful information
    setLogLevel('info')
    runNetwork()

# {'Leverett': ('h1', 'R'), 'Pierce': ('h3', 'S'), 'Maxwell Dworkin': ('h2', 'S')}
# [ buildings[x][0] if ]