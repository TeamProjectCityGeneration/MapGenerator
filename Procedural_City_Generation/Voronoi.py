import numpy
import random
import pygame
from scipy.spatial import Voronoi
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from math import sqrt

def __generate_voronoi():
    """
    Randomly chooses various points within the x and y dimensions of the map.
    Then, uses SciPy to generate a voronoi diagram with them, and returns it.

    :return: SciPy voronoi diagram
    """
    #denstity = 9999
    denstity = 48000
    point_arr = numpy.zeros([denstity, 2], numpy.uint16)

    for i in range(denstity):
        point_arr[i][0] = numpy.uint16(random.randint(0, 1600))
        point_arr[i][1] = numpy.uint16(random.randint(0, 900))

    return Voronoi(point_arr)


def draw_voronoi(pygame_surface,height,area):
    # generate voronoi diagram
    vor = __generate_voronoi()
    w, h = pygame_surface.get_size()
    #print("here is size:")
    #print(w)
    #print(h)
    # draw all the edges
    #area = [(400.83, 50.55), (430.23, 60.13), (460.97, 120.85), (440.44, 100.45)]
    parcels=[]
    parcel=[]
    for indx_pair in vor.ridge_vertices:
        if -1 not in indx_pair:
            start_pos = vor.vertices[indx_pair[0]]
            end_pos = vor.vertices[indx_pair[1]]
            #print(start_pos, " --> " , end_pos)
            if(checkObsticle(height,end_pos,start_pos,h,w,area)):
                parcels, parcel=ifParcel(parcels,parcel,start_pos,end_pos)
                pygame.draw.line(pygame_surface, (0, 0, 0), end_pos, start_pos)
    #print(parcels)
    #print(parcel)
    drawParcel(parcels,pygame_surface)
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

def ifParcel(parcels,parcel,start_pos,end_pos):
    tmp=[]
    if(len(parcel)<10):
        tmp.append(start_pos)
        tmp.append(end_pos)
        parcel.append(tmp)
    if(len(parcel)>1):
        for i in parcel:
            if(find(start_pos,i)):
                #i.append(start_pos)
                i.append(end_pos)
                parcels.append(i)
                parcel.remove(i)
            elif(find(end_pos,i)):
                i.append(start_pos)
                #i.append(end_pos)
                parcels.append(i)
                parcel.remove(i)
    return parcels, parcel


def drawParcel(parcels,surface):
    for parcel in parcels:
        point=cercle_circonscrit(parcel)
        if(point!=0):
            pygame.draw.circle(surface,(250,0,0),point,1.85)

def avg(array):
    point=[0,0]
    for i in array:
        point[0]=point[0]+i[0]
        point[1]=point[1]+i[1]
    point[0]=point[0]/len(array)
    point[1]=point[1]/len(array)
    x=random.randint(0,1)
    if(x==1):
        x=random.uniform(0.0,5.0)
        point[0]=point[0]+x
    else:
        x=random.uniform(0.0,5.0)
        point[0]=point[0]+x
    x=random.randint(0,2)    
    if(x==1):
        x=random.uniform(0.0,5.0)
        point[1]=point[1]-x
    else:
        x=random.uniform(0.0,5.0)
        point[1]=point[1]+x
    return point

def find(item,array):
    for x in array:
        if(item[0]==x[0]):
            if(item[1]==x[1]):
                return True
    return False


def cercle_circonscrit(T):
    (x1, y1), (x2, y2), (x3, y3) = T
    A = numpy.array([[x3-x1,y3-y1],[x3-x2,y3-y2]])
    Y = numpy.array([(x3**2 + y3**2 - x1**2 - y1**2),(x3**2+y3**2 - x2**2-y2**2)])
    if numpy.linalg.det(A) == 0:
        x1 = x1+0.1
        y1 = y1-0.1
        x2=x2+0.1
        y2=y2-0.1
        x3=x3-0.1
        y3=y3+0.1
        A = numpy.array([[x3-x1,y3-y1],[x3-x2,y3-y2]])
        Y = numpy.array([(x3**2 + y3**2 - x1**2 - y1**2),(x3**2+y3**2 - x2**2-y2**2)])
        if numpy.linalg.det(A) == 0:
            return 0
    Ainv = numpy.linalg.inv(A)
    X = 0.5*numpy.dot(Ainv,Y)
    x,y = X[0],X[1]
    r = sqrt((x-x1)**2+(y-y1)**2)
    return (x,y)

