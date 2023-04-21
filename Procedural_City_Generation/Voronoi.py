import numpy
import random
import pygame
from scipy.spatial import Voronoi
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

def __generate_voronoi():
    """
    Randomly chooses various points within the x and y dimensions of the map.
    Then, uses SciPy to generate a voronoi diagram with them, and returns it.

    :return: SciPy voronoi diagram
    """
    denstity = 19900
    point_arr = numpy.zeros([denstity, 2], numpy.uint16)

    for i in range(denstity):
        point_arr[i][0] = numpy.uint16(random.randint(0, 1600))
        point_arr[i][1] = numpy.uint16(random.randint(0, 900))

    return Voronoi(point_arr)


def draw_voronoi(pygame_surface,height,area):
    # generate voronoi diagram
    vor = __generate_voronoi()
    w, h = pygame_surface.get_size()
    print("here is size:")
    print(w)
    print(h)
    # draw all the edges
    #area = [(400.83, 50.55), (430.23, 60.13), (460.97, 120.85), (440.44, 100.45)]

    for indx_pair in vor.ridge_vertices:
        if -1 not in indx_pair:
            start_pos = vor.vertices[indx_pair[0]]
            end_pos = vor.vertices[indx_pair[1]]
            if(checkObsticle(height,end_pos,start_pos,h,w,area)):
                pygame.draw.line(pygame_surface, (0, 0, 0), end_pos, start_pos)

#__generate_voronoi()


def checkObsticle(height,end_pos,start_pos,h,w,area):
    skalar=9
    if(abs(end_pos[0])>=w or abs(end_pos[1])>=h or abs(start_pos[0])>=w or abs(start_pos[1])>=h):
        return False
    if(inShape(area,start_pos,end_pos)==False):
        return False
    if(height[int(start_pos[0]/skalar),int(start_pos[1]/skalar)]>=0.4 and height[int(end_pos[0]/skalar),int(end_pos[1]/skalar)]>=0.4 and height[int(start_pos[0]/skalar),int(start_pos[1]/skalar)]<=0.8 and height[int(end_pos[0]/skalar),int(end_pos[1]/skalar)]<=0.8):
        return True
    return False

def inequality(point,linearBigger,linearSmaller):
    for i in linearBigger:
        if(point[1] > point[0]*i[0]+i[1]):
           return False
    for i in linearSmaller:
        if(point[1] < point[0]*i[0]+i[1]):
           return False
    return True


def inShape(nodes,pointA,pointB):
    poligon=Polygon(nodes)
    if(poligon.contains(Point(pointA))==False):
        return False
    if(poligon.contains(Point(pointB))==False):
        return False
    return True

