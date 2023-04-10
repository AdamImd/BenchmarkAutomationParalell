#! /bin/env python3 
# analysis.py
# tranverses the directory structure created by run.py and constructs a data table
# then enables data analysis on the data such as by creating plots

import os, csv
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def plot_data(data, max):
    # Input data is a np array of floats in shape (frames, n, n)
    # Crete an animation looping through the frames
    fig = plt.figure()
    ims = []
    for frame in data:
        im = plt.imshow(frame, animated=True, vmin=0, vmax=max)
        ims.append([im])
    ani = animation.ArtistAnimation(fig, ims, interval=200, blit=True,
                                    repeat_delay=4000)
    plt.show()
    save_animation(ani)

def save_animation(ani):
    # Save the animation as a mp4 file
    Writer = animation.writers['ffmpeg']
    writer = Writer(fps=5, metadata=dict(artist='Me'), bitrate=1800)
    ani.save('/tmp/animation.mp4', writer=writer)

def main():
    max = 0
    all_kernels = []
    with open("/tmp/parallel-kernels.txt", "r") as file:
        kernels = csv.reader(file)
        for kernel, name, max_val in kernels:
            print("Kernel: {}".format(name))
            max = int(max_val)
            all_data = []
            with open(kernel, "r") as kernel_file:
                filepaths = csv.reader(kernel_file)
                for filepath, time in filepaths:
                    print(filepath)
                    data = []
                    try:
                        with open(filepath, "r") as csvfile:
                            reader = csv.reader(csvfile)
                            for row in reader:
                                row = row[:-1]
                                data.append([float(x) for x in row])
                        all_data.append(data)
                    except:
                        print("Error reading file: {}".format(filepath))
                        break
                all_kernels.append(all_data)

    for kernel in all_kernels:
        plot_data(np.array(kernel), max)



if __name__ == "__main__":
    main()