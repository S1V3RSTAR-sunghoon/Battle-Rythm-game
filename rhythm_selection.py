import pygame
import sys
import inits
import rhythm
import menu
import glob


def main(screen):
	#initilisation phase
	pygame.init()

	fps_clock = pygame.time.Clock()

	start_img = pygame.image.load("Data/Images/Buttons/startbutton.png")
	back_img = pygame.image.load("Data/Images/Buttons/backbutton.png")
	select_img = pygame.image.load("Data/Images/selectionarrow.png")

	start_rect = start_img.get_rect()
	back_rect = back_img.get_rect()
	select_rect = select_img.get_rect()

	start_rect.topleft = (500, 550)
	back_rect.topleft = (500, 655)
	select_rect.midleft = (300, 410)

	tracks = glob.glob("Data/Tracks/*.txt")
	new_tracks = []
	for track in tracks:
		track = track[12:-4]
		new_tracks.append(track)
	tracks = new_tracks

	font = pygame.font.SysFont("Bookman", 23)
	track_labels = []
	for track in tracks:
		track_label = font.render(track, 1, (255, 255, 255))
		track_labels.append(track_label)
	selected_track = 0
	first_label_pos = 400
	list_animated = False

	end = False

	while 1:
		#event phase
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			elif event.type == pygame.MOUSEBUTTONDOWN:
				if start_rect.collidepoint(event.pos):
					end = 'rhythm'
				elif back_rect.collidepoint(event.pos):
					end = 'menu'
				elif not list_animated and event.pos[0] < 400:
					if event.pos[1] < 400 and selected_track != 0:
						list_animated = "Up"
						selected_track -= 1
						track_animate_i = 0
					elif event.pos[1] > 400 and selected_track != len(tracks) - 1:
						list_animated = "Down"
						selected_track += 1
						track_animate_i = 0

		keys = pygame.key.get_pressed()
		if not list_animated:
			if keys[pygame.constants.K_UP] and selected_track != 0:
				list_animated = "Up"
				selected_track -= 1
				track_animate_i = 0
			elif keys[pygame.constants.K_DOWN] and selected_track != len(tracks) - 1:
				list_animated = "Down"
				selected_track += 1
				track_animate_i = 0
		if keys[pygame.constants.K_RETURN]:
			end = 'rhythm'

		#logic phase
		if list_animated == "Up":
			first_label_pos += 5
			track_animate_i += 1
			if track_animate_i == 16:
				list_animated = False
		elif list_animated == "Down":
			first_label_pos -= 5
			track_animate_i += 1
			if track_animate_i == 16:
				list_animated = False

		#render phase

		screen.fill((0, 0, 0))  # background goes here later

		label_i = 0
		for track_label in track_labels:
			screen.blit(track_label, (50, (first_label_pos + 80 * label_i)))
			label_i += 1

		screen.blit(start_img, start_rect)
		screen.blit(back_img, back_rect)
		screen.blit(select_img, select_rect)

		pygame.display.flip()

		fps_clock.tick(60)

		if end:
			break

	if end == 'rhythm':
		rhythm.main(screen, tracks[selected_track])
	elif end == 'menu':
		menu.main(screen)

if __name__ == "__main__":
	screen = inits.screen()
	main(screen)
