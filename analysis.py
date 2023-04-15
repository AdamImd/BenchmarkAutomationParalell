#! /bin/env python3 
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
        im = plt.imshow(np.asarray(frame)[1:-1,1:-1], animated=True, vmin=0, vmax=max)
        ims.append([im])
    ani = animation.ArtistAnimation(fig, ims, interval=100, blit=True,
                                    repeat_delay=4000)
    plt.show()

def save_animation(ani):
    # Save the animation as a mp4 file
    Writer = animation.writers['ffmpeg']
    writer = Writer(fps=5, metadata=dict(artist='Me'), bitrate=1800)
    ani.save('/tmp/animation.mp4', writer=writer)

def analyze():
    with open("/tmp/parallel-kernels.txt", "r") as file:
        kernels = csv.reader(file)
        for kernel, name, max_val in kernels:
            #print("Kernel: {}".format(name))
            kernel_data = []
            kernel_cycles = []
            kernel_micros = []
            with open(kernel, "r") as kernel_file:
                filepaths = csv.reader(kernel_file)
                for filepath, cycles, micros, acc in filepaths:
                    #print("Seconds: {}; Cycles: {}; Acc: {}".format(int(micros)/1000000.0, cycles, acc))
                    data = []
                    times_cycles = []
                    times_micros = []
                    with open(filepath, "r") as csvfile:
                        reader = csv.reader(csvfile)
                        for row in reader:
                            row = row[:-1]
                            data.append([float(x) for x in row])
                            times_micros.append(micros)
                            times_cycles.append(cycles)
                    kernel_data.append(data)
                    kernel_cycles.append(times_cycles)
                    kernel_micros.append(times_micros)
            return (kernel_cycles, kernel_micros, kernel_data)



if __name__ == "__main__":
    analyze()