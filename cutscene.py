import pygame


def white_fader_out(screen, fps_clock):
	fade_img = pygame.image.load("Data/Images/fader.png")
	fade_rect = fade_img.get_rect()
	for i in range(1, 20):
		screen.blit(fade_img, fade_rect)
		pygame.display.flip()
		fps_clock.tick(50)


def white_fader_in():
	pass
