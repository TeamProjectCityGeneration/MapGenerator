from time import sleep
from perlin_noise import PerlinNoise
import pygame
import pygame_menu
from pygame_menu import themes
import Terrains as terrains
import MapColourer as MC
import os
from win32api import GetSystemMetrics
import SaveMap as sm
import numpy as np
import RiversGenerator as rg
import voronoi as voi

# gdzie pokazywać na ekranie będą się okna
Width = GetSystemMetrics(0)
os.environ['SDL_VIDEO_WINDOW_POS'] = '%d,%d' % (Width/2-300, 100)


def GenerateData(base_octave, base_frequency, depth):
    octaves_tab = []
    for i in range(3):
        octaves_tab.append(PerlinNoise(octaves=base_octave*(pow(4, i))))

    pic = []
    for i in range(XPIX):
        row = []
        for j in range(YPIX):
            noise_val = 0
            for k in range(len(octaves_tab)):
                noise_val += octaves_tab[k]([base_frequency *
                                            i/XPIX, base_frequency*j/YPIX])
            row.append(noise_val)
        pic.append(row)
    pic = pow(terrains.NormalizeData(pic, 0, 1), depth)
    return pic


def GenerateRiver(river_type, height_map, moisture_map):
    rivers_map = (XPIX, YPIX)
    rivers_map = np.zeros(rivers_map)
    if river_type == "none":
        return height_map
    if river_type == "perlin":
        rivers_map = GenerateData(2, 1, 2)
        for i in range(XPIX):
            for j in range(YPIX):
                if rivers_map[i][j] >= 0.45 and rivers_map[i][j] <= 0.55 and height_map[i][j] >= 0.33:
                    height_map[i][j] = 0.2
    if river_type == "grad_desc":
        height_map=rg.makeRiver(moisture_map,height_map)
    return height_map


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
                cold_map[i][j] = cold_map[i][j] + \
                    cold_const-(j/XPIX)*(cold_const*0.8)
    if cold == 'south_pole':
        cold_map = terrains.NormalizeData(height_map, 0, 0.4)
        for i in range(XPIX):
            for j in range(YPIX):
                cold_map[i][j] = cold_map[i][j] + \
                    cold_const-(j/XPIX)*(cold_const*0.8)
            cold_map[i][:] = cold_map[i][:][::-1]
            print(cold_map)

    return cold_map


def GenerateMap(height_map, moisture_map, cold_map):
    pygame.init()
    pygame.mixer.init()
    #pygame.mixer.music.load(MUSIC)
    #pygame.mixer.music.set_volume(0)
    #pygame.mixer.music.play(-1)
    screen = pygame.display.set_mode((XPIX*3, YPIX*3))
    
    pygame.display.set_caption("Proceduralnie wygenerowane miasto")
    icon = pygame.image.load('Ikona.png')
    pygame.display.set_icon(icon)
    MC.colorize(TERRAIN, height_map, moisture_map, cold_map, screen)
    surface=pygame.display.get_surface()
    voi.draw_voronoi(surface,height_map)
    pygame.display.update()
    sm.Save("Map.bmp")
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.fadeout(300)
                running = False
                DisplayGUI()


def DisplayGUI():

    # Ustwienia domyślne
    global TERRAIN, RIVER, COLD, COLD_STR, XPIX, YPIX, FILENAME, MUSIC
    TERRAIN = 'mountains'
    RIVER = 'none'
    COLD = 'none'
    MUSIC = ''
    COLD_STR = 'weak'
    FILENAME = 'Map.bmp'
    XPIX, YPIX = 50, 50

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
        else:
            XPIX = int(X)
            YPIX = int(Y)

    def setting_menu_options():
        mainmenu._open(setting_values)

    pygame.init()
    pygame.display.set_caption("Proceduralna generacja miasta v0.0.3")
    icon = pygame.image.load('Ikona.png')
    pygame.display.set_icon(icon)

    surface = pygame.display.set_mode((600, 400))
    mainmenu = pygame_menu.Menu(
        'Main menu', 600, 400, theme=themes.THEME_SOLARIZED)
    mainmenu.add.button('Start generation', start_generating)
    mainmenu.add.button('Change settings', setting_menu_options)
    mainmenu.add.text_input(
        'Save file as: ', default="Map.bmp", maxchar=20, onchange=set_file_name)
    mainmenu.add.button('Quit', pygame_menu.events.EXIT)

    setting_values = pygame_menu.Menu(
        'Select your desired settings', 600, 400, theme=themes.THEME_BLUE)
    setting_values.add.selector('Terrain :',
                                [('Switzerland', 'mountains'), ('Great Plains', 'plains'),
                                 ('Lone Island', 'island'), ("Pirate's heaven",
                                                             'many_islands'),
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

    # Na przyszłość, do zaznaczania co chcemy/niechcemy
    setting_options = pygame_menu.Menu(
        'Select your desired settings', 600, 400, theme=themes.THEME_BLUE)

    loading = pygame_menu.Menu(
        'Generating...', 600, 400, theme=themes.THEME_DARK)
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

                    # Generuję mapę wysokości, maskę wilgotności i zimna
                    height_map = GenerateData(2, 1, 1.5)
                    moisture_map = GenerateData(2, 0.5, 1)
                    cold_map = GenerateColdMap(height_map, COLD, COLD_STR)
                    if TERRAIN == 'mountains':
                        height_map = terrains.MakeMountains(height_map)
                        MUSIC = "Music/mountains.mp3"
                    if TERRAIN == 'plains':
                        height_map = terrains.MakeLowlands(height_map)
                        MUSIC = 'Music/plains.mp3'
                    if TERRAIN == 'island':
                        height_map = terrains.MakeIsland(
                            height_map, XPIX, YPIX)
                        MUSIC = 'Music/island.mp3'
                    if TERRAIN == 'many_islands':
                        height_map = terrains.MakeIslands(height_map)
                        MUSIC = "Music/many_islands.mp3"
                    if TERRAIN == 'big_forest':
                        height_map, moisture_map = terrains.MakeBigForest(
                            height_map, moisture_map)
                        MUSIC = "Music/big_forest.mp3"
                    if TERRAIN == 'desert':
                        height_map, moisture_map = terrains.MakeDesert(
                            height_map, moisture_map)
                        MUSIC = "Music/desert.mp3"
                    if TERRAIN == 'swamp':
                        height_map, moisture_map = terrains.MakeSwamp(
                            height_map, moisture_map)
                        MUSIC = "Music/swamp.mp3"
                    height_map = GenerateRiver(RIVER, height_map, moisture_map)
                    screen = pygame.display.set_mode((3*XPIX, 3*YPIX))
                    MC.colorize(TERRAIN, height_map,
                                moisture_map, cold_map, screen)
                    sm.Save("Map.bmp")

                    # Generowanie mapy na podstawie tych danych
                    GenerateMap(height_map, moisture_map, cold_map)

            if event.type == pygame.QUIT:
                exit()

        if mainmenu.is_enabled():
            mainmenu.update(events)
            mainmenu.draw(surface)
            if (mainmenu.get_current().get_selected_widget()):
                arrow.draw(
                    surface, mainmenu.get_current().get_selected_widget())

        pygame.display.update()


# Wywołanie funkcji głównej.
DisplayGUI()
