
import datetime
import config as config
import random

# Monday = 0
# Sunday = 6

daynumbers = [
    'Monday',
    'Tuesday',
    'Wednesday',
    'Thursday',
    'Friday',
    'Saturday',
    'Sunday'
]

def parsetime(timestring): # Outputs the second in the day based on the time string.
    returntime = 0
    if len(timestring) == 0:
        returntime = 0
    elif len(timestring) <= 2:  # Either 0H, H or HH
        returntime = int(timestring) * 3600
    elif len(timestring) == 3:  # HMM
        returntime = int(timestring[0]) * 3600 + int(timestring[1:3]) * 60
    elif len(timestring) == 4:  # HHMM
        returntime = int(timestring[0:2]) * 3600 + int(timestring[2:4]) * 60
    else:
        returntime = 0

    if returntime > 86400:
        returntime = 0

    return returntime


class Schedule:

    def __init__(self, scheduleconfig, start_epoch=0, end_epoch=2**32):
        self.scheduleconfig = scheduleconfig # For if we need to reuse it.
        self.schedule_type = scheduleconfig['scheduletype'] # periodic or burst types
        self.days = [False,False,False,False,False,False,False] # True for index of days that are "enabled"
        self.day_starttime = 0 # In seconds of the day.
        self.day_endtime = 0 # In seconds of the day.
        self.perperiod = scheduleconfig['perperiod'] # How many times should even happen per scheduled period.
        self.misschance = int(scheduleconfig['misschance']) # Percent chance of missing this period
        self.deviationchance = int(scheduleconfig['deviationchance']) # Percent chance of deviating from schedule
        self.maxdeviation = 0 # maximum deviation in seconds. 0 default. We'll set this below.
        self.start_epoch = start_epoch # For Burst types
        self.end_epoch = end_epoch

 
        self.setMaxDeviation()

        self.setDayTimes()



    def setDayTimes(self):
        # Process the time of day config.
        # Put here to be sure we reget the original values if we set it again.
        # We're not going to handle multiple time of day ranges yet.
        timesection = self.scheduleconfig['time']
        if timesection.find("-") >= 0:
            # time of day range
            (starttime, endtime) = timesection.split("-")
            self.day_starttime = parsetime(starttime) # Convert from the clock time into seconds of the day.
            self.day_endtime = parsetime(endtime)
        else:
            # Not sure at this time how to interpret a single specific time of day or other config.
            raise Exception('Invalid config in time setting {}. Needs to be a range.'.format(str(timesection)))

        # Check to make sure that the configured start time and end time +/- maxdeviation don't overlap.
        #print("Start: " + str(self.day_starttime + self.maxdeviation))
        #print("End: " + str(self.day_endtime - self.maxdeviation))
        if (self.day_starttime + self.maxdeviation) >= (self.day_endtime - self.maxdeviation):
            raise Exception('Start and end times cross for schedule with range {} and maxdeviation {}'.format(
                                                    str(self.scheduleconfig['time']),
                                                    str(self.scheduleconfig['maxdeviation'])))

        # The deviation could be + or - the starttime or end time, so multiply the offset by 2
        # to get the range, then add the random number to the start time minus the maxdeviation.
        randomoffset = random.randint(0,self.maxdeviation * 2)
        self.day_starttime = self.day_starttime - self.maxdeviation + randomoffset

        # Same for end of day
        randomoffset = random.randint(0,self.maxdeviation * 2)
        self.day_endtime = self.day_endtime - self.maxdeviation + randomoffset

        # The question though is what to do about times that end up out of the 0 to 86400 range.
        # This is a "design flaw" that needs to be addressed.
        if self.day_starttime < 0:
            self.day_starttime = 1
        if self.day_endtime >= 86400:
            self.day_endtime = 86399



        for daysection in self.scheduleconfig['days'].split(","): 
            if daysection.find("-") >= 0:
                # Day Range
                (startday, endday) = daysection.split("-")
                startindex = daynumbers.index(startday)
                endindex = daynumbers.index(endday)
                i = startindex
                while i <= endindex:
                    self.days[i] = True
                    i += 1
            else:
                # Individual day
                self.days[daynumbers.index(daysection)] = True


        # For burst type schedules, we need to adjust the start_epoch to be a
        # random time during the range provided at instantiation.
        self.start_epoch = random.randint(self.start_epoch, self.end_epoch)



    def setMaxDeviation(self):
        # Process maxdeviation from config. This can't handle compound deviations such as 10h5m yet.
        # This needs to happen prior to appending to setting day start and end times.
        if isinstance(self.scheduleconfig['maxdeviation'], str):
            maxdevconf = self.scheduleconfig['maxdeviation']
            numeric = "" # The number
            quantifier = "" # h, m or s
            for i in range(0,len(maxdevconf)):
                char = maxdevconf[i]
                if char.isdigit():
                    numeric += char
                elif char == "h" or char == "m" or char == "s":
                    quantifier = char
                else:
                    raise Exception('Invalid character {} in maxdeviation {}'.format(str(char), str(maxdevconf)))

            numeric = int(numeric)

            # Now process the quantifer character in the config if there is one.
            if quantifier == "h":
                self.maxdeviation = numeric * 3600
            elif quantifier == "m":
                self.maxdeviation = numeric * 60
            elif quantifier == "s" or quantifier == "":
                self.maxdeviation = numeric
            else:
                raise Exception('Something went wrong in the processing of maxdeviation {}'.format(str(maxdevconf)))
        else:
            raise Exception('maxdeviation {} is not a string.'.format(str(self.scheduleconfig['maxdeviation'])))


    def epochtimeInSchedule(self, epochtime):
        if self.schedule_type == "periodic":
            dt = datetime.datetime.fromtimestamp(epochtime)
            if self.days[dt.weekday()] == True: # If the day of the week is enabled for this schedule.
                tod_seconds = dt.hour * 3600 + dt.minute * 60 + dt.second
                # Check if the tod_seconds is within the day range.
                if self.day_starttime <= tod_seconds and tod_seconds < self.day_endtime:
                    return True
        elif self.schedule_type == "burst":
            if self.start_epoch <= epochtime and epochtime < self.end_epoch: # Easy
                return True

        return False


    def getEndOfDayTime(self, epochtime): # Given an epochtime, find the end of day time for that scheduled day.
        # Get date from given epochtime
        dt = datetime.datetime.fromtimestamp(epochtime)

        # Find epochtime for midnight on date
        midnightdt = datetime.datetime(dt.year,dt.month,dt.day)
        # Add self.day_endtime to daymidnight-epochtime and store in return value.
        endofdaytimeepoch = midnightdt.timestamp() + self.day_endtime

        return endofdaytimeepoch
        


