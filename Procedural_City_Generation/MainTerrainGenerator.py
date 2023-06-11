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
import Voronoi as voi

# gdzie pokazywać na ekranie będą się okna
Width = GetSystemMetrics(0)
os.environ['SDL_VIDEO_WINDOW_POS'] = '%d,%d' % (Width/2-300, 100)

def GenerateColdMap(height_map, cold_type, cold_str):
    cold_map = (XPIX, YPIX)
    cold_map = np.zeros(cold_map)
    if cold_str == 'none':
        cold_const = 0
    if cold_str == 'weak':
        cold_const = 0.65
    if cold_str == 'medium':
        cold_const = 0.8
    if cold_str == 'strong':
        cold_const = 1.1
    if cold_type == 'none':
        return cold_map
    if cold_type == 'north_pole':
        cold_map = terrains.NormalizeData(height_map, 0, 0.4)
        for i in range(XPIX):
            for j in range(YPIX):
                cold_map[i][j] = cold_map[i][j] + cold_const-(j/YPIX)*(cold_const*0.8)
    if cold_type == 'south_pole':
        cold_map = terrains.NormalizeData(height_map, 0, 0.4)
        for i in range(XPIX):
            for j in range(YPIX):
                cold_map[i][j] = cold_map[i][j] + cold_const-((YPIX-j)/YPIX)*(cold_const*0.8)  
    if cold_type == 'bipolar':
        cold_map = terrains.NormalizeData(height_map, 0, 0.4)
        for i in range(XPIX):
            for j in range(YPIX):
                if j <= YPIX/2:     
                    cold_map[i][j] = cold_map[i][j] + cold_const-(j/XPIX)*(cold_const*0.8)
                else:
                    cold_map[i][j] = cold_map[i][j] + cold_const-((YPIX-j)/YPIX)*(cold_const*0.8)         
    return cold_map


def GenerateMap(height_map, moisture_map, cold_map):
    pygame.init()
    base_size = (XPIX, YPIX)
    current_size = (18*XPIX, 18*YPIX)
    screen = pygame.Surface(current_size)
    #screen = pygame.display.set_mode(current_size)
    pygame.display.set_caption('Proceduralnie wygenerowane miasto')
    icon = pygame.image.load('Ikona.png')
    pygame.display.set_icon(icon)
    if CITY_TYPE == 'grid':
        height_map = cg.GenerateCity1(height_map, base_size)
    MC.set_multiplier(18)
    MC.colorize(height_map, moisture_map, cold_map, screen)
    if CITY_TYPE == 'voronoi':
        area = voi.getRandomArea(current_size)
        #surface=pygame.display.get_surface()
        voi.draw_voronoi(screen,height_map,area)
    if CITY_TYPE == 'fixed':
        cg.LSystemCity(screen, height_map, moisture_map, base_size, current_size)
    pygame.image.save(screen,'Map.bmp')
    screen = pygame.display.set_mode((900,900))
    img = pygame.image.load('Map.bmp')
    screen.blit(img, (0, 0), (0, 0, 900, 900))
    pygame.display.update()
    running = True
    x_offset = 0
    y_offset = 0
    
    while running:
        event = pygame.event.poll()
        pressed = pygame.key.get_pressed()
        
        if event.type == pygame.QUIT:
            running = False
            DisplayGUI()
        if pressed[pygame.K_UP]:
            if (y_offset < 0):
                y_offset += 3
                scrollY(screen, img, x_offset, y_offset)
        elif pressed[pygame.K_DOWN]:
            if (y_offset > -current_size[1]+900):
                y_offset -= 3
                scrollY(screen, img, x_offset, y_offset)
        elif pressed[pygame.K_LEFT]:
            if (x_offset < 0):
                x_offset += 3
                scrollX(screen, img, x_offset, y_offset)
        elif pressed[pygame.K_RIGHT]:
            if (x_offset > -current_size[0]+900):
                x_offset -= 3
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
    COLD_STR = 'none'
    FILENAME = 'Map.bmp'
    XPIX, YPIX = 150, 150
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
            XPIX = 150
            YPIX = 150
            return XPIX, YPIX

        if X == '' or Y == '':
            XPIX = 150
            YPIX = 150
            return XPIX, YPIX
        
        elif int(X) < 150:
            XPIX = 150
        elif int(Y) < 150:
            YPIX = 150
        else:
            XPIX = int(X)
            YPIX = int(Y)

    def setting_menu_options():
        mainmenu._open(setting_values)
        
    # Okienko menu
    pygame.init()
    pygame.display.set_caption("Proceduralna generacja miasta")
    icon = pygame.image.load('Ikona.png')
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
        'Map size (Input X/Y): ', default='150x150', maxchar=7, onchange=set_map_size)

    setting_values.add.selector('River type: ',
                                [('None', 'none'), ('Perlin Worms', 'perlin'), ('Gradient Descent', 'grad_desc')], onchange=set_river_type)

    setting_values.add.selector('Cold spread: ',
                                [('None', 'none'), ('North Pole', 'north_pole'), ('South Pole', 'south_pole'), ('Bipolar', 'bipolar'), ('Central', 'central')], onchange=set_cold_spread_type)

    setting_values.add.selector('Cold power: ',
                                [('None', 'none'), ('Weak', 'weak'), ('Medium', 'medium'), ('Strong', 'strong')], onchange=set_cold_strenght)
    setting_values.add.selector('City Type: ',
                                [('None', 'none'), ('Fixed', 'fixed'), ('Grid', 'grid'), ('Voronoi', 'voronoi')], onchange=set_city_type)


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
                    helper_height_map = terrains.MakeMountains(height_map)
                    moisture_map = ng.GenerateData(2, 0.5, 1, XPIX, YPIX)
                    cold_map = GenerateColdMap(helper_height_map, COLD, COLD_STR)
                    # Generuję mapę wysokości, maskę wilgotności i zimna
                    if TERRAIN == 'mountains':
                        height_map = terrains.MakeMountains(height_map)
                    if TERRAIN == 'plains':
                        height_map = terrains.MakeLowlands(height_map)
                    if TERRAIN == 'island':
                        height_map = terrains.MakeIsland(height_map, XPIX, YPIX)
                    if TERRAIN == 'many_islands':
                        height_map = terrains.MakeIslands(height_map)
                    if TERRAIN == 'big_forest':
                        height_map, moisture_map = terrains.MakeBigForest(height_map, moisture_map)
                    if TERRAIN == 'desert':
                        height_map, moisture_map = terrains.MakeDesert(height_map, moisture_map)
                    if TERRAIN == 'swamp':
                        height_map, moisture_map = terrains.MakeSwamp(height_map, moisture_map)
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