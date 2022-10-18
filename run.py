#!/bin/env python3

#os.system("chown -R $USER:wheel " + root)

import os, json

root = os.getcwd()
tmpfs = root + '/benchmarks/tempfs'
assert os.getuid() == 0, "Error: Run as superuser"




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
    os.system("make clean > ./log.clean && make > ./log.make 2>&1")
    os.system("cp -r " + base_path + src_path + "/* " 
            + base_path + "/benchmarks/tempfs/")
    os.chdir(old)
    print("Compiling: " + src_path)

def run_exe(run_path, exe_file_path, input_file_path, output_file_path):
    old = os.getcwd()
    os.chdir(run_path)
    os.system("sudo perf record -o " + output_file_path + " " +
            exe_file_path + " < " + input_file_path + " >/dev/null 2>&1")
    os.chdir(old)
    print("Running: " + exe_file_path)
    print("\tSaving to: " + output_file_path)

def pf_mod(cpu_type, enable, base_path):
    old = os.getcwd()
    os.chdir(base_path)
    flag = ""
    if (enable): 
        flag = " -e"
    os.system("./tools/uarch-configure/intel-prefetch/intel-prefetch-disable" + flag + " > /tmp/pf_mod-" + str(enable) + ".txt 2>&1")
    os.chdir(old)
    print("Pre-fetcher: " + str(enable))

def tmpfs_mod(base_path, enable):
    old = os.getcwd()
    os.chdir(base_path)
    flag = ""
    if (not enable): 
        flag = " -d"
    os.system("./init_tmpfs.sh" + flag)
    os.chdir(old)
    print("Tempfs: " + str(enable))

#---------------------------------------------------------


os.system("lshw -json -C system -quiet > /tmp/temp.txt")
data = json.load(open("/tmp/temp.txt"))
path = './data/' + data[0]['version'].replace(' ', '') + '/'

assert os.path.isdir('./data'), "Error: Run in root directory!"
if not (os.path.isdir(path)):
    print("Adding dir: " , path)
    os.mkdir(path)

os.chdir(path)
print("Entering dir: " + path)

updateInfo("")

data = json.load(open("./info/processor.json"))
cpu = data[0]['product']

print("\tDetected CPU: " + cpu)
print("\tUpdated: " + path + "info/*")




tmpfs_mod(root, True)
compile_exe("gcc", "-O1 ", root, "/benchmarks/apps/fmm/")
pf_mod("NOT IMPLEMENTED YET", False, root)
run_exe(tmpfs, './FMM', './inputs/input.1.256', "/tmp/test.data")
pf_mod("NOT IMPLEMENTED YET", True, root)
tmpfs_mod(root, False)
