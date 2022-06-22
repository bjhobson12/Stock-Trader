# python3 thread.py >> ./error.log 2>&1 

import pandas_market_calendars as mcal
from datetime import timedelta, datetime
import threading
import os
import time
from pathlib import Path
import sys
import subprocess


if len(sys.argv) > 1:
    spawn = int(sys.argv[1])
    if spawn > 3:
        exit()
else:
    spawn = 0

with open(os.path.join(str(Path.home()), ".stock_trader_keys"), 'r') as keys:
    ENV = {i[0] : i[1] for i in [line.split("=") for line in keys.read().split("\n") if line != ""]}

TZ = mcal.get_calendar('NYSE').tz

def __run_py_script_process__(name, argstring='', background=False):
    subprocess.Popen("python3 {} {} >> ./error.log 2>&1 {}".format(os.path.join(os.getcwd(), name), argstring, '&' if background else ''), shell=True)

def __scrape_internet__():
    __run_py_script_process__('reddit_scraper.py', '{} {} {} {} {}'.format(ENV['client_id'], ENV['client_secret'], ENV['password'], ENV['user_agent'], ENV['username']))

def __init_trader_connection__():
    pass

def __spawn__():

    # new process to update codebase and restart server
    os.system("git pull")
    os.system("pip3 install -r requirements.txt")
    # os.system("chmod +x {}".format(os.path.join(os.getcwd(), 'exec.sh')))
    # subprocess.Popen("{} {} >> ./error.log 2>&1 &".format(os.path.join(os.getcwd(), 'exec.sh'), spawn + 1), shell=True)
    __run_py_script_process__('thread.py', str(spawn + 1))
    exit()

def __next_open_bell__():
    cal = mcal.get_calendar('NYSE')

    bells = cal.schedule(start_date=datetime.today(), end_date=datetime.today() + timedelta(days=7))
    open = bells.iloc[0,0].to_pydatetime() #, bells.iloc[0,1].to_pydatetime()
    
    if open < datetime.now(TZ):
        open = bells.iloc[1,0].to_pydatetime() #, bells.iloc[1,1].to_pydatetime()

    return open

def __time_to_opening_bell__():
    return 15 # (__next_open_bell__() - datetime.now(TZ)).seconds

timer = threading.Timer(max(__time_to_opening_bell__() - 600, 0), __scrape_internet__) # 10 minutes in seconds
timer.start()

timer = threading.Timer(max(__time_to_opening_bell__() - 120, 0), __init_trader_connection__) # 2 minutes in seconds
timer.start()

timer = threading.Timer(__time_to_opening_bell__(), __spawn__)
timer.start()


