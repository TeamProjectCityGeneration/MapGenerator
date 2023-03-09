import numpy
import random
import pygame
from scipy.spatial import Voronoi


def __generate_voronoi():
    """
    Randomly chooses various points within the x and y dimensions of the map.
    Then, uses SciPy to generate a voronoi diagram with them, and returns it.

    :return: SciPy voronoi diagram
    """

    point_arr = numpy.zeros([900, 2], numpy.uint16)

    for i in range(900):
        point_arr[i][0] = numpy.uint16(random.randint(0, 1600))
        point_arr[i][1] = numpy.uint16(random.randint(0, 900))

    return Voronoi(point_arr)


def draw_voronoi(pygame_surface):
    # generate voronoi diagram
    vor = __generate_voronoi()

    # draw all the edges
    for indx_pair in vor.ridge_vertices:
        start_pos = vor.vertices[indx_pair[0]]
        end_pos = vor.vertices[indx_pair[1]]

        pygame.draw.line(pygame_surface, (0, 0, 0), start_pos, end_pos)

__generate_voronoi()