#!/bin/bash

CURRENT=$(cd $(dirname $0) && pwd)
LOGFILE=$CURRENT/log.txt

## Execute COVERT
cd $CURRENT
cd ../sample/analysis_tool/covert_dist
# sh ./covert.sh apkfiles > $LOGFILE

echo "Finished" >> $LOGFILE



