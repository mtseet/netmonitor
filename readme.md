# netmonitor

Script for monitoring local network

## Description

This python script monitors the local network using tcpdump and provides stats
via html GUI. Tcpdump and sqlite are used.

Assumes code is cloned to /home/user/github/netmonitor

## Dependencies

sudo apt install tcpdump sqlite3

## Usage

#start capture
sudo ./process.py &

#test data is being captured
/usr/bin/python3 ./query.py todaytotal

#see more net stats
/usr/bin/python3 $rootpath/query.py latest

for GUI
serve ipstat.php via php
You can for example deploy nginx and php-frm use that to serve the php GUI.

## Screenshot

See [Screenshot](https://github.com/mtseet/netmonitor/blob/master/Screenshot%20from%202022-01-16%2013-53-04.png).

