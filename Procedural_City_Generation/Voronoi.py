import numpy
import random
import pygame
from scipy.spatial import Voronoi
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from math import sqrt
import HomeCreator as hc

def __generate_voronoi(w,h):
    #denstity = 9999
    #denstity = 48000
    denstity = 34000

    point_arr = numpy.zeros([denstity, 2], numpy.uint16)

    for i in range(denstity):
        point_arr[i][0] = numpy.uint16(random.randint(0, w+100))
        point_arr[i][1] = numpy.uint16(random.randint(0, h+100))

    return Voronoi(point_arr)


def draw_voronoi(pygame_surface,height,area):
    w, h = pygame_surface.get_size()
    vor = __generate_voronoi(w,h)
    for indx_pair in vor.ridge_vertices:
        if -1 not in indx_pair:
            start_pos = vor.vertices[indx_pair[0]]
            end_pos = vor.vertices[indx_pair[1]]
            if(checkObsticle(height,end_pos,start_pos,h,w,area)):
                pygame.draw.line(pygame_surface, (0, 0, 0), end_pos, start_pos,3)
    parcels = getMiddleOfRegion(vor,height,area,w,h)
    drawBuildings(parcels,pygame_surface)


def checkObsticle(height,end_pos,start_pos,h,w,area):
    skalarW=w/len(height)
    skalarH=h/len(height[0])
    if(abs(end_pos[0])>=w or abs(end_pos[1])>=h or abs(start_pos[0])>=w or abs(start_pos[1])>=h):
        return False
    if(inShape(area,start_pos,end_pos)==False):
        return False
    if(height[int(start_pos[0]/skalarW),int(start_pos[1]/skalarH)]>=0.33 and height[int(end_pos[0]/skalarW),int(end_pos[1]/skalarH)]>=0.33 and height[int(start_pos[0]/skalarW),int(start_pos[1]/skalarH)]<=0.8 and height[int(end_pos[0]/skalarW),int(end_pos[1]/skalarH)]<=0.8):
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
    for figure in nodes:
        poligon=Polygon(figure)
        if(poligon.contains(Point(pointA))==True and poligon.contains(Point(pointB))==True):
            return True  
    return False

def find(item,array):
    for x in array:
        if(item[0]==x[0]):
            if(item[1]==x[1]):
                return True
    return False

def getRandomArea(max):
    area=[]
    nodes=random.randint(3,15)
    for i in range(nodes):
        x = random.randint(1,max[0])
        y = random.randint(1,max[1])
        point=(x,y)
        area.append(point)
    return area

def getMiddleOfRegion(vor,height,area,w,h):
    buildings=[]
    points=vor.points
    for point in points:
       if(checkPoint(height,area,w,h,point)):
           buildings.append(point)
    return buildings

def checkPoint(height,area,w,h,point):
    skalarW=w/len(height)
    skalarH=h/len(height[0])
    log=False
    if(abs(point[0])>=w or abs(point[1])>=h):
        return False
    for figure in area:
        poligon=Polygon(figure)
        if(poligon.contains(Point(point))==True):
            log = True
            break
    if(log==False):
        return False
    if(height[int(point[0]/skalarW),int(point[1]/skalarH)]>=0.33  and height[int(point[0]/skalarW),int(point[1]/skalarH)]<=0.8):
        return True
    return False

def drawBuildings(points,surface):
    for point in points:
        hc.setBuildingOnPoint(point,surface)