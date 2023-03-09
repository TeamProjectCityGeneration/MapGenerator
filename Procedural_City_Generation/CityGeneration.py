import pygame
import math
import random
import numpy as np

def DrawLine(surface, x_start, y_start, x_end, y_end):
    road_color = (0, 0, 0)        
    # Rysowanie linii
    pygame.draw.line(surface, road_color, (x_start, y_start), (x_end, y_end))
        
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

def LSystemCity(screen, height_map, base_size, current_size):
    multiplier = current_size[0]/base_size[0]
    base_length = 6
    base_degree = 0
    while True:
        x_start = random.randint(0, base_size[0]-6)
        y_start = random.randint(0, base_size[1])
        if height_map[x_start][y_start] > 0.35:
            x_start *= multiplier
            y_start *= multiplier
            break
    positions = []
    base_string = "F"
    rules = {"F" : "F+F+F-[F-FF+F]-F-F-F+[F-FF+F]"}
    complexity_level = 3
    for i in range (complexity_level):
        string = GenerateString(rules, base_string)
        base_string = string
    for char in base_string:
        degree_offset = 0
        check = True
        if char == "F":
            # Specjalny przypadek (dzielenie przez 0)
            if (base_degree+degree_offset) % 180 == 0:
                x_end = round(x_start + base_length)
                y_end = round(y_start)
                DrawLine(screen, x_start, y_start, x_end, y_end)
                x_start = x_end
                y_start = y_end
            # Wszystkie inne przypadki
            else:
                while check == True:         
                    radian = math.pi/(180/base_degree+degree_offset)
                    x_len = round(base_length*math.cos(radian))
                    y_len = round(base_length*math.sin(radian))
                    print(math.ceil(x_end/multiplier),math.ceil(y_end/multiplier))
                    if x_end < base_size[0]*multiplier and y_end < base_size[1]*multiplier and x_end > 0 and y_end > 0 and height_map[math.ceil(x_end/multiplier)][math.ceil(y_end/multiplier)] > 0.35:
                        x_end = round(x_start + x_len)
                        y_end = round(y_start + y_len)
                        DrawLine(screen, x_start, y_start, x_end, y_end)
                        x_start = x_end
                        y_start = y_end
                        check = False
                    else:
                        base_degree += 45
        elif char == "+":
            base_degree += 20
        elif char == "-":
            base_degree -= 20
        elif char == "[":
            positions.append({"x": x_end, "y": y_end})
        elif char == "]":
            position = positions.pop()
            x_start = position["x"]
            y_start = position["y"]
        else:
            pass

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
