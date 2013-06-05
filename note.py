import pygame


class Note(object):
	"""Parent class for notes
	-----------------------------
	"""
	def __init__(self, type, note_speed):
		self.speed = note_speed
		self.surf = pygame.image.load("Data/Images/Notes/" + type + 'note.png')
		self.ghost_surf = pygame.image.load("Data/Images/Notes/" + type + 'ghostnote.png')
		self.rect = self.surf.get_rect()
		self.rect.topleft = 287, 800
		self.passed = False
		self.scored = False

	def step(self):
		self.rect = self.rect.move(0, -self.speed)
		if self.scored:
			new_dim = (self.ghost_surf.get_width() + 1, self.ghost_surf.get_height() + 1)
			self.ghost_surf = pygame.transform.scale(self.ghost_surf, (new_dim))
			self.ghost_rect = self.ghost_surf.get_rect()
			self.ghost_rect.x = self.rect.x
			self.ghost_rect.y = 27
		if not self.passed:
			if self.rect.y < 15:
				self.passed = True
				return True

	def score(self, key, scoring_presses):
		if self.rect.y >= 15 and self.rect.y <= 85:
			if self.type == 'fire':
				if key == 0 and scoring_presses[key]:
					self.scored = True
					return True
			if self.type == 'metal':
				if key == 1 and scoring_presses[key]:
					self.scored = True
					return True
			if self.type == 'earth':
				if key == 2 and scoring_presses[key]:
					self.scored = True
					return True
			if self.type == 'water':
				if key == 3 and scoring_presses[key]:
					self.scored = True
					return True
			if self.type == 'air':
				if key == 4 and scoring_presses[key]:
					self.scored = True
					return True


class FireNote(Note):
	def __init__(self, note_speed):
		self.type = 'fire'
		super(FireNote, self).__init__(self.type, note_speed)


class MetalNote(Note):
	def __init__(self, note_speed):
		self.type = 'metal'
		super(MetalNote, self).__init__(self.type, note_speed)
		self.rect = self.rect.move(45, 0)


class EarthNote(Note):
	def __init__(self, note_speed):
		self.type = 'earth'
		super(EarthNote, self).__init__(self.type, note_speed)
		self.rect = self.rect.move(90, 0)


class WaterNote(Note):
	def __init__(self, note_speed):
		self.type = 'water'
		super(WaterNote, self).__init__(self.type, note_speed)
		self.rect = self.rect.move(135, 0)


class AirNote(Note):
	def __init__(self, note_speed):
		self.type = 'air'
		super(AirNote, self).__init__(self.type, note_speed)
		self.rect = self.rect.move(180, 0)
