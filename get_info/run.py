#!/bin/env python3

import os, json

os.system("lshw -json > /tmp/temp.txt")
data = json.load(open("/tmp/temp.txt"))

print(data)
