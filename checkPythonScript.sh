#!/bin/sh
if ps -ef | grep -v grep | grep harvest.py ; then
        exit 0
else
        python harvest.py &
        #Write note to Logfile
        echo "[`date`]: twitter.py was not running... Restarted" >> /var/log/twitterHarvest.log
        exit 0
fi