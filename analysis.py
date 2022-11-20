#! /bin/env python3 
# analysis.py
# tranverses the directory structure created by run.py and constructs a data table
# then enables data analysis on the data such as by creating plots

import os, csv
import matplotlib.pyplot as plt
# used to control the legend colors for bar plots
import matplotlib.colors as mcolors
import matplotlib.patches as mpatches
import statistics

CPUs = [
        "ThinkPadX270", "ThinkPadX61Tablet", "ThinkPadX120e",
        "Latitude7480", "LatitudeE6230", "LatitudeE6400",
        "LatitudeE6500", "LatitudeE7450",
        ]

#CPU = ["ThinkPadX270"] #, "ThinkPadX61Tablet"]
#CPU = ["ThinkPadX120e"]
#CPU = [CPUs[2], CPUs[5], CPUs[6]]
#CPU = [CPUs[4]]
CPU = [CPUs[7]]


def read_data(fname):
    run = {}
    data = csv.reader(open(fname).readlines()[2:])
    for dat in data:
        run[dat[2]] = dat
    return run

'''
    data = dictionary of test data so far
    machine = CPU to add info to data dictionary for
    test_foldr = folder name containing the tests we want data from
Navigates the folder structure and adds data the for given machine and test
    to the data dictionary
'''
def generate_data(data, machine, test_foldr):
    root = os.getcwd()
    m = machine
    
    if m not in data:
        # create a dictionary entry for this machine
        data[m] = dict()

    foldr = root + "/data/" + machine + "/" + test_foldr + "/"

    # get list of compiler folders
    compilers = list(filter(lambda p: os.path.isdir(foldr + p), os.listdir(foldr)))
    for c in compilers:
        data[m][c] = dict()
        cpath = foldr + c + "/"
        # get list of flag folders
        flags = list(filter(lambda p: os.path.isdir(cpath + p), os.listdir(cpath)))
        for f in flags:
            data[m][c][f] = dict()
            fpath = cpath + f + "/"
            
            for pf in [True, False]:
                # get all csv files with stat data
                stats = list(filter(lambda x: x[-3:] == "csv", os.listdir((fpath + str(pf)))))
                        
                data[m][c][f][pf] = [read_data(fpath + str(pf) + "/" + fname) for fname in stats]
    
    return data

'''
    data = dictionary of test data indexed as
        data[machine][compiler][flag][prefetch bool][index][desired data field]
        e.g., data["ThinkPadX270"]["gcc"]["-O0"][True][4]["branch-misses"]
    x_cat = category to plot on the x axis
    y_cat = category to plot on the y axis
        BOTH should be generated by perf and we are plotting y vs x
    machines = list of machines to plot this data for
    test_name = name of this test, only used to distinguish the plot
    pf = boolean, indicates whether we want to compare for prefetch on/off
        (only use prefetcher off if this is false)
    flags = list of flags to use for all CPUs and compilers, or None to use them all
    save = boolean, indicates whether we want to save the plot to a file
Uses the data dictionary to generate a plot of some desired data
If saving a plot, uses a standard format and saves to plot_data
'''
def generate_plots(data, x_cat, y_cat, machines, test_name, pf = True, flags = None, save = True):
    #x_cat = 'L1-dcache-loads'
    #y_cat = 'L1-dcache-load-misses'
    plt.figure(figsize=(7,7))
    # check the number of machines so we don't print the machine if only 1
    one_m = len(machines) == 1
    # to build up the legend as we go
    legend_list = []
    
    for m in machines:
        for c in data[m]:
            fs = (data[m][c] if flags == None else flags)
            for f in fs:
                pfs = (data[m][c][f] if pf else ["False"])
                for p in pfs:
                    # [:-1] --> exclude the multi from the data to plot
                    to_plot = data[m][c][f][p][:-1]
                    # get the first value in the CSV, the number for this category,
                    # for each of the x and y datapoints
                    x = list(map(lambda d: float(d[x_cat][0]), to_plot))
                    y = list(map(lambda d: float(d[y_cat][0]), to_plot))
                    plt.scatter(x, y)
                    legend = ""
                    # add the machine to the legend if there are multiple
                    legend += "" if one_m else (m + " ")
                    # add the compiler to the legend if there are multiple
                    legend += c #"" if len(data[m]) == 1 else (" " + c)
                    # add the flag for this test
                    legend += " " + f
                    # add the prefetcher if it matters
                    legend += " w/ PF on" if p == True else (" w/ PF off" if p == False and pf else "")
                    
                    legend_list.append(legend)
    # set up the final plot and show it
    plt.title(y_cat + " vs. " + x_cat + \
              ((" for " + machines[0]) if one_m else ""))
    plt.xlabel(x_cat, fontsize = 20)
    plt.ylabel(y_cat, fontsize = 20)
    plt.legend(legend_list)
    if save:
        ms = "-for-" + "-".join(machines)
        root = os.getcwd()
        plt.savefig(root + "\\plot_data\\" + test_name + "-" + y_cat + "-vs-" + x_cat + ms + ".png")
    plt.show()

