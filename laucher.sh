#!/bin/sh
# launcher.sh
# navigate to home directory, then to this directory, then execute python script, then back home

cd /
cd home/pi/dataCollecting
tmux
python3 ftpPush.py |& tee output
