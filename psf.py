#!/usr/bin/env python
# D. Jones - 1/14/14
"""This code is from the IDL Astronomy Users Library"""

from astropy.io import fits
from astropy.nddata import Cutout2D
import numpy as np
import getpsf
import aper
from find import find
import matplotlib.pyplot as plt

# load FITS image and specify PSF star coordinates
data = fits.getdata('stacked.fit')
i,j = np.unravel_index(data.argmax(), data.shape)
image = Cutout2D(data, (j, i), size = 200).data

amp = np.max(image)
ypix, xpix = np.where(image == amp)
x_range = np.take(image, ypix[0], axis=0)
y_range = np.take(image, xpix[0], axis=1)
half_max = amp / 2
d_x = x_range - half_max
d_y = y_range - half_max
indices_x = np.where(d_x > 0)[0]
indices_y = np.where(d_y > 0)[0]

width_x = len(indices_x)
width_y= len(indices_y)

fwhm = (width_x+width_y)/2

rms = (np.std(image-image.mean(axis=0)))

x,y,flux,sharp,round = find(image,fwhm=fwhm,hmin=rms*3,verbose=False)

xpos,ypos = x,y

# run aper to get mags and sky values for specified coords
mag, magerr, flux, fluxerr, sky, skyerr, badflag, outstr = \
    aper.aper(image, xpos, ypos, phpadu=1, apr=5, zeropoint=25,
              skyrad=[40, 50], badpix=[0, 70000], exact=True)
# use the stars at those coords to generate a PSF model
gauss, psf, psfmag = \
    getpsf.getpsf(image, xpos, ypos,
                  mag, sky, 1, 1, np.arange(len(xpos)),
                  fitrad=60, psfname='output_psf.fits',psfrad=70)

# plt.plot(gauss)
# plt.show()
# data = fits.open('output_psf.fits')[0].data
# plt.imshow(data, cmap='gray', vmin=2.e3, vmax=3.e3)
# plt.colorbar()
# plt.show()

