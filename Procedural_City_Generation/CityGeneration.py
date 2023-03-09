import pygame
import math
import random

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
    base_length = 7
    base_degree = 0
    while True:
        x_start = random.randrange(base_size[0]-1)
        y_start = random.randrange(base_size[1]-1)
        if height_map[x_start][y_start] > 0.35:
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
            if base_degree == 0:
                x_end = x_start * multiplier + base_length
                y_end = y_start * multiplier
                DrawLine(screen, x_start, y_start, x_end, y_end)
                x_start = x_end
            # Wszystkie inne przypadki
            else:
                while check == True:
                    radian = math.pi/(180/base_degree+degree_offset)
                    x_len = round(base_length*math.cos(radian))
                    y_len = round(base_length*math.sin(radian))
                    x_end = x_start + x_len
                    y_end = y_start + y_len
                    
                    if height_map[x_end][y_end] > 0.35 and x_end < base_size[0] and y_end < base_size[1] and x_end > 0 and y_end > 0:
                        print(x_end, y_end)
                        x_start *= multiplier
                        y_start *= multiplier
                        x_end = x_start + x_len
                        y_end = y_start + y_len
                        DrawLine(screen, x_start, y_start, x_end, y_end)
                        x_start = x_end
                        y_start = y_end
                        check = False
                    else:
                        degree_offset += 10
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

