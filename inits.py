import pygame


def screen():
	width = 800
	height = 800
	screenSize = width, height
	screen = pygame.display.set_mode(screenSize)
	#call get_size() on screen to recover sizes
	return screen
