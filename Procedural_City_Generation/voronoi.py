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
    denstity = 9900
    point_arr = numpy.zeros([denstity, 2], numpy.uint16)

    for i in range(denstity):
        point_arr[i][0] = numpy.uint16(random.randint(0, 1600))
        point_arr[i][1] = numpy.uint16(random.randint(0, 900))

    return Voronoi(point_arr)


def draw_voronoi(pygame_surface,height):
    # generate voronoi diagram
    vor = __generate_voronoi()
    w, h = pygame_surface.get_size()
    print(w)
    print("here")
    print(h)
    # draw all the edges
    for indx_pair in vor.ridge_vertices:
        if -1 not in indx_pair:
            start_pos = vor.vertices[indx_pair[0]]
            end_pos = vor.vertices[indx_pair[1]]
            #color = pygame_surface.get_at((int(start_pos[0]),int(start_pos[1])))
            #print(" cordinates ",end_pos[0]," ",end_pos[1]," es ",start_pos[0]," ",start_pos[1]," ")
            sp = (start_pos)
            ep = (end_pos)
            if(checkObsticle(height,ep,sp,h,w)):
                pygame.draw.line(pygame_surface, (0, 0, 0), ep, sp)

#__generate_voronoi()


def checkObsticle(height,end_pos,start_pos,h,w):
    if(abs(end_pos[0])>=w or abs(end_pos[1])>=h or abs(start_pos[0])>=w or abs(start_pos[1])>=h):
        return False
    M = [(1,0)]
    W = [(-1,100)]
    if(inequality(start_pos,M,W)==False or inequality(end_pos,M,W)==False):
        return False
    if(height[int(start_pos[0]/3),int(start_pos[1]/3)]>=0.4 and height[int(end_pos[0]/3),int(end_pos[1]/3)]>=0.4 and height[int(start_pos[0]/3),int(start_pos[1]/3)]<=0.8 and height[int(end_pos[0]/3),int(end_pos[1]/3)]<=0.8):
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
