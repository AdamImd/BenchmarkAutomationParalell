
# analysis.py
# tranverses the directory structure created by run.py and constructs a data table
# then enables data analysis on the data such as by creating plots

import os, csv

def read_data(fname):
    run = {}
    data = csv.reader(open(fname).readlines()[2:])
    for dat in data:
        run[dat[2]] = dat
    return run

def main():
    root = os.getcwd()
    machine = input("Enter the machine to get data for: ")
    test_foldr = input("Enter the folder containing all test data: ")

    foldr = root + "/data/" + machine + "/" + test_foldr "/"

    data = dict()

    # get list of compiler folders
    compilers = list(filter(isdir, os.listdir(foldr)))
    for c in compilers:
        data[c] = dict()
        # get list of flag folders
        flags = list(filter(isdir, os.listdir(foldr + c)))
        for f in flags:
            data[c][f] = dict()
            
            for pf in [True, False]:
                # get all csv files with stat data
                stats = list(filter(lambda x: x[-3:] = "csv", 
                                    os.listdir(foldr + c + "/" + f + "/" + str(pf))
                                    ))
                data[c][f][pf] = [read_data(f) for f in stats]

    # data should now exist
    # access via data[compiler][flag][prefetch bool][index][desired data field]




