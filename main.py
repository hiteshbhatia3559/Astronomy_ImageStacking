from astropy.io import fits
from astropy.nddata import Cutout2D
import numpy as np
import matplotlib.pyplot as plt
from PIL import ImageChops
import os
from statistics import mean


def get_data(path_to_files):  # Get data from each file in dir
    print("Getting data...\n")
    filenames = os.listdir(path_to_files)
    dataset = dict()
    for file in filenames:
        try:
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
            ypix, xpix = np.where(main_data == amp)
            x_range = np.take(main_data, ypix[0], axis=0)
            y_range = np.take(main_data, xpix[0], axis=1)
            half_max = amp / 2
            d_x = x_range - half_max
            d_y = y_range - half_max
            indices_x = np.where(d_x > 0)[0]
            indices_y = np.where(d_y > 0)[0]

            # FMHM in x and y - simply counts how many pixels are within half the max in both directions
            width_x = len(indices_x)
            width_y = len(indices_y)
            QF = mean_value / ((width_x + width_y) / 2)
            print("Quality Factor of {} is {}\n".format(QF, file))
            dataset[file] = (file, QF)
        except:
            print("Skipped " + file + " because it did not open or data was corrupted!")

    return dataset


def max_value(array):
    maximums = []
    for item in array:
        if (max(item) < 20000):
            maximums.append(max(item))
    return maximums


def find_best_fit(image_concat,max_values):
    print("Finding best fit for alignment, this is a long process, please wait!\n")
    print("A "+str(len(image_concat)))
    print("B " + str(len(max_values)))
    final_image = np.zeros(shape=image_concat[0].shape)
    x = list(range(-4, 4))
    x.remove(0)
    y = list(range(-4, 4))
    y.remove(0)
    list_of_finals = dict()
    for a in x:
        for b in y:
            i = 0
            for image in image_concat:
                delta = max_values[0].index(max(max_values[0])) - max_values[i].index(max(max_values[i]))
                # print(delta)
                new_image = np.roll(image, [int(delta / a), int(delta / b)], axis=(0, 1))
                print(new_image)
                final_image += new_image
                i += 1
            list_of_finals[max(max_value(final_image))] = final_image

    print(list_of_finals.keys())
    peak_image_brightness = max(list(list_of_finals.keys()))
    # print(peak_image_brightness)
    fitted_final_image = list_of_finals[peak_image_brightness]
    return fitted_final_image


if __name__ == '__main__':

    # EDIT PATH HERE
    path_to_files = './Iota Cancri - Binary System-20190405T043457Z-001/Iota Cancri - Binary System/'

    dataset = get_data(path_to_files)

    print("All QFs calculated\n")

    sorted_list = sorted(list(dataset.values()), key=lambda x: x[1])

    files_to_merge = sorted_list[int(len(sorted_list) * (4 / 5)):]

    print("Top 20% images picked\nMerging now...\n")

    filenames = []
    # Get all filenames in the folder
    for item in files_to_merge:
        x, y = item
        filenames.append(x)

    # Make a list of all 2d arrays that are images
    image_concat = []
    max_values = []
    for image in filenames:
        image_data = fits.getdata(path_to_files + image)
        image_concat.append(image_data)
        max_values.append(max_value(image_data))

    # Making a template array that is blank

    final_image = find_best_fit(image_concat,max_values)

    # ONLY USABLE IN JUPYTER/PYCHARM
    # SEE WHAT THE MERGED IMAGE LOOKS LIKE

    plt.imshow(final_image, cmap='gray', vmin=2.e3, vmax=3.e3)
    plt.colorbar()
    plt.show()

    # outfile = "stacked.fit"
    # hdu = fits.PrimaryHDU(final_image)
    # hdu.writeto(outfile, overwrite=True)
    # print("Please see {} for output".format(outfile))
    # # Prints final file
