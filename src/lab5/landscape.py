import matplotlib.pyplot as plt
from perlin_noise import PerlinNoise
import numpy as np

def get_elevation(size):
    xpix, ypix = size
    noise1 = PerlinNoise(octaves=3, seed=19)
    noise2 = PerlinNoise(octaves=6, seed=24)
    noise3 = PerlinNoise(octaves=12, seed=36)
    elevation = []
    for i in range(xpix):
        row = []
        for j in range(ypix):
            noise_val = noise1([i/xpix, j/ypix])
            noise_val += 0.66*noise2([i/xpix, j/ypix])
            noise_val += 0.25*noise3([i/xpix, j/ypix])

            row.append(noise_val)
        elevation.append(row)
    elevation = np.array(elevation)
    '''Play around with perlin noise to get a better looking landscape (This is required for the lab)'''

    return elevation

def elevation_to_rgba(elevation):
    xpix, ypix = np.array(elevation).shape
    colormap = plt.cm.get_cmap('gist_earth')
    elevation = (elevation - elevation.min())/(elevation.max()-elevation.min())
    ''' You can play around with colormap to get a landscape of your preference if you want '''
    landscape = np.array([colormap(elevation[i, j])[0:3] for i in range(xpix) for j in range(ypix)]).reshape(xpix, ypix, 3)*255
    landscape = landscape.astype('uint8')
    return landscape
 

get_landscape = lambda size: elevation_to_rgba(get_elevation(size))


if __name__ == '__main__':
    size = 640, 480
    pic = elevation_to_rgba(get_elevation(size))
    plt.imshow(pic, cmap='gist_earth')
    plt.show()