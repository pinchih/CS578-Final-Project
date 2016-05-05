#!/bin/bash
# 2016.5.2 tats
# usage: ./vulnerable.sh

CURRENT=$(cd $(dirname $0) && pwd)
LOGFILE=$CURRENT/log_vul.txt
COVERT=$CURRENT/../analysis_tool/covert_dist
DIDFAIL=$CURRENT/../analysis_tool/didfail
OVERALL=$CURRENT/../overallSystemArchitecture

## Execute COVERT
cd $COVERT
sh ./covert.sh apkfiles 2>&1 > $LOGFILE

## Copy the result 
cp app_repo/apkfiles/apkfiles.xml $OVERALL/

## Convert xml to json (graph.json will be updated)
cd $OVERALL
python VulnerablePathXMLCovertor.py 2>&1 >> $LOGFILE

## Execute DidFail
cd $DIDFAIL
./cert/run-didfail.sh out ../../apkfiles/*.apk 2>&1 >> $LOGFILE

## Copy the result 
cp out/flows.out $OVERALL/
cp out/*.fd.xml $OVERALL/

## Convert xml to json (graph.json will be updated)
cd $OVERALL
python VulnerablePathDidFail.py 2>&1 >> $LOGFILE


echo "__Finished__" >> $LOGFILE



