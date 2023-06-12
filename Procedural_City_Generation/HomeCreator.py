import pygame
import random

def setBuildingOnPoint(point,surface):
    size=2.2
    shape=random.randint(0,2)
    R=random.randint(75,150)
    G=random.randint(75,150)
    B=random.randint(75,150)
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
            y=random.uniform(-3.0,3.0)
            newPoint[0]=newPoint[0]+x
            newPoint[1]=newPoint[1]+y
            points.append(newPoint)
        pygame.draw.polygon(surface,(R,G,B),points)