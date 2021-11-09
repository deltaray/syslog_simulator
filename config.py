
hostname = 'myrtle'
logfile = 'syslog'

# Set the range for the logs
days = 17
# Start time of log.
startepoch = 1570420800  # unix epoch time.
# For convenience, just calculate endepoch, it can also be a epochtime.
endepoch = startepoch + 86400*days

# People/bots who play roles in the simulation
actors = {
    'Alice': { # Just a unique label.
        'count': '1', # How many instances of this actor will be created for the simulation
        'usernames': ['alice'],  # A list of usernames to use.
        'success': True,
        'intentions': 'benign',
        'schedule': [ 
            {'scheduletype': 'periodic', # Occurs repeatedly
             'days': 'Monday-Friday',
             'time': '0800-1600', # Non-inclusive on end of range
             'perperiod': '2-4',
             'misschance': '10', # Percentage
             'deviationchance': '10',
             'maxdeviation': '10m' # 10 minutes.
             # Be careful not to make maxdeviation overlap with end time maxdeviation.
            },
        ],
        'address-block': '129.120.10.0/24', # Can be any valid network block or specific IP in CIDR format.
        'services': ['sshd'] # The code is mostly ssh based now.
    },
    'Bob': {
        'count': '1',
        'usernames': ['bob'],
        'success': True,
        'intentions': 'benign',
        'schedule': [ 
            {'scheduletype': 'periodic',
             'days': 'Monday-Wednesday',
             'time': '0900-1700',
             'perperiod': '1-2',
             'misschance': '15', # Percentage
             'deviationchance': '20',
             'maxdeviation': '30m' # 30 minutes
            },
        ],
        'address-block': '2001:0:887c:a084::/64', #IPv6 works too.
        'services': ['sshd']
    },
    'Carol': {
        'count': '1',
        'usernames': ['carol'],
        'success': True,
        'intentions': 'benign',
        'schedule': [ 
            {'scheduletype': 'periodic',
             'days': 'Monday-Friday',
             'time': '1000-1600',
             'perperiod': '1-2',
             'misschance': '15', # Percentage
             'deviationchance': '20',
             'maxdeviation': '2h'
            },
        ],
        'address-block': '2001:0:887c:a084::/64', #IPv6 works too.
        'services': ['sshd']
    },
    'Eve': {
        'count': '50', # Create this many instances of this actor class.
        'usernames': ['root'],
        'success': False, # Short circuit for now.
        'intentions': 'malicious',
        'maxattempts': '900-1100', # This is optional.
        'schedule': [ 
            {'scheduletype': 'burst', # All at once, anytime during the overall range.
             # These settings below would have no effect on burst type schedules.
             'days': 'Monday-Sunday',
             'time': '0000-2400',  # Non-inclusive, does not include midnight on the following day
             'perperiod': '10-110',
             'misschance': '10',
             'deviationchance': '100',
             'maxdeviation': '0' # burst mode takes care of randomizing start.
            }
        ],
        'address-block': '0.0.0.0/0', # Any IPv4 address that is not reserved.
        'services': ['sshd']
    },
    'Ev6': {
        'count': '10',
        'usernames': ['root'],
        'success': False, # Short circuit for now.
        'intentions': 'malicious',
        'maxattempts': '900-1100', # This is optional.
        'schedule': [ 
            {'scheduletype': 'burst', # All at once, anytime during the overall range.
             # These settings below would have no effect on burst type schedules.
             'days': 'Monday-Sunday',
             'time': '0000-2400',  # Non-inclusive, does not include midnight on the following day
             'perperiod': '10-110',
             'misschance': '10',
             'deviationchance': '100',
             'maxdeviation': '0'
            }
        ],
        'address-block': '::/0', # Any IPv6 address that is not reserved.
        'services': ['sshd']
    },
    'Mallory': {
        'count': '2', # If just one username, then 200 different attempts at that one.
        # If more than 1 user, it will create an instance using each username round robin fashion.
        'usernames': ['mallory', 'admin'],
        'success': False, # Short circuit for now.
        'maxattempts': '101',
        'intentions': 'malicious',
        'schedule': [ 
            {'scheduletype': 'burst',
             'days': 'Friday,Saturday',
             'time': '1800-2400',  # Non-inclusive, does not include midnight on the following day
             'perperiod': '20',
             'misschance': '10',
             'deviationchance': '100',
             'maxdeviation': '1h'
            }
        ],
        'address-block': '129.120.10.0/24',
        'services': ['sshd']
    },
}




              


            
            

                                


