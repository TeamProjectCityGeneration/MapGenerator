import pygame
import math
import random
import numpy as np
import Voronoi as vn
import MapColourer as mc

surface = 0
heightmap = 0

def set_surface(surf):
    global surface
    surface = surf
    
def set_heightmap(height):
    global heightmap
    heightmap = height
    
def set_moisturemap(moisture):
    global moisturemap
    moisturemap = moisture

def DrawLine(surface, x_start, y_start, x_end, y_end):
    road_color = (0, 0, 0)        
    # Rysowanie linii
    pygame.draw.line(surface, road_color, (x_start, y_start), (x_end, y_end))
# funkcja do testowania 
def DrawNode(surface, x, y, i):
    if i == -1:
        node_color = (255, 0, 0)
    if i == 0:
        node_color = (0, 255, 0)
    if i == 1:
        node_color = (0, 0, 255)
    if i == 2:
        node_color = (255, 255, 0)
    if i == 3:
        node_color = (255, 0, 255)
    # Rysowanie nodeów (do testowania)
    pygame.draw.circle(surface, node_color, (x, y), 2)
        
def GenerateString(rules, sentence):
    newString = ''
    for char in sentence:
        map = char
        try:       
            map = rules[char]
        except:
            pass
        newString += map
    return newString

def LSystemCity(screen, height_map, moisture_map, base_size, current_size):
    set_heightmap(height_map)
    set_surface(screen)
    set_moisturemap(moisture_map)
    nodes_positions = []
    multiplier = current_size[0]/base_size[0]
    base_length = 40
    base_degree = 0
    while True:
        x_start = random.randint(base_size[0]/5, base_size[0]-base_size[0]/5)
        y_start = random.randint(base_size[1]/5, base_size[1]-base_size[1]/5)
        if height_map[x_start][y_start] > 0.35:
            x_start *= multiplier
            y_start *= multiplier
            break
    positions = []
    base_string = "F"
    rules = {"F" : "F[+F][-F]"}
    complexity_level = 3
    DrawNode(screen, x_start, y_start, -1)
    nodes_positions.append((x_start, y_start))
    for j in range (pow(complexity_level,2)):
        x_new, y_new = GenerateRandomNode(x_start, y_start, base_length)
        DrawNode(screen, x_new, y_new, -1)
        nodes_positions.append((x_start, y_start))
    for i in range (complexity_level):
        string = GenerateString(rules, base_string)
        base_string = string
        for char in base_string:
            checks = 0
            check = True
            if char == "F":
                # Specjalny przypadek (dzielenie przez 0)
                if (base_degree) % 180 == 0:
                    x_end = round(x_start + base_length)
                    y_end = round(y_start)
                    DrawNode(screen, x_end, y_end, i)
                    nodes_positions.append((x_start, y_start))
                    DrawLine(screen, x_start, y_start, x_end, y_end)
                    for j in range (complexity_level-3*i+3):
                        x_new, y_new = GenerateRandomNode(x_end, y_end, base_length*pow(2,i))
                        DrawNode(screen, x_new, y_new, i)
                        nodes_positions.append((x_start, y_start))
                    x_start = x_end
                    y_start = y_end
                # Wszystkie inne przypadki
                else:
                    #while check == True and checks < 30:         
                        radian = math.pi/(180/base_degree)
                        x_len = round(base_length*math.cos(radian))
                        y_len = round(base_length*math.sin(radian))
                        if x_end < base_size[0]*multiplier and y_end < base_size[1]*multiplier and x_end > 0 and y_end > 0 and height_map[math.floor(x_end/multiplier)][math.floor(y_end/multiplier)] > 0.35:
                            x_end = round(x_start + x_len)
                            y_end = round(y_start + y_len)
                            DrawLine(screen, x_start, y_start, x_end, y_end)
                            DrawNode(screen, x_end, y_end, i)
                            nodes_positions.append((x_start, y_start))
                            for j in range (complexity_level-3*i+3):
                                x_new, y_new = GenerateRandomNode(x_end, y_end, base_length*pow(2,i))
                                DrawNode(screen, x_new, y_new, i)
                                nodes_positions.append((x_start, y_start))
                            x_start = x_end
                            y_start = y_end
                            check = False
                        else:
                            base_degree += 35
                            checks += 1
            elif char == "+":
                base_degree += random.randint(20, 70)
            elif char == "-":
                base_degree -= random.randint(20, 70)
            elif char == "[":
                positions.append({"x": x_end, "y": y_end, "alpha": base_degree})
            elif char == "]":
                position = positions.pop()
                x_start = position["x"]
                y_start = position["y"]
                base_degree = position["alpha"]
            else:
                pass
    DrawPolygonAndCity(nodes_positions)
    #Polygonize(nodes_positions)
    
