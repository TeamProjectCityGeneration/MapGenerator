import pygame

def Save(filename):
	surface=pygame.display.get_surface()
	pygame.image.save(surface,filename)
