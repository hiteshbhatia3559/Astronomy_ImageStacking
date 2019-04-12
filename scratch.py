from astropy.io import fits
import numpy as np
import matplotlib.pyplot as plt
from PIL import ImageChops
import os
from statistics import mean
from astropy.nddata import Cutout2D

def max_value(array):
    maximums = []
    for item in array:
        if (max(item) < 20000) and (max(item > 200)):
            maximums.append(max(item))
    return maximums

filenames = ['Autosave Image -0019.fit', 'Autosave Image -0051.fit', 'Autosave Image -0079.fit', 'Autosave Image -0062.fit', 'Autosave Image -0053.fit', 'Autosave Image -0030.fit', 'Autosave Image -0042.fit', 'Autosave Image -0069.fit', 'Autosave Image -0008.fit', 'Autosave Image -0050.fit', 'Autosave Image -0044.fit', 'Autosave Image -0004.fit', 'Autosave Image -0020.fit', 'Autosave Image -0002.fit', 'Autosave Image -0052.fit', 'Autosave Image -0040.fit', 'Autosave Image -0061.fit']
path = 'Iota Cancri - Binary System-20190405T043457Z-001/Iota Cancri - Binary System/'

ran = []

for file in filenames[:4]:
    data = fits.getdata(path+file)
    ran.append(max_value(data))

new = []

for seq in ran:
    delta = ran[0].index(max(ran[0])) - seq.index(max(seq))
    new_seq = np.roll(seq,delta)
    new.append(new_seq)

for item in new:
    plt.plot(item)

plt.show()

