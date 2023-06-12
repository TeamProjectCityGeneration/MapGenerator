import pygame
import random
import math
import numpy
from scipy.spatial import distance

# Definicje kolorów
DEEP_SEA = 0x0c1fb3  # Ciemnoniebieski
SHALLOW_SEA = 0x0c54b3  # Jasnoniebieski
WARM_WATERS = 0x18a7c7  # Błękitny
BEACH = 0xdeddb1  # Bladożółty
FROZEN_BEACH = 0xeaf0dd
PLAINS = 0x8ede7a  # Bladozielony
FROZEN_PLAINS = 0xccf5cb
DESERT = 0xd1ce58  # Żółty
SHRUBLAND = 0x57b837  # Zielony
SWAMP = 0x1B8E6B  # Ciemnobłękitny
FOREST = 0x1a5716  # Ziemnozielony
FROZEN_FOREST = 0x98b897
WASTELAND = 0xC15A1B  # Brudnopomarańczowy
HIGHLANDS = 0xc9b265  # Lekko brązowy
FROZEN_HIGHLANDS = 0xc4ba99
HIGHFOREST = 0x3c5c34  # Khaki???
MOUNTAINS = 0x707070  # Szary
SNOW = 0xffffff  # Śnieg
FROZEN_WATER = 0x8ea8d1  # Zamrożona woda
TREE = 0x000000  # Czarne kropki
CITY = 0xff0000  # Czerwony
ROUTE = 0xffaa00  # Pomarańczowy jasny

global MULTIPLIER

def set_multiplier(value):
    global MULTIPLIER
    MULTIPLIER = value

