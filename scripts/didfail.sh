#!/bin/bash

CURRENT=$(cd $(dirname $0) && pwd)
LOGFILE=$CURRENT/log_didfail.txt
DIDFAIL=$CURRENT/../analysis_tool/didfail

## Execute DidFail
cd $DIDFAIL
./cert/run-didfail.sh ./out ../../apkfiles/*.apk 2>&1 > $LOGFILE

echo "__Finished__" >> $LOGFILE



