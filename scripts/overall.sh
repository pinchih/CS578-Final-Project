#!/bin/bash

CURRENT=$(cd $(dirname $0) && pwd)
LOGFILE=$CURRENT/log.txt
OVERALL=$CURRENT/../overallSystemArchitecture
COVERT=$CURRENT/../analysis_tool/covert_dist

## Extract APKs
cd $COVERT/resources/Covert
echo "Extracting apk models ..."
./covert.sh model apkfiles > $LOGFILE

## Copy the result
cp -f $COVERT/app_repo/apkfiles/analysis/model/*.xml $OVERALL

## Convert XML to JSON
echo "Convert extracting data to json ..."
#cd $CURRENT
#python soup.py ../sample/analysis_tool/covert_dist/app_repo/apkfiles/analysis/model output >> $LOGFILE
cd $OVERALL
python overallArchXMLCovertor.py >> $LOGFILE

echo "Finished" >> $LOGFILE