def colorize(height_map, moisture_map, cold_map, pygame_screen):
    upper = math.ceil(MULTIPLIER/2)
    lower = math.floor(MULTIPLIER/2)
    row_mid_pixel = upper
    for i in range(len(height_map[0])):  # X
        collumn_mid_pixel = upper
        for j in range(len(height_map)):  # Y
            #possible_tree = random.randint(0, 99)
            # Ocean
            #print(collumn_mid_pixel-lower, row_mid_pixel-lower, collumn_mid_pixel+lower, row_mid_pixel+lower)
            if 0 <= height_map[j][i] < 0.15:
                pygame.draw.rect(pygame_screen, DEEP_SEA, pygame.Rect(
                    collumn_mid_pixel-lower, row_mid_pixel-lower, collumn_mid_pixel+lower, row_mid_pixel+lower))
                if cold_map[j][i] > 0.9:
                    pygame.draw.rect(pygame_screen, FROZEN_WATER, pygame.Rect(
                        collumn_mid_pixel-lower, row_mid_pixel-lower, collumn_mid_pixel+lower, row_mid_pixel+lower))
            if 0.15 <= height_map[j][i] < 0.33:
                if moisture_map[j][i] < 0.7:
                    pygame.draw.rect(pygame_screen, SHALLOW_SEA, pygame.Rect(
                        collumn_mid_pixel-lower, row_mid_pixel-lower, collumn_mid_pixel+lower, row_mid_pixel+lower))
                if moisture_map[j][i] >= 0.7:
                    pygame.draw.rect(pygame_screen, WARM_WATERS, pygame.Rect(
                        collumn_mid_pixel-lower, row_mid_pixel-lower, collumn_mid_pixel+lower, row_mid_pixel+lower))
                if cold_map[j][i] > 0.8:
                    pygame.draw.rect(pygame_screen, FROZEN_WATER, pygame.Rect(
                        collumn_mid_pixel-lower, row_mid_pixel-lower, collumn_mid_pixel+lower, row_mid_pixel+lower))            
            # Plaże
            if 0.33 <= height_map[j][i] < 0.40:
                if moisture_map[j][i] < 0.5:
                    pygame.draw.rect(pygame_screen, BEACH, pygame.Rect(
                        collumn_mid_pixel-lower, row_mid_pixel-lower, collumn_mid_pixel+lower, row_mid_pixel+lower))
                    if cold_map[j][i] > 0.8:
                        pygame.draw.rect(pygame_screen, FROZEN_BEACH, pygame.Rect(
                            collumn_mid_pixel-lower, row_mid_pixel-lower, collumn_mid_pixel+lower, row_mid_pixel+lower))
                    #if possible_tree >= 98:
                    #    pygame.draw.rect(pygame_screen, TREE, pygame.Rect(
                    #        collumn_mid_pixel, row_mid_pixel, collumn_mid_pixel, row_mid_pixel))
                if moisture_map[j][i] >= 0.5:
                    pygame.draw.rect(pygame_screen, SWAMP, pygame.Rect(
                        collumn_mid_pixel-lower, row_mid_pixel-lower, collumn_mid_pixel+lower, row_mid_pixel+lower))
                    if cold_map[j][i] > 0.8:
                        pygame.draw.rect(pygame_screen, FROZEN_PLAINS, pygame.Rect(
                            collumn_mid_pixel-lower, row_mid_pixel-lower, collumn_mid_pixel+lower, row_mid_pixel+lower))
                    #if possible_tree >= 75:
                    #    pygame.draw.rect(pygame_screen, TREE, pygame.Rect(
                    #        collumn_mid_pixel, row_mid_pixel, collumn_mid_pixel, row_mid_pixel))
            # Niziny
            if 0.40 <= height_map[j][i] < 0.70:
                if moisture_map[j][i] < 0.1:
                    pygame.draw.rect(pygame_screen, WASTELAND, pygame.Rect(
                        collumn_mid_pixel-lower, row_mid_pixel-lower, collumn_mid_pixel+lower, row_mid_pixel+lower))
                if 0.1 <= moisture_map[j][i] < 0.25:
                    pygame.draw.rect(pygame_screen, DESERT, pygame.Rect(
                        collumn_mid_pixel-lower, row_mid_pixel-lower, collumn_mid_pixel+lower, row_mid_pixel+lower))
                if 0.25 <= moisture_map[j][i] < 0.5:
                    pygame.draw.rect(pygame_screen, PLAINS, pygame.Rect(
                        collumn_mid_pixel-lower, row_mid_pixel-lower, collumn_mid_pixel+lower, row_mid_pixel+lower))
                    if cold_map[j][i] > 0.8:
                        pygame.draw.rect(pygame_screen, FROZEN_PLAINS, pygame.Rect(
                            collumn_mid_pixel-lower, row_mid_pixel-lower, collumn_mid_pixel+lower, row_mid_pixel+lower))
                    #if possible_tree >= 93:
                    #    pygame.draw.rect(pygame_screen, TREE, pygame.Rect(
                    #        collumn_mid_pixel, row_mid_pixel, collumn_mid_pixel, row_mid_pixel))
                if 0.5 <= moisture_map[j][i] < 0.55:
                    pygame.draw.rect(pygame_screen, SHRUBLAND, pygame.Rect(
                        collumn_mid_pixel-lower, row_mid_pixel-lower, collumn_mid_pixel+lower, row_mid_pixel+lower))
                    if cold_map[j][i] > 0.8:
                        pygame.draw.rect(pygame_screen, FROZEN_FOREST, pygame.Rect(
                            collumn_mid_pixel-lower, row_mid_pixel-lower, collumn_mid_pixel+lower, row_mid_pixel+lower))
                    #if possible_tree >= 70:
                    #    pygame.draw.rect(pygame_screen, TREE, pygame.Rect(
                    #        collumn_mid_pixel, row_mid_pixel, collumn_mid_pixel, row_mid_pixel))
                if 0.55 <= moisture_map[j][i] < 0.8:
                    pygame.draw.rect(pygame_screen, FOREST, pygame.Rect(
                        collumn_mid_pixel-lower, row_mid_pixel-lower, collumn_mid_pixel+lower, row_mid_pixel+lower))
                    if cold_map[j][i] > 0.8:
                        pygame.draw.rect(pygame_screen, FROZEN_FOREST, pygame.Rect(
                            collumn_mid_pixel-lower, row_mid_pixel-lower, collumn_mid_pixel+lower, row_mid_pixel+lower))
                    #if possible_tree >= 40:
                    #    pygame.draw.rect(pygame_screen, TREE, pygame.Rect(
                    #        collumn_mid_pixel, row_mid_pixel, collumn_mid_pixel, row_mid_pixel))
                if moisture_map[j][i] >= 0.8:
                    pygame.draw.rect(pygame_screen, FROZEN_PLAINS, pygame.Rect(
                        collumn_mid_pixel-lower, row_mid_pixel-lower, collumn_mid_pixel+lower, row_mid_pixel+lower))
                    if cold_map[j][i] > 0.8:
                        pygame.draw.rect(pygame_screen, SNOW, pygame.Rect(
                            collumn_mid_pixel-lower, row_mid_pixel-lower, collumn_mid_pixel+lower, row_mid_pixel+lower))
                    #if possible_tree >= 70:
                    #    pygame.draw.rect(pygame_screen, TREE, pygame.Rect(
                    #        collumn_mid_pixel, row_mid_pixel, collumn_mid_pixel, row_mid_pixel))
            # Wyżyny
            if 0.70 <= height_map[j][i] < 0.80:
                if moisture_map[j][i] < 0.55:
                    pygame.draw.rect(pygame_screen, HIGHLANDS, pygame.Rect(
                        collumn_mid_pixel-lower, row_mid_pixel-lower, collumn_mid_pixel+lower, row_mid_pixel+lower))
                    if cold_map[j][i] > 0.8:
                        pygame.draw.rect(pygame_screen, FROZEN_HIGHLANDS, pygame.Rect(
                            collumn_mid_pixel-lower, row_mid_pixel-lower, collumn_mid_pixel+lower, row_mid_pixel+lower))
                    #if possible_tree >= 95:
                    #    pygame.draw.rect(pygame_screen, TREE, pygame.Rect(
                    #        collumn_mid_pixel, row_mid_pixel, collumn_mid_pixel, row_mid_pixel))
                if 0.55 <= moisture_map[j][i] < 0.6:
                    pygame.draw.rect(pygame_screen, SHRUBLAND, pygame.Rect(
                        collumn_mid_pixel-lower, row_mid_pixel-lower, collumn_mid_pixel+lower, row_mid_pixel+lower))
                    if cold_map[j][i] > 0.8:
                        pygame.draw.rect(pygame_screen, FROZEN_FOREST, pygame.Rect(
                            collumn_mid_pixel-lower, row_mid_pixel-lower, collumn_mid_pixel+lower, row_mid_pixel+lower))
                    #if possible_tree >= 77:
                    #    pygame.draw.rect(pygame_screen, TREE, pygame.Rect(
                    #        collumn_mid_pixel, row_mid_pixel, collumn_mid_pixel, row_mid_pixel))
                if moisture_map[j][i] >= 0.6:
                    pygame.draw.rect(pygame_screen, HIGHFOREST, pygame.Rect(
                        collumn_mid_pixel-lower, row_mid_pixel-lower, collumn_mid_pixel+lower, row_mid_pixel+lower))
                    if cold_map[j][i] > 0.8:
                        pygame.draw.rect(pygame_screen, FROZEN_FOREST, pygame.Rect(
                            collumn_mid_pixel-lower, row_mid_pixel-lower, collumn_mid_pixel+lower, row_mid_pixel+lower))
                    #if possible_tree >= 60:
                    #    pygame.draw.rect(pygame_screen, TREE, pygame.Rect(
                    #        collumn_mid_pixel, row_mid_pixel, collumn_mid_pixel, row_mid_pixel))
            # Góry
            if height_map[j][i] >= 0.80:
                pygame.draw.rect(pygame_screen, MOUNTAINS, pygame.Rect(
                    collumn_mid_pixel-lower, row_mid_pixel-lower, collumn_mid_pixel+lower, row_mid_pixel+lower))
                if cold_map[j][i] > 0.8:
                    pygame.draw.rect(pygame_screen, SNOW, pygame.Rect(
                        collumn_mid_pixel-lower, row_mid_pixel-lower, collumn_mid_pixel+lower, row_mid_pixel+lower))
                #if possible_tree >= 99:
                #    pygame.draw.rect(pygame_screen, TREE, pygame.Rect(
                #        collumn_mid_pixel, row_mid_pixel, collumn_mid_pixel, row_mid_pixel))
            collumn_mid_pixel += MULTIPLIER
        row_mid_pixel += MULTIPLIER
              
