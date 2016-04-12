#!/bin/bash
# usage: ./this.sh directory_having_json_files
# $ Ex. ./this.sh output/
# 
outdir=$1
pwd=`pwd`

for file in $1/*.json; do
	echo file://${pwd}/index.html?file=${file}
done