'''
    data = dictionary of test data indexed as
        data[machine][compiler][flag][prefetch bool][index][desired data field]
        e.g., data["ThinkPadX270"]["gcc"]["-O0"][True][4]["branch-misses"]
    cat = category to plot for each machine; should be generated by perf
    machines = list of machines to plot this data for
    test_name = name of this test, only used to distinguish the plot
    pf = boolean, indicates whether we want to compare for prefetch on/off
        (only use prefetcher off if this is false)
    flags = list of flags to use for all CPUs and compilers, or None to use them all
    save = boolean, indicates whether we want to save the plot to a file
    legend_on = boolean, indicates whether we want to show an explicit legend with colors
Uses the passed in data dictionary to generate a bar plot for the 
specified machines and categories, with sub-bars for each compiler/setting
'''
def generate_bar_plots(data, cat, machines, test_name, pf = True, flags = None, save = True, legend_on = True):

    # define colors to use for bars for consistency across machines
    #colors = list(mcolors.TABLEAU_COLORS)
    colors = list(mcolors.CSS4_COLORS)
    
    tot_space = 10
    plt.figure(figsize = (tot_space,7))
    space_per_m = tot_space / (2*len(machines))
    locs = [2*i*space_per_m for i in range(len(machines))]
    
    # check the number of machines so we don't print the machine if only 1
    one_m = len(machines) == 1

    # legend for subplots and locations of the bars themselves
    legend_list = []
    minor_labels = []
    minor = []

    for (m, loc) in zip(machines, locs):
        for_this = []
        for c in data[m]:
            fs = (data[m][c] if flags == None else flags)
            for f in fs:
                pfs = (data[m][c][f] if pf else ["False"])
                for p in pfs:
                    # [:-1] --> exclude the multi from the data to plot
                    to_plot = data[m][c][f][p][:-1]
                    # get the first value in the CSV, the number for this category,
                    # for each of the datapoints
                    y = list(map(lambda d: float(d[cat][0]), to_plot))
                    # average the result so we get ONE bar
                    y = statistics.mean(y)
                    legend = ""
                    # add the compiler to the legend
                    legend += c #"" if len(data[m]) == 1 else (" " + c)
                    # add the flag for this test
                    legend += " " + f
                    # add the prefetcher if it matters
                    legend += " w/ PF on" if p == True else (" w/ PF off" if p == False and pf else "")
                    # add the data from this branch
                    # plot for THIS machine
                    for_this.append((legend, y))
                    # overall list of labels
                    minor_labels.append(legend)
            # separator for different compilers
            for_this.append(None)

        # determine how much space to alloc to each sub-bar
        # subtract 1 so we don't add extra space at the end for the last separator
        space_per_setting = space_per_m / (len(for_this) - 1)

        # plot the bars for this machine and track their legend data
        for i in range(len(for_this) - 1):
            # don't put a bar here if at a separator
            if for_this[i] == None:
                continue

            bar_loc = loc - space_per_m / 2 + (i + 1/2) * space_per_setting
            minor.append(bar_loc)
            # only put unique compiler/flag/prefetch settings in the legend
            if not (for_this[i][0] in legend_list):
                legend_list.append(for_this[i][0])
            # correlate color with the unique legend entry
            color = colors[legend_list.index(for_this[i][0])]
            # plot this bar
            plt.bar([bar_loc], [for_this[i][1]], space_per_setting,
                    label = for_this[i][0], color = color, edgecolor = "Black")
            

    plt.title("Comparison of " + cat + \
              ((" for " + machines[0]) if one_m else ""))
    # for testing
    assert(len(locs) == len(machines))
    assert(len(minor) == len(minor_labels))
    #print("Legend list: ", legend_list)
    
    plt.ylabel(cat, fontsize = 20)
    # build the legend based on the unique compiler/flag/prefetch settings tracked
    if legend_on:
        legend_entries = []
        for i in range(len(legend_list)):
            patch = mpatches.Patch(color = colors[i], label = legend_list[i])
            legend_entries.append(patch)
        plt.legend(handles = legend_entries)

    # operate on the axes to show the compiler/flag/prefetch setting under each bar
    ax = plt.gca()
    ax.set_xticks(minor)
    ax.set_xticklabels(minor_labels, fontsize = 8, rotation = "45", ha = 'right')
    # plot the machines at the TOP if there are multiple (couldn't get major/minor to work)
    if not one_m:
        ax2 = ax.twiny()
        ax2.set_xticks(locs)
        ax2.set_xticklabels(machines)
        ax2.set_xlim(ax.get_xlim())
        
    # Tweak spacing to prevent clipping of tick-labels off the bottom of the plot
    plt.subplots_adjust(bottom=0.15)

    # maybe save the plot to a file
    if save:
        ms = "-for-" + "-".join(machines)
        root = os.getcwd()
        plt.savefig(root + "\\plot_data\\" + test_name + "-" + cat + ms + ".png")

    plt.show()


def main():
    root = os.getcwd()
    #machine = input("Enter the machine to get data for: ")
    machine = CPU
    #x_cat = 'L1-dcache-loads'
    x_cat = 'cycles'
    y_cats = [
             'L1-dcache-loads', 'L1-dcache-load-misses', 
             'context-switches', 'L1-icache-load-misses',
             'page-faults', 'cpu-migrations',
             'instructions', 'branch-misses', 'branches',
             'dTLB-loads', 'dTLB-load-misses',
             'iTLB-loads', 'iTLB-load-misses',
             'LLC-loads', 'LLC-load-misses',
             ]

    #test_foldr = input("Enter the folder containing all test data: ")
    test_foldr = "11-15_FFT"

    data = dict()

    for machine in CPU:
        data = generate_data(data, machine, test_foldr)
        
    #for y_cat in y_cats:
    #    generate_plots(data, x_cat, y_cat, CPU, test_foldr)

    #for y_cat in y_cats:
    #    generate_bar_plots(data, y_cat, CPU, test_foldr, legend_on = False)

    # generate_bar_plots(data, 'cycles', CPU, test_foldr, legend_on = False)
    generate_bar_plots(data, 'L1-dcache-load-misses', CPU, test_foldr, legend_on = False)

if __name__ == "__main__":
    main()