def DrawTree(pygame_screen, height_map, moisture_map, nodes_positions):
    upper = math.ceil(MULTIPLIER/2)
    row_pixel = upper
    for i in range(len(height_map[0])):  # X
        collumn_pixel = upper
        for j in range(len(height_map)):  # Y
            possible_tree = random.randint(0, 99)
            point = numpy.array([(j*MULTIPLIER,i*MULTIPLIER)])
            dist_array = distance.cdist(nodes_positions,point).min(axis=1)
            min = numpy.amin(dist_array)
            if min > 100:
                if 0.33 <= height_map[j][i] < 0.40:
                    if moisture_map[j][i] < 0.5:
                        if possible_tree >= 98:
                            pygame.draw.rect(pygame_screen, TREE, pygame.Rect(collumn_pixel, row_pixel, 6, 6))
                    if moisture_map[j][i] >= 0.5:
                        if possible_tree >= 75:
                            pygame.draw.rect(pygame_screen, TREE, pygame.Rect(collumn_pixel, row_pixel, 6, 6))
                if 0.40 <= height_map[j][i] < 0.70:
                    if 0.25 <= moisture_map[j][i] < 0.5:
                        if possible_tree >= 93:
                            pygame.draw.rect(pygame_screen, TREE, pygame.Rect(collumn_pixel, row_pixel, 6, 6))
                    if 0.5 <= moisture_map[j][i] < 0.55:
                        if possible_tree >= 70:
                            pygame.draw.rect(pygame_screen, TREE, pygame.Rect(collumn_pixel, row_pixel, 6, 6))
                    if 0.55 <= moisture_map[j][i] < 0.8:
                        if possible_tree >= 40:   
                            pygame.draw.rect(pygame_screen, TREE, pygame.Rect(collumn_pixel, row_pixel, 6, 6))
                    if moisture_map[j][i] >= 0.8:
                        if possible_tree >= 80: 
                            pygame.draw.rect(pygame_screen, TREE, pygame.Rect(collumn_pixel, row_pixel, 6, 6))
                if 0.70 <= height_map[j][i] < 0.80:
                    if moisture_map[j][i] < 0.55:
                        if possible_tree >= 95:
                            pygame.draw.rect(pygame_screen, TREE, pygame.Rect(collumn_pixel, row_pixel, 6, 6))
                    if 0.55 <= moisture_map[j][i] < 0.6:
                        if possible_tree >= 77:
                            pygame.draw.rect(pygame_screen, TREE, pygame.Rect(collumn_pixel, row_pixel, 6, 6))
                    if moisture_map[j][i] >= 0.6:
                        if possible_tree >= 60:
                            pygame.draw.rect(pygame_screen, TREE, pygame.Rect(collumn_pixel, row_pixel, 6, 6))
                if height_map[j][i] >= 0.80:
                    if possible_tree >= 99:
                        pygame.draw.rect(pygame_screen, TREE, pygame.Rect(collumn_pixel, row_pixel, 6, 6))
            collumn_pixel += MULTIPLIER
        row_pixel += MULTIPLIER