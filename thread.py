# /usr/local/bin/python3 thread.py >> ./error.log 2>&1 

import pandas_market_calendars as mcal
from datetime import timedelta, datetime
import threading
import os
import time
from pathlib import Path
import sys
import subprocess

spawn = 0
if len(sys.argv) > 1:
    spawn = int(sys.argv[1])

with open(os.path.join(str(Path.home()), ".stock_trader_keys"), 'r') as keys:
    ENV = {i[0] : i[1] for i in [line.split("=") for line in keys.read().split("\n") if line != ""]}

# Path to thread, arguments, blocking?
SCRIPT_PATHS = [
    (os.path.join(str(Path.cwd()), "greeting.py"), None, False),
    (os.path.join(str(Path.cwd()), "reddit_scraper.py"), '{} {} {} {} {}'.format(ENV['client_id'], ENV['client_secret'], ENV['password'], ENV['user_agent'], ENV['username']), False)
]
TZ = mcal.get_calendar('NYSE').tz

def __dispatch__():
    for threads in SCRIPT_PATHS:
        pass
        #os.system('/usr/local/bin/python3 {} {}'.format(*threads[:2]))

    # new process to update codebase and restart server
    os.system("chmod +x {}".format(os.path.join(os.getcwd(), 'exec.sh')))
    subprocess.Popen("{} {} >> ./error.log 2>&1 &".format(os.path.join(os.getcwd(), 'exec.sh'), spawn + 1), shell=True)
    exit()

def __next_open_bell__():
    cal = mcal.get_calendar('NYSE')

    bells = cal.schedule(start_date=datetime.today(), end_date=datetime.today() + timedelta(days=7))
    open = bells.iloc[0,0].to_pydatetime() #, bells.iloc[0,1].to_pydatetime()
    
    if open < datetime.now(TZ):
        open = bells.iloc[1,0].to_pydatetime() #, bells.iloc[1,1].to_pydatetime()

    return open

def __time_to_opening_bell__():
    return 2 # (__next_open_bell__() - datetime.now(TZ)).seconds

timer = threading.Timer(__time_to_opening_bell__(), __dispatch__)
timer.start()


