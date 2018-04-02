
from datetime import date, time, datetime, timedelta
import globalvars

# For now we're not handling facilities and levels

class SyslogOutput:
    shortmonths = ['','Jan', 'Feb', 'Mar', 'Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

    def __init__(self, logfile, hostid):
        self.logfile = logfile
        self.hostid = hostid
        self.timestamp = 0 # The syslog timestampe that we'll generate
        self.service = ""
        self.pid = 0
        
        # Open the log file here so we're not opening and closing it all the time.
        self.log = open(self.logfile, "a", 1)  # Write line buffered.

    def logmessage(self, service, pid, message):
        curtime = datetime.fromtimestamp(globalvars.epochtime)

        if service == "kernel":
            servicepidstring = "kernel"
        else:
            servicepidstring = '{}[{}]'.format(service, pid)

        # Use the typical default syslog format for now.
        logline = '{:3} {:2} {:02}:{:02}:{:02} {} {}: {}\n'.format(
                                                        self.shortmonths[curtime.month],
                                                        curtime.day,
                                                        curtime.hour,
                                                        curtime.minute,
                                                        curtime.second,
                                                        self.hostid,
                                                        servicepidstring,
                                                        message
                                                        )
        self.log.write(logline)

        return True


