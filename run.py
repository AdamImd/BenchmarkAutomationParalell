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
          output_folder = directory in which to store perf.data aliases
          iters = number of times to run perf report
    runs a compiled benchmark executable file with preset inputs and logs the perf record data
    runs iters times and stores each run's data in a different file in the output_folder
'''
def run_exe(run_path, exe_file_path, parameters, output_folder, iters):
    old = os.getcwd()
    os.chdir(run_path)
    # run the executable with perf record iters times and save the outputs 
    # to files of the form reporti.data in output_folder
    for i in range(iters):
        os.system("sudo perf record -o " + output_folder + "/record" + str(i) + ".data " +
            exe_file_path + " " + parameters + " >/dev/null") # 2>&1")
    os.chdir(old)
    print("Running: " + exe_file_path)
    print("\tSaving to: " + output_folder)

''' args: run_path = path to the executable to run (e.g., tempfs)
          exe_file_path = name of the executable file
          input_file_path = relative path to input file desired for this run
          output_folder = directory in which to store perf stat data for this run
          iters = number of times to run perf stat
    runs a compiled benchmark executable file with preset inputs and logs the perf stat data
    runs iters times and stores each run's data in a different file in the output_folder
    also stores a CSV of iters repeated runs and aggregate statistics, taken separately
'''
def run_exe_stats(run_path, exe_file_path, parameters, output_folder, iters):
    old = os.getcwd()
    os.chdir(run_path)
    # run the executable with perf stat iters times and write the outputs to 
    # csv files in output_folder of the form stati.csv
    for i in range(iters):
        os.system("sudo perf stat -d -d -d -o " 
            + output_folder + "/stat" + str(i) + ".csv -x , " +
            exe_file_path + " " + parameters + " >/dev/null")
    
    os.system("sudo perf stat -d -d -d -o " + output_folder + 
            "/stat_multi.csv -x , " + " -r " + str(iters) + " " +
            exe_file_path + " " + parameters + " >/dev/null")

    os.chdir(old)
    print("Running: " + exe_file_path)
    print("\tSaving to: " + output_folder)

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

# resets the Makefile to its original state so we don't have merge conflicts
# takes in the path to the base directory
def reset_config(base_path):
    # save current directory 
    old = os.getcwd()
    os.chdir(base_path)
    # restore original Makefile to erase config edits from prior runs
    os.system("cp ./benchmarks/Makefile.config.src ./benchmarks/Makefile.config")
    
    os.chdir(old)

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
    # all possible flag options we might want to test
    flags["gcc"] = ["-O0", "-O1", "-O2", "-O3", "-Ofast", "-fprefetch-loop-arrays"]
    # refine to just 2
    flags["gcc"] = ["-O0", "-O1", "-O2", "-Ofast"]

    app = "/benchmarks/kernels/fft"
    prog = "./FFT"
    # 2^24 data points gives around 4 sec per test
    # Add or subtract 2 to scale by around 4x or 1/4x
    # start with p = 1 thread
    inpt = " -m22 -p1"

    records = 2
    stats = 20

    # run the tests
    old = os.getcwd()
    results_dir = input("Directory name for results: ")
    os.mkdir(results_dir);
    os.chdir(results_dir);

    for c in compilers:
        os.mkdir(c);
        os.chdir(c);
        for f in flags[c]:
            os.mkdir(f);
            os.chdir(f);
            tmpfs_mod(root, True)
            compile_exe(c, f, root, app)
            for pf in [True, False]:
                os.mkdir(str(pf));
                os.chdir(str(pf));
                pf_mod("??????", pf, root)
                outpath = os.getcwd() 
                # run many tests and collect data for particular choice of c, f, pf
                run_exe(tmpfs, prog, inpt, outpath, records)
                run_exe_stats(tmpfs, prog, inpt, outpath, stats)
                os.chdir("../");
            os.chdir("../");
        os.chdir("../");
    os.chdir("../");
    # remove temp file system
    tmpfs_mod(root, False)

    os.chdir(root)
    # Change ownership of all files to current user
    os.system('chown "$SUDO_USER" ./ -R')

    reset_config(root)

if __name__ == "__main__":
    main()

