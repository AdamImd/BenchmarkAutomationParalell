#!/bin/env python3

#os.system("chown -R $USER:wheel " + root)

import os, json

root = os.getcwd()

assert os.getuid() == 0, "Error: Run as superuser"

os.system("lshw -json -enable test -quiet > /tmp/temp.txt")
data = json.load(open("/tmp/temp.txt"))

cpu = data[0]['children'][0]['children'][0]['product']
path = './data/' + data[0]['version'].replace(' ', '') + '/'

assert os.path.isdir('./data'), "Error: Run in root directory!"
if not (os.path.isdir(path)):
    print("Adding dir: " , path)
    os.mkdir(path)

os.chdir(path)
print("Entering dir: " + path)
os.system("lshw -json -enable test -quiet > ./computer_info.json")
print("\tDetected CPU: " + cpu)
print("\tUpdated: " + path + "computer_info.json")


