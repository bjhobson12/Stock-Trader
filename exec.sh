#!/usr/bin/env bash
# to execute chmod +x && ./exec.sh >> ./error.log 2>&1

if [ "$1" = "4" ]; then
    echo "Emergency shutdown issued after 4 spawns"
    exit 0
fi

now=$(date)

echo "PID: $$ - $now" 

spawn=$1
if [ -z "$1" ]; then
    spawn=0
fi

git pull
/usr/local/bin/python3 thread.py $spawn -u >> ./error.log 2>&1
