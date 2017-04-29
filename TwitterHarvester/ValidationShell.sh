#!/bin/sh
if ps -ef | grep -v grep | grep getTweetSearch.py ; then
        exit 0
else
        python /home/pythonFiles/getTweetSearch.py &
        #Write note to Logfile
        echo "[`date`]: twitter.py was not running... Restarted" >> /home/pythonFiles/twitterHarvest.log
        exit 0
fi