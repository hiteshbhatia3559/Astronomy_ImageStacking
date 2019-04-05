from astropy.io import fits
import numpy as np
import matplotlib.pyplot as plt
import os
from statistics import mean


def get_data(path_to_files):  # Get data from each file in dir
    filenames = os.listdir(path_to_files)
    dataset = dict()
    for file in filenames:
        try:  # print(file)
            image_file = fits.open(path_to_files + file)
            main_data = image_file[0].data
            # in general, QF = mean(max(of each row))/mean of FWHM of x and y
            # mean of maxs of each row
            maxs = []
            for item in main_data:
                maxs.append(max(item))
            mean_value = mean(maxs)
            # FWHM
            amp = np.max(main_data)
            ypix, xpix = np.where(main_data==amp)
            x_range = np.take(main_data,ypix[0],axis=0)
            y_range = np.take(main_data, xpix[0], axis=1)
            half_max = amp/2
            d_x = x_range - half_max
            d_y = y_range - half_max
            indices_x = np.where(d_x > 0)[0]
            indices_y = np.where(d_y > 0)[0]

            # FMHM in x and y - simply counts how many pixels are within half the max in both directions
            width_x = len(indices_x)
            width_y = len(indices_y)
            QF = mean_value/((width_x+width_y)/2)
            dataset[file] = (file,QF)
        except:
            print("Skipped " + file + " because it did not open!")

    return dataset


path_to_files = './Iota Cancri - Binary System-20190405T043457Z-001/Iota Cancri - Binary System/'

dataset = get_data(path_to_files)

for item in list(dataset.values()):
    print(item)