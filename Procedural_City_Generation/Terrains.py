import numpy as np
import random


def NormalizeData(data, minimum, maximum):
    return (maximum-minimum)*((data - np.min(data)) / (np.max(data) - np.min(data)))+minimum


def MakeMountains(pic):
    pic = NormalizeData(pic, 0.5, 1)
    current_row_mid_pixel = 2
    for i in range(len(pic[0])):
        current_collumn_mid_pixel = 2
        for j in range(len(pic)):
            pic[j][i] = pow(pic[j][i], 0.7)
            current_collumn_mid_pixel += 3
        current_row_mid_pixel += 3
    return pic


def MakeLowlands(pic):
    pic = NormalizeData(pic, 0.3, 0.8)
    current_row_mid_pixel = 2
    for i in range(len(pic[0])):
        current_collumn_mid_pixel = 2
        for j in range(len(pic)):
            if 0.33 <= pic[j][i] < 0.40:
                pic[j][i] = pow(pic[j][i], 0.88)
            current_collumn_mid_pixel += 3
        current_row_mid_pixel += 3
    return pic


def MakeIsland(pic, x_size, y_size):
    current_row_mid_pixel = 2
    for i in range(len(pic[0])):
        current_collumn_mid_pixel = 2
        for j in range(len(pic)):
            d = 1 - ((1-pow(2*(current_collumn_mid_pixel-x_size*3/2)/(x_size*3), 2))
                     * (1-pow(2*(current_row_mid_pixel-y_size*3/2)/(y_size*3), 2)))
            pic[j][i] = (pic[j][i] + (1-d)) / 2
            current_collumn_mid_pixel += 3
        current_row_mid_pixel += 3
    return NormalizeData(pic, 0, 1)


def MakeIslands(pic):
    current_row_mid_pixel = 2
    for i in range(len(pic[0])):
        current_collumn_mid_pixel = 2
        for j in range(len(pic)):
            pic[j][i] = pow(pic[j][i], 2)
            current_collumn_mid_pixel += 3
        current_row_mid_pixel += 3
    return pic


def MakeBigForest(pic, moisture):
    pic = NormalizeData(pic, 0.15, 0.8)
    moisture = NormalizeData(moisture, 0.35, 1)
    current_row_mid_pixel = 2
    for i in range(len([pic[0]])):
        current_collumn_mid_pixel = 2
        for j in range(len(pic)):
            if 0.15 <= pic[j][i] <= 0.33:
                pic[j][i] = pow(pic[j][i], 0.8)
            if 0.33 <= pic[j][i] <= 0.4:
                pic[j][i] = pow(pic[j][i], 0.5)
            current_collumn_mid_pixel += 3
        current_row_mid_pixel += 3
    return pic, moisture


def MakeDesert(pic, moisture):
    pic = NormalizeData(pic, 0.3, 1)
    moisture = NormalizeData(moisture, 0, 0.25)
    current_row_mid_pixel = 2
    for i in range(len(pic[0])):
        current_collumn_mid_pixel = 2
        for j in range(len(pic)):
            if 0.33 <= pic[j][i] < 0.4:
                pic[j][i] = pow(pic[j][i], 0.87)
                if pic[j][i] < 0.4:
                    pic[j][i] += 0.02
                    moisture[j][i] = 0.4
            if pic[j][i] >= 0.4:
                pic[j][i] = pow(pic[j][i], 0.8)
            current_collumn_mid_pixel += 3
        current_row_mid_pixel += 3
    return NormalizeData(pic, 0.3, 1), moisture


def MakeSwamp(pic, moisture):
    pic = NormalizeData(pic, 0.28, 0.8)
    current_row_mid_pixel = 2
    for i in range(len(pic[0])):
        current_collumn_mid_pixel = 2
        for j in range(len(pic)):
            if 0.33 <= pic[j][i] < 0.4:
                moisture[j][i] = 0.6
            if 0.4 <= pic[j][i] < 0.7:
                if 0.55 <= moisture[j][i] < 0.8:
                    moisture[j][i] = pow(moisture[j][i], 0.6)
                moisture[j][i] = pow(moisture[j][i], 0.6)
            current_collumn_mid_pixel += 3
        current_row_mid_pixel += 3
    return pic, moisture
