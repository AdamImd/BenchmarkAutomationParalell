#!/bin/env python3

#os.system("chown -R $USER:wheel " + root)

import os, json

root = os.getcwd()
tmpfs = root + '/benchmarks/tempfs'
assert os.getuid() == 0, "Error: Run as superuser"


os.system("lshw -json -C system -quiet > /tmp/temp.txt")
data = json.load(open("/tmp/temp.txt"))
path = './data/' + data[0]['version'].replace(' ', '') + '/'

assert os.path.isdir('./data'), "Error: Run in root directory!"
if not (os.path.isdir(path)):
    print("Adding dir: " , path)
    os.mkdir(path)

os.chdir(path)
print("Entering dir: " + path)

data = json.load(open("./info/processor.json"))
cpu = data[0]['product']

print("\tDetected CPU: " + cpu)
print("\tUpdated: " + path + "info/*")



#-------------------------------------------------

def updateInfo(path):
    os.system("mkdir -p ./info/")
    os.system("lshw -json -enable test -quiet > ./info/all.json")
    os.system("lshw -json -C processor -quiet > ./info/processor.json")
    os.system("lshw -json -C memory -quiet > ./info/memory.json")
    os.system("lshw -json -C storage -quiet > ./info/storage.json")
    os.system("lshw -json -C system -quiet > ./info/system.json")
    os.system("lshw -json -C power -quiet > ./info/power.json")
    os.system("lshw -json -C input -quiet > ./info/input.json")
    os.system("lshw -json -C bridge -quiet > ./info/bridge.json")


# Return location of executable
def compile_exe(compiler, flags, base_path, src_path):
    old = os.getcwd()
    os.chdir(base_path)
    os.system("cp ./benchmarks/Makefile.config.src ./benchmarks/Makefile.config")
    data = open("./benchmarks/Makefile.config").readlines()
    data[0] = "CC := " + compiler + '\n'
    data[1] = "CFLAGS := " + flags + '\n'
    data[6] = "BASEDIR := " + base_path + "/benchmarks/" + '\n'
    open("./benchmarks/Makefile.config", 'w').writelines(data)
    os.chdir(base_path+src_path)
    os.system("make clean > ./log.clean && make > ./log.make")
    os.system("cp -r " + base_path + src_path + "/* " 
            + base_path + "/benchmarks/tempfs/")
    os.chdir(old)

def run_exe(run_path, exe_file_path, input_file_path, output_file_path):
    old = os.getcwd()
    os.chdir(run_path)
    os.system("sudo perf record -o " + output_file_path + " " +
            exe_file_path + " < " + input_file_path)
    os.chdir(old)

def tmpfs_init(base_path):
    old = os.getcwd()
    os.chdir(base_path)
    os.system("./init_tmpfs.sh")
    os.chdir(old)
    
def tmpfs_del(base_path):
    old = os.getcwd()
    os.chdir(base_path)
    os.system("./init_tmpfs.sh")
    os.chdir(old)

tmpfs_init(root)
compile_exe("gcc", "-O2 ", root, "/benchmarks/apps/fmm/")
run_exe(tmpfs, './FMM', './inputs/input.1.256', "/tmp/test.data")
#os.system(root + "/init_tmpfs.sh -u")
