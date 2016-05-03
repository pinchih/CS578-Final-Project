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
<<<<<<< HEAD
=======
rm $OVERALL/*.xml
>>>>>>> 741a2b22eb52ad39b15763244e1fb133a12a4cb7
cp -f $COVERT/app_repo/apkfiles/analysis/model/*.xml $OVERALL

## Convert XML to JSON
echo "Convert extracting data to json ..."
#cd $CURRENT
#python soup.py ../sample/analysis_tool/covert_dist/app_repo/apkfiles/analysis/model output >> $LOGFILE
cd $OVERALL
<<<<<<< HEAD
python overallArchXMLCovertor.py >> $LOGFILE
=======
python overallArchXMLCovertor.py 2>&1 >> $LOGFILE
>>>>>>> 741a2b22eb52ad39b15763244e1fb133a12a4cb7

echo "__Finished__" >> $LOGFILE

