import pygame
import sys
import inits
import note


def main(screen, track):
	# initilisation phase
	pygame.init()

	pygame.mixer.music.load("Data/Audio/" + track + ".ogg")
	pygame.mixer.music.set_volume(1.0)

	fps_clock = pygame.time.Clock()

	end = False

	note_track_img = pygame.image.load("Data/Images/notetrack.png")
	note_track_rect = note_track_img.get_rect()
	note_track_rect = note_track_rect.move(277, 0)

	q_tile_img = pygame.image.load("Data/Images/ControlTiles/QTile.png")
	w_tile_img = pygame.image.load("Data/Images/ControlTiles/WTile.png")
	o_tile_img = pygame.image.load("Data/Images/ControlTiles/OTile.png")
	p_tile_img = pygame.image.load("Data/Images/ControlTiles/PTile.png")
	q_tile_rect = q_tile_img.get_rect()
	w_tile_rect = w_tile_img.get_rect()
	o_tile_rect = o_tile_img.get_rect()
	p_tile_rect = p_tile_img.get_rect()
	q_tile_rect = q_tile_rect.move(297, 30)
	w_tile_rect = w_tile_rect.move(357, 30)
	o_tile_rect = o_tile_rect.move(420, 30)
	p_tile_rect = p_tile_rect.move(480, 30)

	fader_img = pygame.image.load("Data/Images/fader.png")
	fader_rect = fader_img.get_rect()
	fader_img = fader_img.convert()

	score_font = pygame.font.SysFont("Bookman", 23)
	title_font = pygame.font.SysFont("Bookman", 60)
	title_label = title_font.render(track, 1, (255, 255, 255))

	file = open('Data/Tracks/' + track + '.txt')
	bpm = int(file.readline())  # max milliseconds per note

	mspb = pow(bpm, -1) * 60000
	note_speed = int(mspb / 120)

	notes = []
	mspb_time = 0
	game_ticks = 0
	mspb_start = False
	music_start_ticks = int((780 / note_speed)) + 261

	notes_scored = 0
	total_notes = 0
	bad_notes = 0

	tapped = [False, False, False, False]  # true if the key has not be released

	# true if a note will be scored from presses q,w,e,r,t
	scoring_presses = [False, False, False, False]

	while 1:
		# event phase
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()

		# scoring keys are checked. Also make sure they are not held.
		keys = pygame.key.get_pressed()
		if keys[pygame.constants.K_q]:
			if not tapped[0]:
				tapped[0] = True
				scoring_presses[0] = True
		else:
			tapped[0] = False
		if keys[pygame.constants.K_w]:
			if not tapped[1]:
				tapped[1] = True
				scoring_presses[1] = True
		else:
			tapped[1] = False
		if keys[pygame.constants.K_o]:
			if not tapped[2]:
				tapped[2] = True
				scoring_presses[2] = True
		else:
			tapped[2] = False
		if keys[pygame.constants.K_p]:
			if not tapped[3]:
				tapped[3] = True
				scoring_presses[3] = True
		else:
			tapped[3] = False

		# logic phase

		# making new notes
		if mspb_time >= mspb:
			mspb_time = mspb_time - mspb
			line = file.readline()
			if line != '':
				new_notes = eval(line)
				if new_notes[0]:
					notes.append(note.FireNote(note_speed))
				if new_notes[1]:
					notes.append(note.EarthNote(note_speed))
				if new_notes[2]:
					notes.append(note.WaterNote(note_speed))
				if new_notes[3]:
					notes.append(note.AirNote(note_speed))

		# fade in and countdown
		if not mspb_start:
			if fader_img.get_alpha() > 0:
				fader_img.set_alpha(fader_img.get_alpha() - 3)
			elif game_ticks > 260:
				mspb_start = True
			elif game_ticks > 220:
				title_label = title_font.render("Battle!", 1, (255, 255, 255))
			elif game_ticks > 180:
				title_label = title_font.render("1", 1, (255, 255, 255))
			elif game_ticks > 140:
				title_label = title_font.render("2", 1, (255, 255, 255))
			elif game_ticks > 100:
				title_label = title_font.render("3", 1, (255, 255, 255))

		# music begins as first note reaches scoring zone
		if game_ticks == music_start_ticks:
			pygame.mixer.music.play()

		# scores a note if it is
		for n in notes:
			for key in range(0, 4):
				if n.score(key, scoring_presses):
					notes_scored = notes_scored + 1
					scoring_presses[key] = False

		# moves notes along. Removes them from array if past window. Adds to total notes if past scoring zone.
		new_notes = []
		for n in notes:
			if n.rect.midbottom[1] > 0:
				if n.step():
					total_notes = total_notes + 1
				new_notes.append(n)
		notes = new_notes

		# adds a bad note if a key was pressed with no note.
		for i in scoring_presses:
			if i:
				bad_notes = bad_notes + 1
				notes_scored = notes_scored - 1

		scoring_presses = [False, False, False, False]  # reset score presses

		# render phase

		screen.fill((200, 200, 200))  # background goes here later

		screen.blit(note_track_img, note_track_rect)
		screen.blit(q_tile_img, q_tile_rect)
		screen.blit(w_tile_img, w_tile_rect)
		screen.blit(o_tile_img, o_tile_rect)
		screen.blit(p_tile_img, p_tile_rect)

		for n in notes:
			screen.blit(n.surf, n.rect)
			if n.scored:
				screen.blit(n.ghost_surf, n.ghost_rect)

		try:
			percent_score =  int(notes_scored / total_notes * 100)
			if percent_score > 100:
				percent_score = 100
			if percent_score < 0:
				percent_score = 0
		except ZeroDivisionError:
			percent_score = 100
		score_string = 'Score: ' + str(percent_score) + '%'
		score_label = score_font.render(score_string, 1, (255, 255, 255))
		screen.blit(score_label, (650, 10))
		bad_notes_label = score_font.render("Bad Notes: " + str(bad_notes), 1, (255, 255, 255))
		screen.blit(bad_notes_label, (650, 25))
		if not mspb_start:
			screen.blit(title_label, (400, 400))

		screen.blit(fader_img, fader_rect)

		pygame.display.flip()

		fps_clock.tick_busy_loop(50)
		if mspb_start:
			mspb_time += 20
		game_ticks += 1

		if end:
			break

if __name__ == "__main__":
	track = 'Test'
	screen = inits.screen()
	main(screen, track)
