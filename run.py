#! /bin/env python3 
import os, csv
from analysis import analyze, plot_data
import pickle

all_data = []

#settings = csv.reader(open("./benchmarks/settings.csv", "r"))
settings = []
for kernel in range(2):
    for dim in range(30000, 40000, 5000):
        for precision in range(0, 3):
            settings.append((kernel, dim, 5*10**-precision, 100, 100, 200))

for setting in settings:
    data = {}
    data["setting"] = setting

    with open("./benchmarks/config.h", "w") as config:
        print("Running with settings: {}".format(setting))
        config.write("#ifndef config_h\n")
        config.write("#define config_h\n")
        config.write("#define KERNEL {}\n".format(setting[0]))
        config.write("#define DIMENSION {}\n".format(setting[1]))
        config.write("#define PRECISION {}\n".format(setting[2]))
        config.write("#define MAX_VALUE {}\n".format(setting[3]))
        config.write("#define LOG_STEP {}\n".format(setting[4]))
        config.write("#define SEED {}\n".format(setting[5]))
        config.write("#endif\n")

    compile = "gcc -fopenmp -o ./benchmarks/shared ./benchmarks/sharedMemoryParallel.c ./benchmarks/kernels.c "
    os.system(compile)

    perf = "perf stat -x , -o /tmp/perf.csv -ddd "
    perf = ""
    run = "./benchmarks/shared"
    os.system(perf + run)

    data['perf'] = {}
    with open("/tmp/perf.csv", "r") as file:
        file.readline()
        file.readline()
        perf = csv.reader(file)
        for row in perf:
            data['perf'][row[2]] = row[3]
    print(data['perf'])

    data['iterations'], data['raw'] = analyze()
    print(data['iterations'])

    all_data.append(data)

    plot_data(data['raw'], setting[3])
    break

with open("./data/all_data.pickle", "wb") as file:
    pickle.dump(all_data, file)
