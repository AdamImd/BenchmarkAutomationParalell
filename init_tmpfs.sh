#!/bin/bash

mkdir -p ./benchmarks/tempfs
sudo umount ./benchmarks/tempfs/ 2>/dev/null
sudo mount -t tmpfs -o size=1G tmpfs ./benchmarks/tempfs/ 

