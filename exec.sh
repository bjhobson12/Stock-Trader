#!/usr/bin/env bash

now=$(date)

echo "PID: $$ - $now" 

if [ "$1" = "4" ]; then
    echo "Emergency shutdown issued after 4 spawns"
    exit 0
fi

git pull
/usr/local/bin/python3 thread.py $1

exit 0