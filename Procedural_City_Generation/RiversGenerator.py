import random
from re import I
import numpy as np
import NoiseGenerator as ng
import math

def gradientDescent():
    return(0)


def PerlinRiver(height_map, xpix, ypix):
    rivers_map = (xpix, ypix)
    rivers_map = np.zeros(rivers_map)
    rivers_map = ng.GenerateData(2, 1, 2, xpix, ypix)
    for i in range(xpix):
        for j in range(ypix):
            if rivers_map[i][j] >= 0.45 and rivers_map[i][j] <= 0.55 and height_map[i][j] >= 0.33:
                height_map[i][j] = 0.2
    return height_map

def makeRiver(moisture,height):
    number=random.randint(int(math.sqrt(len(moisture)*len(moisture[0]))/5),int(math.sqrt(len(moisture)*len(moisture[0]))/4))
    for x in range (number):
        i=random.randint(1,len(moisture)-1)
        j=random.randint(1,len(moisture[0])-1)
        moisture[i][j]=0.9
        makeLine(0,i,j,len(moisture)-1,len(moisture[0]),moisture,height)
    return  moisture, height

def stop(i , j, maxX,maxY):
    if(i>=maxX or j>= maxY or i<=0 or j<=0):
        return True
    return False
def direction(i,j,height,VI,VJ,maxX,maxY):
    ai=[]
    aj=[]
    bi=[]
    bj=[]
    x=height[i][j]
    if(VI!=2):
        if(checkDirection(x,i+VI,j+VJ,maxX,maxY,height)):
            coin=random.randint(0,10)
            if(coin!=0):
                return i+VI,j+VJ
    if(checkDirection(x,i+1,j,maxX,maxY,height) and VI != 1 and VJ != 0):
        ai.append(i+1)
        aj.append(j)
    else:
        bi.append(i+1)
        bj.append(j)
    if(checkDirection(x,i+1,j+1,maxX,maxY,height) and VI != 1 and VJ != 0):
        ai.append(i+1)
        aj.append(j+1)
    else:
        bi.append(i+1)
        bj.append(j+1) 
    if(checkDirection(x,i+1,j-1,maxX,maxY,height) and VI != 1 and VJ != 1):
        ai.append(i+1)
        aj.append(j-1)
    else:
        bi.append(i+1)
        bj.append(j-1) 
    if(checkDirection(x,i,j+1,maxX,maxY,height) and VI != 1 and VJ != -1):
        ai.append(i)
        aj.append(j+1)
    else:
        bi.append(i)
        bj.append(j+1) 
    if(checkDirection(x,i,j-1,maxX,maxY,height) and VJ != 1):
        ai.append(i)
        aj.append(j-1)
    else:
        bi.append(i)
        bj.append(j-1)
    if(checkDirection(x,i-1,j,maxX,maxY,height) and VI != 0 and VJ != -1):
        ai.append(i-1)
        aj.append(j)
    else:
        bi.append(i-1)
        bj.append(j) 
    if(checkDirection(x,i-1,j+1,maxX,maxY,height) and VI != -1 and VJ != 0):
        ai.append(i-1)
        aj.append(j+1)
    else:
        bi.append(i-1)
        bj.append(j+1)
    if(checkDirection(x,i-1,j-1,maxX,maxY,height) and VI != -1 and VJ != 1):
        ai.append(i-1)
        aj.append(j-1)
    else:
        bi.append(i-1)
        bj.append(j-1)
    if(len(ai)>0):
        index=random.randint(0,len(ai)-1)
        return ai[index], aj[index]
    else:
        index=random.randint(0,7)
        return bi[index],bj[index]

def makeLine(x,i,j,maxX,maxY,moisture,height):
    number=random.randint(int((maxX+maxY)/3),int((maxX+maxY)/2))
    prevI, prevJ = i, j
    i,j=direction(i, j, height,2,2,maxX,maxY) 
    for k in range(number):
        try:
            height[i][j]=0.1
            moisture[i][j]=0.9
            VI, VJ = i-prevI,j-prevJ
            prevI, prevJ = i, j
            i, j=direction(i, j, height,VI,VJ,maxX,maxY)
            prevI, prevJ = i, j
            if(stop(i,j,maxX,maxY)==True):
                break
        except:
            break

def checkDirection(x,i, j,maxX,maxY,height):
    if(i>=maxX or j>= maxY or i<=0 or j<=0):
        return False
    if(height[i][j]<=x and height[i][j]!=0.1):
        return True