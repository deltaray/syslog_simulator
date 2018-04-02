
import random

from netaddr import IPAddress, IPSet, IPNetwork
import config as config


class Actor:
    def __init__(self, name, ip, intention, username, success, schedule, maxattempts):
        self.name = name
        self.ip = ip
        self.intention = intention
        self.username = username
        self.success = success
        self.schedule = schedule
        self.maxattempts = maxattempts # If set, the total number of connection failures allowed before stopping altogether
        self.attempts = 0 # Current count of how many connection attempts have been made.
        self.activeconnections = 0
        self.opensessions = []

        if isinstance(maxattempts, str):
            if maxattempts.find("-") >= 0:
                #print("Found - in maxattempts for {}".format(str(username)))
                (low, high) = maxattempts.split("-")
                #print("low: {} high: {}".format(low, high))
                self.maxattempts = int(random.randint(int(low), int(high)))
            else:
                self.maxattempts = int(maxattempts)
        

    def getMaxAttempts(self):
        return self.maxattempts

    def setMaxAttempts(self, maxattempts):
        self.maxattempts = maxattempts

    def getAttempts(self):
        return self.attempts

    def incrementAttempts(self):  # This would never go down, the object would just be destroyed
        self.attempts += 1

    def getActiveConnections(self):
        return self.activeconnections

    def incrementActiveConnections(self):
        self.activeconnections += 1

    def decrementActiveConnections(self):
        self.activeconnections -= 1

    def newSession(self, session):
        self.opensessions.append(session)

    def deleteSession(self, srcPort, endtime): # Uses the srcPort of the session for this actor. Ideally unique.
        index = 0
        for session in self.opensessions:
            if session['srcPort'] == srcPort and session['endtime'] == endtime:
                #print("Deleting sessions of len {} for {} with index {}".format(str(len(self.opensessions)), str(self.username), str(index)))
                del self.opensessions[index]
                #print("Len of sessions is now {}".format(str(len(self.opensessions))))
                self.decrementActiveConnections()
                #print("activeconnections for this user is now {}".format(str(self.activeconnections)))
                return True
            index += 1


