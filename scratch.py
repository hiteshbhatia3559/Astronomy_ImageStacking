from astropy.io import fits
import matplotlib.pyplot as plt

data = fits.open('stacked1.fit')[0].data
data1 = fits.open('output_psf.fits')[0].data

n1, n2 = 0,0
total = 0
for row in data1:
    for item in row:
        if item > 5000:
            n1+=1
        total+=1

print(total/n1)



plt.imshow(data, cmap='gray', vmin=1.e3, vmax=6.e3)
plt.colorbar()
plt.show()