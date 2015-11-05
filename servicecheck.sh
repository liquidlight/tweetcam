#!/bin/sh

RESULT=`ps aux | grep '[b]ot.py'`

if [ "${RESULT:-null}" = null ]; then
    echo "Starting"
    sudo service tweets start
else
    echo "Already running"
fi
