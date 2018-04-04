
from syslogoutput import SyslogOutput
import random
import config as config

class Service:

    pids = list(range(100)) # In use PIDs. Usually the first 100 or so are being used.
    maxpid = 65535 # highest pid we can assign.
    lastpid = 0 # The last allocated pid.

    def __init__(self, name, logger):
        self.name = name
        self.logger = logger
        if name == "kernel":
            self.pid = 0
        else:
            self.pid = self.getPID()
        #print("Got a pid of " + str(self.pid))

    def getPID(self):
        Service.lastpid += 1
        while Service.lastpid in Service.pids:
            Service.lastpid += 1
        Service.pids.append(Service.lastpid)
        return Service.lastpid


    def releasePID(self, pid):
        Service.pids.remove(pid)
        return True



#class KernelService(Service):

class SSHService(Service):

    def connect(self, username, login_success, srcIP, srcPort):
        waitseconds = 1

        if login_success == True:
            logmessage = "Accepted keyboard-interactive/pam for {} from {} port {} ssh2".format(str(username), str(srcIP), str(srcPort))
            self.logger.logmessage(self.name, self.pid, logmessage)
            logmessage = "pam_unix(sshd:session): session opened for user {} by (uid=0)".format(str(username))
            self.logger.logmessage(self.name, self.pid, logmessage)
        else:
            logmessage = "pam_unix(sshd:auth): authentication failure; logname= uid=0 euid=0 tty=ssh ruser= rhost={}  user={}".format(str(srcIP), str(username))
            self.logger.logmessage(self.name, self.pid, logmessage)
            # For now this won't handle the multiple tries per open session and "more authentication failures errors"
            # messages that SSH usually generates.
            logmessage = "Failed password for {} from {} port {} ssh2".format(str(username), str(srcIP), str(srcPort))
            self.logger.logmessage(self.name, self.pid, logmessage)
            waitseconds = 3  # How long to wait before next attempt.

        return waitseconds

    def disconnect(self, username, srcIP, srcPort):
        logmessage = "Disconnected from user {} {} port {}".format(str(username), str(srcIP), str(srcPort))
        self.logger.logmessage(self.name, self.pid, logmessage)
        return True



#class CronService(Service):



