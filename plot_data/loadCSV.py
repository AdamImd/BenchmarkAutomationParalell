#!/bin/env python3

import csv

run = {}
file = "./test.csv"
data = csv.reader(open(file).readlines()[2:])
for dat in data:
    run[dat[2]] = dat

print(run["task-clock"][3])
