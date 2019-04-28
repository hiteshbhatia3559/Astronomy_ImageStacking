from astropy.io import fits
import matplotlib.pyplot as plt

data = fits.open('output_psf.fits')[0].data

plt.imshow(data, cmap='gray', vmin=2.e3, vmax=3.e3)
plt.colorbar()
plt.show()