import pygame
from pygame.math import Vector2

class RepairCrate(pygame.sprite.Sprite):
	def __init__(self, pos, allSprites, crateSprite):
		super().__init__()
		
		self.position = pos

		self.image = pygame.Surface((40,40), pygame.SRCALPHA)
		self.image = pygame.image.load("Images/repairCrate.png")

		self.original_image = self.image
		self.rect = self.image.get_rect(center=self.position)

		self.allSprites = allSprites
		self.add(self.allSprites)

		self.crateSprite = crateSprite
		self.add(self.crateSprite)
	
	def update(self):
		self.rect.center = self.position

class EnviromentSprite(pygame.sprite.Sprite):
	def __init__(self, pos, theme, spriteObject, rotation, allSprites, enviroment):
		super().__init__()
		
		self.position = Vector2(pos)
		self.theme = theme
		self.spriteObject = spriteObject
		self.rotation = rotation

		if(self.theme == 0):
			if(self.spriteObject == 0):
				self.spriteImage = "Images/Grass/rock.png"
			else:
				self.spriteImage = "Images/Grass/house.png"
		elif(self.theme == 1):
			if(self.spriteObject == 0):
				self.spriteImage = "Images/Desert/rock.png"
			else:
				self.spriteImage = "Images/Desert/house.png"
		elif(self.theme == 2):
			if(self.spriteObject == 0):
				self.spriteImage = "Images/Snow/rock.png"
			else:
				self.spriteImage = "Images/Snow/house.png"

		self.image = pygame.Surface((50,50), pygame.SRCALPHA)
		self.image = pygame.image.load(self.spriteImage)

		self.original_image = self.image
		self.rect = self.image.get_rect(center=self.position)

		self.image = pygame.transform.rotate(self.original_image, rotation)

		self.allSprites = allSprites
		self.add(self.allSprites)

		self.enviroment = enviroment
		self.add(self.enviroment)

		self.health = 100
	
	def update(self):
		self.rect.center = self.position

		if(self.health <= 0):
			self.kill()
		
			NewEnviromentSprite(self.position, self.theme, self.spriteObject, self.rotation, self.allSprites, self.enviroment, self.health)

class NewEnviromentSprite(pygame.sprite.Sprite):
	def __init__(self, pos, theme, spriteObject, rotation, allSprites, enviroment, health):
		super().__init__()
		
		self.position = Vector2(pos)
		self.theme = theme
		self.spriteObject = spriteObject
		self.rotation = rotation

		if(self.theme == 0):
			if(self.spriteObject == 0):
				self.spriteImage = "Images/Grass/rockBroken.png"
			else:
				self.spriteImage = "Images/Grass/houseBroken.png"
		elif(self.theme == 1):
			if(self.spriteObject == 0):
				self.spriteImage = "Images/Desert/rockBroken.png"
			else:
				self.spriteImage = "Images/Desert/houseBroken.png"
		elif(self.theme == 2):
			if(self.spriteObject == 0):
				self.spriteImage = "Images/Snow/rockBroken.png"
			else:
				self.spriteImage = "Images/Snow/houseBroken.png"

		self.image = pygame.Surface((50,50), pygame.SRCALPHA)
		self.image = pygame.image.load(self.spriteImage)

		self.original_image = self.image
		self.rect = self.image.get_rect(center=self.position)

		self.image = pygame.transform.rotate(self.original_image, rotation)

		self.allSprites = allSprites
		self.add(self.allSprites)

		self.enviroment = enviroment
		self.add(self.enviroment)

		self.health = health
	
	def update(self):
		self.rect.center = self.position

			