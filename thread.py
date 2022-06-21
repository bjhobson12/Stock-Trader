# python3 thread.py >> ./error.log 2>&1 

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
    (os.path.join(str(Path.cwd()), "model.py"), None, False)
]
TZ = mcal.get_calendar('NYSE').tz

def __scrape_internet__():
    subprocess.Popen("python3 {} >> ./error.log 2>&1 &".format(os.path.join(os.getcwd(), 'reddit_scraper.py')), shell=True)

def __init_trader_connection__():
    pass

def __dispatch__():
    for threads in SCRIPT_PATHS:
        os.system('python3 {} {}'.format(*threads[:2]))

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
    return (__next_open_bell__() - datetime.now(TZ)).seconds

timer = threading.Timer(__time_to_opening_bell__() - 600, __scrape_internet__) # 10 minutes in seconds
timer.start()

timer = threading.Timer(__time_to_opening_bell__() - 120, __init_trader_connection__) # 2 minutes in seconds
timer.start()

timer = threading.Timer(__time_to_opening_bell__(), __dispatch__)
timer.start()


