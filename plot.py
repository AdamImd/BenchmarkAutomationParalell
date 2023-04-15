#!/usr/bin/env python3
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pickle
from analysis import plot_data


def convert_im():
    with open("./data/all_data.pickle", "rb") as file:
        all_data = pickle.load(file)
    
    plot_data = {}
    for data in all_data:
        if data['setting'][0] not in plot_data: # KERNEL
            plot_data[data['setting'][0]] = {}
        if data['setting'][1] not in plot_data[data['setting'][0]]: # DIMENSION
            plot_data[data['setting'][0]][data['setting'][1]] = {}
        if data['setting'][2] not in plot_data[data['setting'][0]][data['setting'][1]]: # PRECISION
            plot_data[data['setting'][0]][data['setting'][1]][data['setting'][2]] = {}
        
        cycles = []
        for cycle in data['cycles']:
            cycles.append(cycle[0])

        micros = []
        for micro in data['micros']:
            micros.append(micro[0])

        plot_data[data['setting'][0]][data['setting'][1]][data['setting'][2]][data['setting'][3]] = {
            'perf': data['perf'], # PERF stats
            'cycles': cycles, # Times / Iterations
            'micros': micros, # Times / Iterations
            'raw': data['raw'], # Raw images
        }
    
    print(plot_data.keys())

    with open("./data/plot_data_im.pickle", "wb") as file:
        pickle.dump(plot_data, file)


def convert():
    with open("./data/all_data.pickle", "rb") as file:
        all_data = pickle.load(file)
    
    plot_data = {}
    for data in all_data:
        if data['setting'][0] not in plot_data: # KERNEL
            plot_data[data['setting'][0]] = {}
        if data['setting'][1] not in plot_data[data['setting'][0]]: # DIMENSION
            plot_data[data['setting'][0]][data['setting'][1]] = {}
        if data['setting'][2] not in plot_data[data['setting'][0]][data['setting'][1]]: # PRECISION
            plot_data[data['setting'][0]][data['setting'][1]][data['setting'][2]] = {}
        
        cycles = []
        for cycle in data['cycles']:
            cycles.append(cycle[0])

        micros = []
        for micro in data['micros']:
            micros.append(micro[0])

        plot_data[data['setting'][0]][data['setting'][1]][data['setting'][2]][data['setting'][3]] = {
            'perf': data['perf'], # PERF stats
            'cycles': cycles, # Times / Iterations
            'micros': micros, # Times / Iterations
           #'raw': data['raw'], # Raw images
        }
    
    print(plot_data.keys())

    with open("./data/plot_data.pickle", "wb") as file:
        pickle.dump(plot_data, file)




def main():
    # convert()
    # convert_im()
    # exit()

    if(True): # False for images
        with open("./data/plot_data.pickle", "rb") as file:
            plot_data = pickle.load(file)
    else:
        with open("./data/plot_data_im.pickle", "rb") as file:
            plot_data = pickle.load(file)
    
    kernel = 0
    precision = 0.05
    for dim in plot_data[kernel]:
        print(dim)
        x = []
        y = []
        for max_value in plot_data[kernel][dim][precision]:
            x.append(dim)
            print(np.average(plot_data[kernel][dim][precision][max_value]['cycles']))
            y.append(np.average(plot_data[kernel][dim][precision][max_value]['cycles']))
        plt.plot(x, y, label=dim)





if __name__ == "__main__":
    main()