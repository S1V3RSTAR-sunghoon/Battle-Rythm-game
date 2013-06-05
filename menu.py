import pygame
import inits
import sys
import settings
import battle
import story
import rhythm_selection


def main(screen):
	#initilisation phase
	fps_clock = pygame.time.Clock()

	end = False

	story_img = pygame.image.load("Data/Images/Buttons/storybutton.png")
	rhythm_img = pygame.image.load("Data/Images/Buttons/rhythmbutton.png")
	battle_img = pygame.image.load("Data/Images/Buttons/battlebutton.png")
	settings_img = pygame.image.load("Data/Images/Buttons/settingsbutton.png")
	quit_img = pygame.image.load("Data/Images/Buttons/quitbutton.png")

	story_rect = story_img.get_rect()
	rhythm_rect = rhythm_img.get_rect()
	battle_rect = battle_img.get_rect()
	settings_rect = settings_img.get_rect()
	quit_rect = quit_img.get_rect()

	story_rect.topleft = (80, 270)
	rhythm_rect.topleft = (80, 375)
	battle_rect.topleft = (80, 475)
	settings_rect.topleft = (80, 575)
	quit_rect.topleft = (80, 675)

	while 1:
		#event phase
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			elif event.type == pygame.MOUSEBUTTONDOWN:
				if story_rect.collidepoint(event.pos):
					end = 'story'
				elif rhythm_rect.collidepoint(event.pos):
					end = 'rhythm'
				elif battle_rect.collidepoint(event.pos):
					end = 'battle'
				elif settings_rect.collidepoint(event.pos):
					end = 'settings'
				elif quit_rect.collidepoint(event.pos):
					sys.exit()

		#logic phase

		#render phase

		screen.fill((0, 0, 0))  # background goes here later

		screen.blit(story_img, story_rect)
		screen.blit(rhythm_img, rhythm_rect)
		screen.blit(battle_img, battle_rect)
		screen.blit(settings_img, settings_rect)
		screen.blit(quit_img, quit_rect)

		pygame.display.flip()

		fps_clock.tick(60)

		if end:
			break
	if end == 'story':
		story.main(screen)
	elif end == 'rhythm':
		rhythm_selection.main(screen)
	elif end == 'battle':
		battle.main(screen)
	elif end == 'settings':
		settings.main(screen)


if __name__ == "__main__":
	screen = inits.screen()
	main(screen)
