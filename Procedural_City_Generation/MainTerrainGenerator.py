import pygame
import pygame_menu
from pygame_menu import themes
import Terrains as terrains
import MapColourer as MC
import os
from win32api import GetSystemMetrics
import numpy as np
import RiversGenerator as rg
import NoiseGenerator as ng
import CityGeneration as cg
import random


# gdzie pokazywać na ekranie będą się okna
Width = GetSystemMetrics(0)
os.environ['SDL_VIDEO_WINDOW_POS'] = '%d,%d' % (Width/2-300, 100)


def GenerateColdMap(height_map, cold, cold_str):
    cold_map = (XPIX, YPIX)
    cold_map = np.zeros(cold_map)
    if cold_str == 'weak':
        cold_const = 0.8
    if cold_str == 'medium':
        cold_const = 1
    if cold_str == 'strong':
        cold_const = 1.2
    if cold == 'none':
        return cold_map
    if cold == 'north_pole':
        cold_map = terrains.NormalizeData(height_map, 0, 0.4)
        for i in range(XPIX):
            for j in range(YPIX):
                cold_map[i][j] = cold_map[i][j] + cold_const-(j/XPIX)*(cold_const*0.8)
    if cold == 'south_pole':
        cold_map = terrains.NormalizeData(height_map, 0, 0.4)
        for i in range(XPIX):
            for j in range(YPIX):        
                cold_map[i][j] = cold_map[i][j] + cold_const-(j/XPIX)*(cold_const*0.8)
            cold_map[i][:] = cold_map[i][:][::-1]
        
    return cold_map


def GenerateCity1(height_map):
    def DrawLineX(height_map, x, y):
        for line in range(1, 10, 1):
            if (x + line >= XPIX) or (x + line <= 0) or (height_map[x + line, y] < 0.33):
                continue
            height_map[x + line, y] = 1.02
        return height_map

    def DrawLineY(height_map, x, y):
        for line in range(1, 10, 1):
            if (y + line >= YPIX) or (y + line <= 0) or (height_map[x, y + line] < 0.33):
                continue
            height_map[x, y + line] = 1.02
        return height_map

    city_map = (XPIX, YPIX)
    city_map = np.zeros(city_map)
    startX = random.randint(0, XPIX)
    startY = random.randint(0, YPIX)
    iterationX, iterationY = 0, 0

    while height_map[startX, startY] < 0.33:
        startX = random.randint(0, XPIX)
        startY = random.randint(0, YPIX)

    for x in range(-50, 51, 10):
        for y in range(-50, 51, 10):
            if (startX + x <= 0) or (startX + x >= XPIX):
                continue
            if (startY + y <= 0) or (startY + y >= YPIX):
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


def GenerateMap(height_map, moisture_map, cold_map):
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(MUSIC)
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play(-1)
    base_size = (XPIX, YPIX)
    current_size = (XPIX*9, YPIX*9)
    screen = pygame.display.set_mode(current_size)
    pygame.display.set_caption('Proceduralnie wygenerowane miasto')
    icon = pygame.image.load('Procedural_City_Generation/Ikona.png')
    pygame.display.set_icon(icon)
    MC.colorize(height_map, moisture_map, cold_map, screen)
    if CITY_TYPE == 'lsystem':
        cg.LSystemCity(screen, height_map, base_size, current_size)
    pygame.image.save(screen,'Procedural_City_Generation/Map.bmp')
    screen = pygame.display.set_mode((450,450))
    img = pygame.image.load('Procedural_City_Generation/Map.bmp')
    screen.blit(img, (0, 0), (0, 0, 450, 450))
    pygame.display.update()
    running = True
    x_offset = 0
    y_offset = 0
    
    while running:
        event = pygame.event.poll()
        pressed = pygame.key.get_pressed()
        
        if event.type == pygame.QUIT:
            pygame.mixer.music.fadeout(300)
            running = False
            DisplayGUI()
        if pressed[pygame.K_UP]:
            if (y_offset < 0):
                y_offset += 1
                scrollY(screen, img, x_offset, y_offset)
        elif pressed[pygame.K_DOWN]:
            if (y_offset > -current_size[1]+450):
                y_offset -= 1
                scrollY(screen, img, x_offset, y_offset)
        elif pressed[pygame.K_LEFT]:
            if (x_offset < 0):
                x_offset += 1
                scrollX(screen, img, x_offset, y_offset)
        elif pressed[pygame.K_RIGHT]:
            if (x_offset > -current_size[0]+450):
                x_offset -= 1
                scrollX(screen, img, x_offset, y_offset)
        pygame.display.update()
        
