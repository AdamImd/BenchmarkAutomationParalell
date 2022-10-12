#!/bin/bash

sudo umount ./benchmarks/tempfs/ 2>/dev/null
rm -r ./benchmarks/tempfs/
mkdir -p ./benchmarks/tempfs

if [ -z "$1" ] 
then
	sudo mount -t tmpfs -o size=1G tmpfs ./benchmarks/tempfs/ 
fi
