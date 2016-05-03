#!/bin/bash

CURRENT=$(cd $(dirname $0) && pwd)
LOGFILE=$CURRENT/log_covert.txt
COVERT=$CURRENT/../analysis_tool/covert_dist
OVERALL=$CURRENT/../overallSystemArchitecture

## Execute COVERT
cd $COVERT
sh ./covert.sh apkfiles 2>&1 > $LOGFILE

## Copy the result 
cp app_repo/apkfiles/apkfiles.xml $OVERALL/

echo "__Finished__" >> $LOGFILE



