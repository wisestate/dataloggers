#!/bin/sh
# logManaging,.sh
# navigate to home directory, then to this directory, then execute python script, then back home

cd /
cd home/pi/dataCollecting
zip -r logs_$(date --date="1 week ago" "+"%Y-%m-%d"")_$(date + "%Y-%m-%d").zip logs/*
rm -r logs
python3 logManaging.csv
cd /
