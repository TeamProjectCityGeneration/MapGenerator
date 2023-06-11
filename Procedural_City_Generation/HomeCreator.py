import pygame
import random

def setBuildingOnPoint(point,surface):
    shape=random.randint(0,2)
    R=random.randint(75,150)
    G=random.randint(75,150)
    B=random.randint(75,150)
    if(shape==0):
        pygame.draw.circle(surface,(R,G,B),point,3)
    elif(shape==1):
        rect=pygame.Rect(point[0],point[1]+4,4,4)
        pygame.draw.rect(surface,(R,G,B),rect)
    else:
        points=[]
        shape=random.randint(3,8)
        for i in range(shape):
            newPoint=[point[0],point[1]]
            x=random.uniform(-3.0,3.0)
            y=random.uniform(-3.0,3.0)
            newPoint[0]=newPoint[0]+x
            newPoint[1]=newPoint[1]+y
            points.append(newPoint)
        pygame.draw.polygon(surface,(R,G,B),points)