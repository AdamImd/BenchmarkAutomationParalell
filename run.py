#!/bin/env python3

#os.system("chown -R $USER:wheel " + root)

import os, json

root = os.getcwd()
tmpfs = root + '/benchmarks/tempfs'
assert os.getuid() == 0, "Error: Run as superuser"




#-------------------------------------------------

# write CPU info to json files in info directory
def updateInfo():
    os.system("mkdir -p ./info/")
    os.system("lshw -json -enable test -quiet > ./info/all.json")
    os.system("lshw -json -C processor -quiet > ./info/processor.json")
    os.system("lshw -json -C memory -quiet > ./info/memory.json")
    os.system("lshw -json -C storage -quiet > ./info/storage.json")
    os.system("lshw -json -C system -quiet > ./info/system.json")
    os.system("lshw -json -C power -quiet > ./info/power.json")
    os.system("lshw -json -C input -quiet > ./info/input.json")
    os.system("lshw -json -C bridge -quiet > ./info/bridge.json")


# TODO: Return location of executable
''' args: compiler = compiler to use for this compilation
          flags = compiler flags to pass in
          base_path = path to the benchmark folder, should be BenchmarkAutomation root
          src_path = path to the particular benchmark program to compile
    compiles one benchmark program according to the passed in settings
'''
def compile_exe(compiler, flags, base_path, src_path):
    # save current directory 
    old = os.getcwd()
    os.chdir(base_path)
    # restore original Makefile to erase config edits from prior runs
    os.system("cp ./benchmarks/Makefile.config.src ./benchmarks/Makefile.config")
    data = open("./benchmarks/Makefile.config").readlines()
    # fill in compiler and flags
    data[0] = "CC := " + compiler + '\n'
    data[1] = "CFLAGS := " + flags + '\n'
    # fill in location of benchmark on particular CPU
    data[6] = "BASEDIR := " + base_path + "/benchmarks/" + '\n'
    # re-write modifications to Makefile config
    open("./benchmarks/Makefile.config", 'w').writelines(data)
    os.chdir(base_path+src_path)
    os.system("make clean > ./log.clean && make" ) # > ./log.make 2>&1")
    # move compiled program to temp file system so there are no conflicts with hard drive page faults
    # also copies all files that come with it (e.g., preset inputs)
    os.system("cp -r " + base_path + src_path + "/* " + base_path + "/benchmarks/tempfs/")
    # restore directory
    os.chdir(old)
    print("Compiling: " + src_path)

''' args: run_path = path to the executable to run (e.g., tempfs)
          exe_file_path = name of the executable file
          input_file_path = relative path to input file desired for this run
          output_file_path = name to give perf.data for this run
    runs a compiled benchmark executable file with preset inputs and logs the perf record data
'''
def run_exe(run_path, exe_file_path, input_file_path, output_file_path):
    old = os.getcwd()
    os.chdir(run_path)
    # run the executable with perf record and save the output to output_file_path
    os.system("sudo perf record -o " + output_file_path + " " +
            exe_file_path + " < " + input_file_path + " >/dev/null") # 2>&1")
    os.chdir(old)
    print("Running: " + exe_file_path)
    print("\tSaving to: " + output_file_path)

# run perf report for a particular perf.data alias
''' args: report_file = alias for perf.data to call report on
          report_path = location of the data
'''
def report_from_run(report_file, report_path):
    old = os.getcwd()
    os.chdir(report_path)

    os.system("cp " + report_file + " perf.data")
    os.system("sudo perf report")

    os.system("rm perf.data")
    os.chdir(old)

# turn on or off the hardware prefetcher
# TODO: work on this later
def pf_mod(cpu_type, enable, base_path):
    old = os.getcwd()
    os.chdir(base_path)
    flag = ""
    if (enable): 
        flag = " -e"
    os.system("./tools/uarch-configure/intel-prefetch/intel-prefetch-disable" + flag + " > /tmp/pf_mod-" + str(enable) + ".txt") # 2>&1")
    os.chdir(old)
    print("Pre-fetcher: " + str(enable))

# set up temp file system using init_tempfs.sh script
''' args: base_path = location of init_tempfs.sh (root directory of project)
          enable = boolean, if True then sets up file system in tempfs
                            else reverts tempfs to a normal directory
    erases the tempfs directory and sets up/tears down a temp file system there
'''
# TODO: maybe copy script directly into os.system commands
def tmpfs_mod(base_path, enable):
    old = os.getcwd()
    os.chdir(base_path)
    flag = "" if enable else " -d" # for disable 
    os.system("./init_tmpfs.sh" + flag)
    os.chdir(old)
    print("Tempfs: " + str(enable))

#---------------------------------------------------------

def main():
    # store temporary data on the current CPU we're using
    os.system("lshw -json -C system -quiet > /tmp/temp.txt")
    data = json.load(open("/tmp/temp.txt"))
    try:
        benchmark_data_path = './data/' + data[0]['version'].replace(' ', '') + '/'
    except:
        print("WARNING: Couldn't find version, writing to default folder")
        benchmark_data_path = './data/' + 'versionless/'

    assert os.path.isdir('./data'), "Error: Run in root directory!"
    # create 
    if not (os.path.isdir(benchmark_data_path)):
        print("Adding dir: " , benchmark_data_path)
        os.mkdir(benchmark_data_path)

    os.chdir(benchmark_data_path)
    print("Entering dir: " + benchmark_data_path)
    # convert relative path to absolute path
    benchmark_data_path = os.getcwd()

    # record CPU info
    updateInfo()

    try:
        data = json.load(open("./info/processor.json"))
        cpu = data[0]['product']
    except:
        cpu = 'unknown'
        print("WARNING: CPU not found")

    print("\tDetected CPU: " + cpu)
    print("\tUpdated: " + benchmark_data_path + "info/*")

    # all compilers and possible flags to test
    compilers = ["gcc"]
    flags = dict()
    flags["gcc"] = ["-O1", "-O2"]

    app = "/benchmarks/apps/fmm"
    prog = "./FMM"
    inpt = "./inputs/input.1.256"

    # run the tests

    for c in compilers:
        for f in flags[c]:
            compile_exe(c, f, root, app)
            for pf in [True, False]:
                tmpfs_mod(root, True)
                pf_mod("??????", pf, root)
                outpath = benchmark_data_path + "/test_"+prog+"_"+c+"_"+f+"_"+pf
                run_exe(tmpfs, prog, inpt, outpath)
    tmpfs_mod(root, False)

#    tmpfs_mod(root, True)
#    # compile the program to use
#    compile_exe("gcc", "-O1 ", root, "/benchmarks/apps/fmm/")
#    pf_mod("NOT IMPLEMENTED YET", False, root)
#    run_exe(tmpfs, './FMM', './inputs/input.1.256', benchmark_data_path+"/test_off.data")
#    pf_mod("NOT IMPLEMENTED YET", True, root)
#    run_exe(tmpfs, './FMM', './inputs/input.1.256', benchmark_data_path+"/test_on.data")
#    tmpfs_mod(root, False)

if __name__ == "__main__":
    main()

