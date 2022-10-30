#! /bin/env python3 
# analysis.py
# tranverses the directory structure created by run.py and constructs a data table
# then enables data analysis on the data such as by creating plots

import os, csv
import matplotlib.pyplot as plt

CPU = "ThinkPadX270"

def read_data(fname):
    run = {}
    data = csv.reader(open(fname).readlines()[2:])
    for dat in data:
        run[dat[2]] = dat
    return run

def main():
    root = os.getcwd()
    #machine = input("Enter the machine to get data for: ")
    machine = CPU

    test_foldr = input("Enter the folder containing all test data: ")

    foldr = root + "/data/" + machine + "/" + test_foldr + "/"

    data = dict()

    # get list of compiler folders
    compilers = list(filter(lambda p: os.path.isdir(foldr + p), os.listdir(foldr)))
    for c in compilers:
        data[c] = dict()
        cpath = foldr + c + "/"
        # get list of flag folders
        flags = list(filter(lambda p: os.path.isdir(cpath + p), os.listdir(cpath)))
        for f in flags:
            data[c][f] = dict()
            fpath = cpath + f + "/"
            
            for pf in [True, False]:
                # get all csv files with stat data
                stats = list(filter(lambda x: x[-3:] == "csv", os.listdir((fpath + str(pf)))))
                        
                data[c][f][pf] = [read_data(fpath + str(pf) + "/" + fname) for fname in stats]

    # data should now exist
    # access via data[compiler][flag][prefetch bool][index][desired data field]
    # e.g., data["gcc"]["-O0"][True][4]["branch-misses"]

    x_cat = 'L1-dcache-loads'
    y_cat = 'L1-dcache-load-misses'
    parameter = (("-O1", False), ("-O1", True), ("-O2", False), ("-O2", True), ("-Ofast", False), ("-Ofast", True))
    for parm in parameter:
        x = []
        y = []
        for i in data["gcc"][parm[0]][parm[1]][:-1]:
            x.append(float(i[x_cat][0]))
            y.append(float(i[y_cat][0]))
        plt.scatter(x, y)
    plt.legend([i[0]+"_"+str(i[1]) for i in parameter])
    plt.xlabel(x_cat)
    plt.ylabel(y_cat)
    plt.show()

if __name__ == "__main__":
    main()