def scrollX(screenSurf, image, offsetX, offsetY):
    width, height = image.get_size()
    screenSurf.blit(image, (offsetX, offsetY))
    if offsetX < 0:
        screenSurf.blit(image, (width + offsetX, 0), (0, 0, -offsetX, height))
        
def scrollY(screenSurf, image, offsetX, offsetY):
    width, height = image.get_size()
    screenSurf.blit(image, (offsetX, offsetY))
    if offsetY < 0:
        screenSurf.blit(image, (0, height + offsetY), (0, 0, width, -offsetY))


def DisplayGUI():

    # Ustwienia domyślne
    global TERRAIN, RIVER, COLD, COLD_STR, XPIX, YPIX, FILENAME, MUSIC, CITY_TYPE
    TERRAIN = 'mountains'
    RIVER = 'none'
    COLD = 'none'
    MUSIC = ''
    COLD_STR = 'weak'
    FILENAME = 'Map.bmp'
    XPIX, YPIX = 50, 50
    CITY_TYPE = 'none'
    
    def set_file_name(filename):
        global FILENAME
        FILENAME = filename

    def start_generating():
        mainmenu._open(loading)
        pygame.time.set_timer(update_loading, 20)

    def set_terrain(l, value):
        global TERRAIN
        TERRAIN = value

    def set_river_type(l, value):
        global RIVER
        RIVER = value

    def set_cold_spread_type(l, value):
        global COLD
        COLD = value

    def set_cold_strenght(l, value):
        global COLD_STR
        COLD_STR = value
        
    def set_city_type(l, value):
        global CITY_TYPE
        CITY_TYPE = value

    def set_map_size(value):
        global XPIX, YPIX
        if 'x' in value:
            X, Y = value.split('x')
        else:
            XPIX = 50
            YPIX = 50
            return XPIX, YPIX

        if X == '' or Y == '':
            XPIX = 50
            YPIX = 50
            return XPIX, YPIX
        
        elif int(X) < 50:
            XPIX = 50
        elif int(Y) < 50:
            YPIX = 50
        else:
            XPIX = int(X)
            YPIX = int(Y)

    def setting_menu_options():
        mainmenu._open(setting_values)

    pygame.init()
    pygame.display.set_caption("Proceduralna generacja miasta v0.0.3")
    icon = pygame.image.load('Procedural_City_Generation/Ikona.png')
    pygame.display.set_icon(icon)
    surface = pygame.display.set_mode((800, 500))
    mainmenu = pygame_menu.Menu('Main menu', 800, 500, theme=themes.THEME_SOLARIZED)
    mainmenu.add.button('Start generation', start_generating)
    mainmenu.add.button('Change settings', setting_menu_options)
    mainmenu.add.text_input('Save file as: ', default="Map.bmp", maxchar=20, onchange=set_file_name)
    mainmenu.add.button('Quit', pygame_menu.events.EXIT)

    setting_values = pygame_menu.Menu(
        'Select your desired settings', 800, 500, theme=themes.THEME_BLUE)
    setting_values.add.selector('Terrain :',
                                [('Switzerland', 'mountains'), ('Great Plains', 'plains'),
                                 ('Lone Island', 'island'), ("Pirate's heaven",'many_islands'),
                                 ('Amazon Forest', 'big_forest'), ('Sahara', 'desert'),
                                 ('Louisiana', 'swamp')], onchange=set_terrain)
    setting_values.add.text_input(
        'Map size X/Y (max 600x400): ', default='50x50', maxchar=7, onchange=set_map_size)

    setting_values.add.selector('River type :',
                                [('None', 'none'), ('Perlin Worms', 'perlin'), ('Gradient Descent', 'grad_desc')], onchange=set_river_type)

    setting_values.add.selector('Cold spread :',
                                [('None', 'none'), ('North Pole', 'north_pole'), ('South Pole', 'south_pole')], onchange=set_cold_spread_type)

    setting_values.add.selector('Cold power :',
                                [('Weak', 'weak'), ('Medium', 'medium'), ('Strong', 'strong')], onchange=set_cold_strenght)
    setting_values.add.selector('City Type :',
                                [('None', 'none'), ('L-systems', 'lsystem'), ('Grid', 'grid'), ('Voronoi', 'voronoi')], onchange=set_city_type)


    loading = pygame_menu.Menu(
        'Generating...', 800, 500, theme=themes.THEME_DARK)
    loading.add.progress_bar(
        "Progress", progressbar_id="1", default=0, width=200)
    
    arrow = pygame_menu.widgets.LeftArrowSelection(arrow_size=(10, 15))

    update_loading = pygame.USEREVENT + 0

    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == update_loading:
                progress = loading.get_widget("1")
                progress.set_value(progress.get_value() + 1)
                if progress.get_value() == 100:
                    pygame.time.set_timer(update_loading, 0)
                    progress.set_value(0)

                    # Wczytywanie i generowanie danych
                    height_map = ng.GenerateData(2, 1, 1.5, XPIX, YPIX)
                    moisture_map = ng.GenerateData(2, 0.5, 1, XPIX, YPIX)
                    cold_map = GenerateColdMap(height_map, COLD, COLD_STR)

                    # Generuję mapę wysokości, maskę wilgotności i zimna
                    if TERRAIN == 'mountains':
                        height_map = terrains.MakeMountains(height_map)
                        MUSIC = "Procedural_City_Generation/Music/mountains.mp3"
                    if TERRAIN == 'plains':
                        height_map = terrains.MakeLowlands(height_map)
                        MUSIC = 'Procedural_City_Generation/Music/plains.mp3'
                    if TERRAIN == 'island':
                        height_map = terrains.MakeIsland(height_map, XPIX, YPIX)
                        MUSIC = 'Procedural_City_Generation/Music/island.mp3'
                    if TERRAIN == 'many_islands':
                        height_map = terrains.MakeIslands(height_map)
                        MUSIC = "Procedural_City_Generation/Music/many_islands.mp3"
                    if TERRAIN == 'big_forest':
                        height_map, moisture_map = terrains.MakeBigForest(height_map, moisture_map)
                        MUSIC = "Procedural_City_Generation/Music/big_forest.mp3"
                    if TERRAIN == 'desert':
                        height_map, moisture_map = terrains.MakeDesert(height_map, moisture_map)
                        MUSIC = "Procedural_City_Generation/Music/desert.mp3"
                    if TERRAIN == 'swamp':
                        height_map, moisture_map = terrains.MakeSwamp(height_map, moisture_map)
                        MUSIC = "Procedural_City_Generation/Music/swamp.mp3"
                    if RIVER == 'perlin':
                        height_map = rg.PerlinRiver(height_map, XPIX, YPIX)
                    if RIVER == 'grad_desc':
                        moisture_map, height_map=rg.makeRiver(moisture_map,height_map)
                    # Generowanie mapy na podstawie tych danych
                    GenerateMap(height_map, moisture_map, cold_map)

            if event.type == pygame.QUIT:
                exit()

        if mainmenu.is_enabled():
            mainmenu.update(events)
            mainmenu.draw(surface)
            if (mainmenu.get_current().get_selected_widget()):
                arrow.draw(surface, mainmenu.get_current().get_selected_widget())

        pygame.display.update()


# Wywołanie funkcji głównej.
DisplayGUI()
