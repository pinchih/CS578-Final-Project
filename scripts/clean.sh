#!/bin/bash
# 2016.5.2. tats
# usage: ./clean.sh

CURRENT=$(cd $(dirname $0) && pwd)
OVERALL=$CURRENT/../overallSystemArchitecture
COVERT=$CURRENT/../analysis_tool/covert_dist
DIDFAIL=$CURRENT/../analysis_tool/didfail
COMPO=$CURRENT/../interCompo

## Preparation
rm -rf $CURRENT/../apkfiles/*
rm -rf $CURRENT/../graph.json
rm -rf $CURRENT/log*.txt
rm -rf $COVERT/app_repo/apkfiles
rm -rf $DIDFAIL/out/*
rm -rf $OVERALL/*.json
rm -rf $OVERALL/*.xml
rm -rf $OVERALL/flows.out
rm -rf $COMPO/output/*

