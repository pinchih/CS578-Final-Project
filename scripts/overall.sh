#!/bin/bash

CURRENT=$(cd $(dirname $0) && pwd)
LOGFILE=$CURRENT/log.txt

## Extract APKs
cd $CURRENT
cd ../sample/analysis_tool/covert_dist/resources/Covert
echo "Extracting apk models ..."
./covert.sh model apkfiles > $LOGFILE


## Convert XML to JSON
cd $CURRENT
echo "Convert extracting data to json ..."
python soup.py ../sample/analysis_tool/covert_dist/app_repo/apkfiles/analysis/model output >> $LOGFILE

echo "Finished" >> $LOGFILE

