#!/usr/bin/env python
# D. Jones - 1/14/14
"""This code is from the IDL Astronomy Users Library"""

from astropy.io import fits
from astropy.nddata import Cutout2D
import numpy as np
import getpsf
import aper

# load FITS image and specify PSF star coordinates
image = fits.getdata('stacked.fit')
xpos, ypos = np.array([1450, 1400]), np.array([1550, 1600])
# run aper to get mags and sky values for specified coords
mag, magerr, flux, fluxerr, sky, skyerr, badflag, outstr = \
    aper.aper(image, xpos, ypos, phpadu=1, apr=5, zeropoint=25,
              skyrad=[40, 50], badpix=[-12000, 60000], exact=True)
# use the stars at those coords to generate a PSF model
gauss, psf, psfmag = \
    getpsf.getpsf(image, xpos, ypos,
                  mag, sky, 1, 1, np.arange(len(xpos)),
                  5, 'output_psf.fits')