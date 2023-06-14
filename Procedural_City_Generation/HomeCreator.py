import pygame
import random

def setBuildingOnPoint(point,surface):
    baseSize=2.5
    changeSize=random.uniform(-1.0,1.0)
    size=baseSize+changeSize
    shape=random.randint(0,2)
    R=random.randint(75,150)
    G=random.randint(75,150)
    B=random.randint(75,150)
    if(checkPoint(point,surface)==False):
        return
    if(shape==0):
        pygame.draw.circle(surface,(R,G,B),point,1.5*size)
    elif(shape==1):
        rect=pygame.Rect(point[0],point[1]+2*size,2*size,2*size)
        pygame.draw.rect(surface,(R,G,B),rect)
    else:
        points=[]
        shape=random.randint(3,8)
        for i in range(shape):
            newPoint=[point[0],point[1]]
            x=random.uniform(-1.5*size,1.5*size)
            y=random.uniform(-1.5*size,1.5*size)
            newPoint[0]=newPoint[0]+x
            newPoint[1]=newPoint[1]+y
            if(checkPoint(newPoint,surface)==False):
               return
            points.append(newPoint)
        pygame.draw.polygon(surface,(R,G,B),points)


def checkPoint(point,surface):
    try:
        coordinates = [int(point[0]),int(point[1])]
        color=surface.get_at(coordinates)
        if(color==(0,0,0,255)):
            randomX=random.randint(-1,1)
            randomY=random.randint(-1,1)
            return False
            color2=surface.get_at((int(point[0])+randomX,int(point[1])+randomY))
            if(color2==(0,0,0,255)):
                return point
            else:
                return ((int(point[0])+randomX,int(point[1])+randomY))
        return True
    except:
        return True
    
#def addictionalBuilding():
