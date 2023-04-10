#! /bin/env python3 
# analysis.py
# tranverses the directory structure created by run.py and constructs a data table
# then enables data analysis on the data such as by creating plots

import os, csv
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def plot_data(data):
    # Input data is a np array of floats in shape (frames, n, n)
    # Crete an animation looping through the frames
    fig = plt.figure()
    ims = []
    for frame in data:
        im = plt.imshow(frame, animated=True)
        ims.append([im])
    ani = animation.ArtistAnimation(fig, ims, interval=50, blit=True,
                                    repeat_delay=4000)
    plt.show()
    save_animation(ani)

def save_animation(ani):
    # Save the animation as a mp4 file
    Writer = animation.writers['ffmpeg']
    writer = Writer(fps=15, metadata=dict(artist='Me'), bitrate=1800)
    ani.save('animation.mp4', writer=writer)

def main():
    all_data = []
    with open("/tmp/parallel-names.txt", "r") as file:
        filepaths = file.read().splitlines()
        for filepath in filepaths:
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
    plot_data(np.array(all_data))



if __name__ == "__main__":
    main()