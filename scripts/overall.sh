#!/bin/bash

CURRENT=$(cd $(dirname $0) && pwd)
LOGFILE=$CURRENT/log.txt
OVERALL=$CURRENT/../overallSystemArchitecture
COVERT=$CURRENT/../analysis_tool/covert_dist
COMPO=$CURRENT/../interCompo

## Extract APKs
cd $COVERT/resources/Covert
echo "Extracting apk models ..."
./covert.sh model apkfiles > $LOGFILE

## Copy the result
rm $OVERALL/*.xml
cp -f $COVERT/app_repo/apkfiles/analysis/model/*.xml $OVERALL

## Convert XML to JSON for overall architecture
echo "Convert extracting data to json ..."
#cd $CURRENT
#python soup.py ../sample/analysis_tool/covert_dist/app_repo/apkfiles/analysis/model output >> $LOGFILE
cd $OVERALL
python overallArchXMLCovertor.py 2>&1 >> $LOGFILE

## Convert XML to JSON for intra application visualization
cd $COMPO
rm -rf output/*
python soup.py $COVERT/app_repo/apkfiles/analysis/model ./output 2>&1 >> $LOGFILE


echo "__Finished__" >> $LOGFILE

