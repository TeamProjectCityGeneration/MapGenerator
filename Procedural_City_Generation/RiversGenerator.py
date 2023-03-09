import random
from re import I
import numpy as np
import NoiseGenerator as ng

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
    number=random.randint(int(len(moisture)/4),int(len(moisture)/2))
    for x in range (number):
        i=random.randint(1,len(moisture)-25)
        j=random.randint(1,len(moisture)-25)
        moisture[i][j]=0.9
        makeLine(0,i,j,len(moisture)-1,moisture,height)
    #for x in range(100):
    #    print(moisture[x])
    return   moisture, height

def stop(x, i , j, max):
    if(i>=max or j>= max or i<=0 or j<=0):
        return True
    return False
def direction(i,j,height,VI,VJ):
    ai=[]
    aj=[]
    bi=[]
    bj=[]
    x=height[i][j]
    if(VI!=2):
        if(height[i+VI][j+VJ]<=x):
            coin=random.randint(0,10)
            if(coin!=0):
                return i+VI,j+VJ
    if(height[i+1][j]<=x and VI != 1 and VJ != 0 and height[i+1][j]!=0.1):
        ai.append(i+1)
        aj.append(j)
    else:
        bi.append(i+1)
        bj.append(j)
    if(height[i+1][j+1]<=x and VI != 1 and VJ != 0 and height[i+1][j+1]!=0.1):
        ai.append(i+1)
        aj.append(j+1)
    else:
        bi.append(i+1)
        bj.append(j+1) 
    if(height[i+1][j-1]<=x and VI != 1 and VJ != 1 and height[i+1][j-1]!=0.1):
        ai.append(i+1)
        aj.append(j-1)
    else:
        bi.append(i+1)
        bj.append(j-1) 
    if(height[i][j+1]<=x and VI != 1 and VJ != -1 and height[i][j+1]!=0.1):
        ai.append(i)
        aj.append(j+1)
    else:
        bi.append(i)
        bj.append(j+1) 
    if(height[i][j-1]<=x and VI != 0 and VJ != 1 and height[i][j-1]!=0.1):
        ai.append(i)
        aj.append(j-1)
    else:
        bi.append(i)
        bj.append(j-1)
    if(height[i-1][j]<=x and VI != 0 and VJ != -1 and height[i-1][j]!=0.1):
        ai.append(i-1)
        aj.append(j)
    else:
        bi.append(i-1)
        bj.append(j) 
    if(height[i-1][j+1]<=x and VI != -1 and VJ != 0 and height[i-1][j+1]!=0.1):
        ai.append(i-1)
        aj.append(j+1)
    else:
        bi.append(i-1)
        bj.append(j+1)
    if(height[i-1][j-1]<=x and VI != -1 and VJ != 1 and height[i-1][j-1]!=0.1):
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

def makeLine(x,i,j,max,moisture,height):
    number=random.randint(len(moisture),len(moisture)*5)
    prevI, prevJ = i, j
    i,j=direction(i, j, height,2,2) 
    for k in range(number):
        height[i][j]=0.1
        moisture[i][j]=0.9
        VI, VJ = i-prevI,j-prevJ
        prevI, prevJ = i, j
        i, j=direction(i, j, height,VI,VJ)
        prevI, prevJ = i, j
        #makeLine(x,newI,newJ,max,moisture,height,newI-i,newJ-j)
        if(stop(x,i,j,max)==True):
            break