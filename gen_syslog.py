#!/usr/bin/env python3

# This is more of a mental exercise than a production program.
# I wasn't sure how this would work so I had to try something
# to explore the concepts.

# After this I'll need to do a proper design of the interfaces
# and program flow and write something from scratch.


import re
import random
from netaddr import IPAddress, IPSet, IPNetwork
import datetime

# Custom modules
from syslogoutput import SyslogOutput
from service import Service, SSHService
from actor import Actor
from schedule import Schedule
import globalvars

# Later we'll need to write some code to verify the config is valid.
import config as config

daynames = [
    'Monday',
    'Tuesday',
    'Wednesday',
    'Thursday',
    'Friday',
    'Saturday',
    'Sunday'
]

# Taken and augmented from Kay's apache_log_simulator.
# Good candidate for a unified module.
def random_ipaddr(lowerbound, upperbound):                    
    # 2 ^ 32 = 4294967296, subtract one to get 4294967295                       
    addr = IPAddress(random.randint(lowerbound, upperbound))                             
    invalid_ips = IPSet()
    for net in ( #IPv4 reserved blocks.
                '0.0.0.0/8',
                '10.0.0.0/8',
                '127.0.0.0/8',
                '172.16.0.0/12',
                '192.168.0.0/16',
                '224.0.0.0/4',
                '240.0.0.0/4',
                # IPv6 reserved blocks. Taken from https://en.wikipedia.org/wiki/Reserved_IP_addresses
                '::/128',
                '::1/128',
                '::ffff:0:0/96',
                '64:ff9b::/96',
                '100::/64',
#                '2001::/32', # Including this one causes it to deadloop for unknown reasons.
                '2001:10::/28',
                '2001:20::/28',
                '2001:db8::/32',
                '2002::/16',
                'fc00::/7',
                'fe80::/10',
                'ff00::/8'
                ):
        invalid_ips.add(IPNetwork(net))

    while addr in invalid_ips:
        addr = IPAddress(random.randint(lowerbound, upperbound))
    return addr


# This global is accessed by the SyslogOutput class. It's up to us to increment it.
globalvars.epochtime = config.startepoch

# Right now this software only generates sshd logs.
sshd = SSHService('sshd', config.logfile, config.hostname)

# A list of all the actor objects in the simulation.
actorqueue = []

for actorkey in list(config.actors.keys()):
    actorconfig = config.actors[actorkey]
    usernames = actorconfig['usernames']
    success = actorconfig['success']
    intentions = actorconfig['intentions']
    scheduleconfig = actorconfig['schedule']
    services = actorconfig['services']
    # this is an optional config value that has a default of 3.
    actormaxattempts = 3
    if 'maxattempts' in actorconfig:
        actormaxattempts = actorconfig['maxattempts']

    for i in range(int(config.actors[actorkey]['count'])):
        # The downside of this implementation is it doesn't make it easy to configure
        # Multiple user instances coming from a single IP address by simply increasing 'count'.

        # Determine a username from the list. Choosen 1 in turn, not randomly.
        username = usernames[i % len(usernames)]
        # Determine IP address. For now let's not worry about excluded blocks.
        ipnet = IPNetwork(actorconfig['address-block'])
        ipnetlow = int(ipnet.network) + 1 # Allowing router IP.
        ipnethigh = int(ipnet.broadcast) - 1
        actorip = IPAddress(random_ipaddr(ipnetlow, ipnethigh))

        # Just use the first schedule in the list for now.
        schedule = Schedule(scheduleconfig[0], config.startepoch, config.endepoch)

        actorobj = Actor(actorkey, actorip, intentions, username, success, schedule, actormaxattempts)
#        print("Times for {} are {} to {}".format(str(actorobj.username),
#                                               str(actorobj.schedule.day_starttime),
#                                               str(actorobj.schedule.day_endtime)))
        
        actorqueue.append(actorobj)

for i in range(1,86400*config.days):
    dt = datetime.datetime.fromtimestamp(globalvars.epochtime)
    if dt.hour == 0 and dt.minute == 0 and dt.second == 0:
        print("== {:04}-{:02}-{:02} {:02}:{:02}:{:02} ({}) ==".format(
                        dt.year, dt.month, dt.day, dt.hour, dt.minute,
                        dt.second, daynames[dt.weekday()]))

    for thisactor in actorqueue:

        # SCHEDULE: Check if we need to open a connection based on the time.
        if thisactor.schedule.epochtimeInSchedule(globalvars.epochtime) == True:

#            print("{:8} {}".format(thisactor.username, thisactor.ip))
#            print("Actor {} active sessions: {} Attempts: ({} / {})".format(
#                                                str(thisactor.username),
#                                                str(thisactor.getActiveConnections()), 
#                                                str(thisactor.attempts),
#                                                str(thisactor.maxattempts)))

            if thisactor.getActiveConnections() == 0:
                # For now, we'll only deal with one successful connection at a time.
                if thisactor.getAttempts() < thisactor.getMaxAttempts():
                    # Won't allow a normal user to make a few mistakes before success yet.
                    randomSrcPort = random.randint(1024, 65535) # Later make this actor attribute
                    waittime = sshd.connect(thisactor.username,
                                 thisactor.success,
                                 thisactor.ip,
                                 randomSrcPort)

                    if thisactor.success == True: # If only it were this easy.
                        thisactor.incrementActiveConnections()
                        endofsessionepoch = thisactor.schedule.getEndOfDayTime(globalvars.epochtime)
                        sshsession = {'username': thisactor.username,
                                      'srcPort': randomSrcPort,
                                      'endtime': endofsessionepoch}
                        thisactor.newSession(sshsession)
           
                    elif thisactor.success == False:
                        # This implies that attempts means failed attempts.
                        thisactor.incrementAttempts()
                        # How do I handle the waittime now?
                        # Maybe a next_try epoch variable in actor?

        # It's not in schedule, so....    
        # Check if there are active connections to close
        elif thisactor.getActiveConnections() > 0:
            if len(thisactor.opensessions) > 0:
                for sshsession in thisactor.opensessions:
                    if sshsession['endtime'] <= globalvars.epochtime:
                        sshd.disconnect(thisactor.username,
                                        thisactor.ip,
                                        sshsession['srcPort'])
                        thisactor.deleteSession(sshsession['srcPort'], sshsession['endtime'])
                        thisactor.schedule.setDayTimes() # Generate a new set of start-end of day random times for the next day.

    
    globalvars.epochtime += 1 # By the minute

    


del sshd
