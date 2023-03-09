from perlin_noise import PerlinNoise
import Terrains as tr

def GenerateData(base_octave, base_frequency, depth, xpix, ypix):
    octaves_tab = []
    for i in range(3):
        octaves_tab.append(PerlinNoise(octaves=base_octave*(pow(4, i))))

    pic = []
    for i in range(xpix):
        row = []
        for j in range(ypix):
            noise_val = 0
            for k in range(len(octaves_tab)):
                noise_val += octaves_tab[k]([base_frequency *i/xpix, base_frequency*j/ypix])
            row.append(noise_val)
        pic.append(row)
    pic = pow(tr.NormalizeData(pic, 0, 1), depth)
    return pic