
from syslogoutput import SyslogOutput
import random
import config as config

class Service:

    def __init__(self, name, logfile, hostid):
        self.name = name
        self.logger = SyslogOutput(logfile, hostid)
        if name == "kernel":
            self.pid = 0
        else:
            self.pid = random.randint(100,10000)
        #print("Got a pid of " + str(self.pid))



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