def DrawPolygonAndCity(nodes_positions):
    vn.draw_voronoi(surface, heightmap, nodes_positions)    
    mc.DrawTree(surface, heightmap, moisturemap, nodes_positions)
    
"""
def Polygonize(nodes_positions):
    left = len(nodes_positions)
    n_of_generations = nodes_positions[left-1]["generation"]
    breakpoints = []
    search = -1
    total = 0
    for i in range (n_of_generations+2):
        start = total
        while total < left and nodes_positions[total]["generation"] == search:
            total += 1
        search += 1
        breakpoints.append({"start": start, "end": total})
        
    group_id = 0
    while group_id < len(breakpoints):
        start = breakpoints[group_id]["start"]
        end = breakpoints[group_id]["end"]
        left = end-start
        while left > 0:
            polygon_vertex_number = random.randint(3,6)
            if polygon_vertex_number < left:
                if left-polygon_vertex_number < 3:
                    polygon_vertex_number = left-polygon_vertex_number
            else:
                polygon_vertex_number = left
            left = left - polygon_vertex_number
            i = 0
            while True:
                if nodes_positions[i]["taken"] == False:
                    init_point_id = i
                    nodes_positions[i]["taken"] = True
                    CountDistance(init_point_id, nodes_positions, start, end, polygon_vertex_number)
                    break
                else:
                    i += 1
                    continue
        group_id += 1
    
def CountDistance(init_point_id, nodes_positions, start, end, polygon_vertex_number):
    distance = []
    ids = []
    ids.append(init_point_id)
    for i in range(start, end):
        if i != init_point_id:
            dst = math.sqrt(pow(nodes_positions[init_point_id]["x"]-nodes_positions[i]["x"],2)+pow(nodes_positions[init_point_id]["y"]-nodes_positions[i]["y"],2))
            distance.append({"distance": dst, "id": i})
    distance = sorted(distance, key=lambda d: d['distance'])
    for i in range(polygon_vertex_number):  
        id = distance[i]["id"]
        nodes_positions[id]["taken"] = True
        ids.append(id)
    DrawPolygonAndCity(nodes_positions)
"""        
      
def GenerateRandomNode(x, y, radius):
    degree = 2 * math.pi * random.random()
    r = radius * math.sqrt(random.random())
    x_new = r * math.cos(degree) + x
    y_new = r * math.sin(degree) + y
    return x_new, y_new

def GenerateCity1(height_map, base_size):
    def DrawLineX(height_map, x, y):
        for line in range(1, 10, 1):
            if (x + line >= base_size[0]) or (x + line <= 0) or (height_map[x + line, y] < 0.33):
                continue
            height_map[x + line, y] = 1.02
        return height_map

    def DrawLineY(height_map, x, y):
        for line in range(1, 10, 1):
            if (y + line >= base_size[1]) or (y + line <= 0) or (height_map[x, y + line] < 0.33):
                continue
            height_map[x, y + line] = 1.02
        return height_map

    city_map = (base_size[0], base_size[1])
    city_map = np.zeros(city_map)
    startX = random.randint(0, base_size[0])
    startY = random.randint(0, base_size[1])
    iterationX, iterationY = 0, 0

    while height_map[startX, startY] < 0.33:
        startX = random.randint(0, base_size[0])
        startY = random.randint(0, base_size[1])

    for x in range(-50, 51, 10):
        for y in range(-50, 51, 10):
            if (startX + x <= 0) or (startX + x >= base_size[0]):
                continue
            if (startY + y <= 0) or (startY + y >= base_size[1]):
                continue
            if height_map[startX + x, startY + y] < 0.33:
                continue
            height_map[startX + x, startY + y] = 1.01

            if x != 50:
                if iterationX < 3:
                    DrawLineX(height_map, startX + x, startY + y)
                else:
                    iterationX = 0
            if y != 50:
                if iterationY < 4:
                    DrawLineY(height_map, startX + x, startY + y)
                else:
                    iterationY = 0

            iterationX = iterationX + 1
            iterationY = iterationY + 1

    return height_map
