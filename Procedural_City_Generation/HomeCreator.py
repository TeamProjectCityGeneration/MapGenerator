import pygame
import random

def setBuildingOnPoint(point,surface):
    shape=random.randint(0,1)
    R=random.randint(50,200)
    G=random.randint(50,200)
    B=random.randint(50,200)
    if(shape==0):
        pygame.draw.circle(surface,(R,G,B),point,1.85)
    else:
        points=[]
        shape=random.randint(3,8)
        for i in range(shape):
            newPoint=[point[0],point[1]]
            x=random.uniform(-2.0,2.0)
            y=random.uniform(-2.0,2.0)
            newPoint[0]=newPoint[0]+x
            newPoint[1]=newPoint[1]+y
            points.append(newPoint)
        pygame.draw.polygon(surface,(R,G,B),points)