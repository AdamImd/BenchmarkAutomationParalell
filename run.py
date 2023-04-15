#! /bin/env python3 
import os, csv
from analysis import analyze, plot_data
import pickle
import math

all_data = []

#settings = csv.reader(open("./benchmarks/settings.csv", "r"))
settings = []
for dim in range(1000000, 100000000, 10000000):
    for precision in range(0, 3):
        for kernel in range(0, 6):
            settings.append((kernel, int(math.sqrt(dim)), 0.05*10**precision, 100, 100, 200))

for setting in settings:
    data = {}
    data["setting"] = setting

    with open("./benchmarks/config.h", "w") as config:
        #print("Running with settings: {}".format(setting))
        config.write("#ifndef config_h\n")
        config.write("#define config_h\n")
        config.write("#define KERNEL {}\n".format(setting[0]))
        config.write("#define DIMENSION {}\n".format(setting[1]))
        config.write("#define PRECISION {}\n".format(setting[2]))
        config.write("#define MAX_VALUE {}\n".format(setting[3]))
        config.write("#define LOG_STEP {}\n".format(setting[4]))
        config.write("#define SEED {}\n".format(setting[5]))
        config.write("#define SAVE_IMG 0\n")
        config.write("#endif\n")

    compile = "gcc -fopenmp -O3 -march=native -mfpmath=sse -O3 -ffast-math -o ./benchmarks/shared ./benchmarks/sharedMemoryParallel.c ./benchmarks/kernels.c "
    os.system(compile)

    perf = "perf stat -x , -o /tmp/perf.csv -ddd "
    run = "./benchmarks/shared"
    print("Perf and running")
    os.system(perf + run)
    print()

    with open("./benchmarks/config.h", "w") as config:
        #print("Running with settings: {}".format(setting))
        config.write("#ifndef config_h\n")
        config.write("#define config_h\n")
        config.write("#define KERNEL {}\n".format(setting[0]))
        config.write("#define DIMENSION {}\n".format(setting[1]))
        config.write("#define PRECISION {}\n".format(setting[2]))
        config.write("#define MAX_VALUE {}\n".format(setting[3]))
        config.write("#define LOG_STEP {}\n".format(setting[4]))
        config.write("#define SEED {}\n".format(setting[5]))
        config.write("#define SAVE_IMG 1\n")
        config.write("#endif\n")

    print("Running\n")
    os.system(compile)
    os.system(run)
    print()

    data['perf'] = {}
    with open("/tmp/perf.csv", "r") as file:
        file.readline()
        file.readline()
        perf = csv.reader(file)
        for row in perf:
            data['perf'][row[2]] = row[3]

    data['cycles'], data['micros'], data['raw'] = analyze()

    all_data.append(data)

with open("./data/all_data.pickle", "wb") as file:
    pickle.dump(all_data, file)



