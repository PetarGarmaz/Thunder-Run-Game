import pygame
import pygame_gui #pip install pygame_gui
from pygame.math import Vector2
import math
import random

from Player import PlayerProjectile120mm, PlayerProjectile30mm, Player, PlayerTurret, PlayerHealthSprite, PlayerReloadBar120mm, PlayerReloadBar30mm
from Enemy import EnemyProjectile, Enemy, EnemyTurret, EnemyHealthSprite
from Enviroment import EnviromentSprite, RepairCrate

class GameModel():
	def __init__(self):
		#All sprite groups
		self.allSprites = pygame.sprite.Group()
		self.enemies = pygame.sprite.Group()
		self.enemyTurrets = pygame.sprite.Group()
		self.players = pygame.sprite.Group()
		self.playerTurrets = pygame.sprite.Group()
		self.enemyProjectiles = pygame.sprite.Group()
		self.playerProjectiles = pygame.sprite.Group()
		self.crates = pygame.sprite.Group()
		self.enviroment = pygame.sprite.Group()
		self.bars = pygame.sprite.Group()

		#Defining a player
		self.player = Player((400, 300), self.allSprites, self.players)
		self.playerTurret = PlayerTurret(self.player, self.allSprites, self.playerTurrets, self.playerProjectiles)

		self.playerHealthBar = PlayerHealthSprite(self.player, self.bars)
		self.playerReloadBar = PlayerReloadBar120mm(self.player, self.playerTurret, self.bars)
		self.playerReloadBar2 = PlayerReloadBar30mm(self.player, self.playerTurret, self.bars)

		#Enemy/Round controllers
		self.roundStart = 0
		self.enemyNum = 1

		#Theme controllers: 0 = "Grass"; 1 = "Desert"; 2 = "Snow";
		self.spawnEnviroment = True
		self.theme = 0

		#Misc
		self.clock = pygame.time.Clock()
		self.deltaTime = 0

	def GameEnviroment(self):
		if self.spawnEnviroment == True:
			numOfDecor = 4
			currentObject = None
			distanceBetweenObjects = 0

			for i in range(numOfDecor - 1):
				spawnObject = False
				randomObject = random.randint(0,1)

				while spawnObject == False:
					x = random.randint(100, 700)
					y = random.randint(100, 500)

					randomRotation = random.choice([0, 90, 180, 270])

					if(currentObject == None):
						currentObject = (EnviromentSprite((x, y), self.theme, randomObject, randomRotation, self.allSprites, self.enviroment))
						spawnObject = True
					else:
						distanceBetweenObjects = math.hypot(x - currentObject.position.x, y - currentObject.position.y)
							
						if(distanceBetweenObjects > 200 and distanceBetweenObjects < 500):
							currentObject = (EnviromentSprite((x, y), self.theme, randomObject, randomRotation, self.allSprites, self.enviroment))
							spawnObject = True

					
			self.spawnEnviroment = False
				

	def GameEnemySpawner(self):
		repairCrateChance = random.randint(0, 1)

		if(len(self.enemies) <= 0):
			self.roundStart += 1/60
		else:
			self.roundStart = 0

		if(self.roundStart >= 5):
			if(repairCrateChance == 1):
				self.SpawnCrate()

			for i in range(self.enemyNum):
				x = random.choice([0, 800])
				y = random.choice([0, 600])

				newX = random.randint(0, 800)
				newY = random.randint(0, 600)

				fireTiming = random.randint(1, 6)

				#Generate enemies
				enemy = Enemy((x, y), (newX, newY), self.player, self.allSprites, self.enemies)
				enemyTurret = EnemyTurret(enemy, self.player, fireTiming, self.allSprites, self.enemyTurrets, self.enemyProjectiles)

				enemyHealthBar = EnemyHealthSprite(enemy, self.bars)

			self.enemyNum += 1

	def SpawnCrate(self):
		x = random.randint(100, 700)
		y = random.randint(100, 500)

		repairCrate = RepairCrate((x, y), self.allSprites, self.crates)

	def GameLogic(self):
		self.playerToEnemyHitList = pygame.sprite.groupcollide(self.enemies, self.playerProjectiles, False, True)
		self.enemyToPlayerHitList = pygame.sprite.groupcollide(self.players, self.enemyProjectiles, False, True)
		self.playerCratePickup = pygame.sprite.groupcollide(self.players, self.crates, False, True)

		self.playerWithEnviroment = pygame.sprite.groupcollide(self.enviroment, self.players, False, False)
		self.enemyWithEnviroment = pygame.sprite.groupcollide(self.enviroment, self.enemies, False, False)

		self.playerProjectileWithEnviroment = pygame.sprite.groupcollide(self.enviroment, self.playerProjectiles, False, False)
		self.enemyProjectileWithEnviroment = pygame.sprite.groupcollide(self.enviroment, self.enemyProjectiles, False, False)

		for enemy, projectileList in self.playerToEnemyHitList.items():
			for projectile in projectileList:
				enemy.health -= projectile.damage

		for player, projectileList in self.enemyToPlayerHitList.items():
			for projectile in projectileList:
				player.health -= projectile.damage
			
		for player, crateList in self.playerCratePickup.items():
			for crate in crateList:
				player.health = player.maxHealth

		for enviromentObject, playerList in self.playerWithEnviroment.items():
			for player in playerList:
				enviromentObject.isBroken = True

		for enviromentObject, enemyList in self.enemyWithEnviroment.items():
			for enemy in enemyList:
				enviromentObject.isBroken = True

		for enviroment, projectileList in self.playerProjectileWithEnviroment.items():
			for projectile in projectileList:
				if(enviroment.health > 0):
					projectile.kill()
					enviroment.health -= projectile.damage

		for enviroment, projectileList in self.enemyProjectileWithEnviroment.items():
			for projectile in projectileList:
				if(enviroment.health > 0):
					projectile.kill()
					enviroment.health -= projectile.damage
				
	def GameDraw(self, view):
		self.allSprites.update()
		self.bars.update()	
		view.screen.fill((255, 255, 255))
		view.screen.blit(view.background, (0, 0))

		#Layered drawing (top = first drawn; bottom = last drawn)
		self.enviroment.draw(view.screen)
		self.crates.draw(view.screen)		
		self.enemies.draw(view.screen)
		self.enemyTurrets.draw(view.screen)
		self.players.draw(view.screen)
		self.playerTurrets.draw(view.screen)
		self.enemyProjectiles.draw(view.screen)
		self.playerProjectiles.draw(view.screen)
		self.bars.draw(view.screen)

		pygame.display.flip()
		self.clock.tick(60)

class GameView():
	def __init__(self):
		self.model = GameModel()

		#Setting up game screen and UI managers
		self.screen = pygame.display.set_mode((800, 600))
		self.guiManager = pygame_gui.UIManager((800, 600))
		
		#Setting up backgrounds and icon
		self.background = None

		self.grassBG = pygame.image.load("Images/Grass/background.png")
		self.desertBG = pygame.image.load("Images/Desert/background.png")
		self.snowBG = pygame.image.load("Images/Snow/background.png")

		self.mainMenuBackground = pygame.image.load("Images/UI/mainMenuBG.png")
		self.optionsBackground = pygame.image.load("Images/UI/optionsBG.png")

		self.menuBackground = self.mainMenuBackground

		self.gameIcon = pygame.Surface((75,75))
		self.gameIcon.set_colorkey((0,0,0))
		self.gameIcon = pygame.image.load("Images/gameIcon.png")

		#Some window settings
		pygame.display.set_caption("Thunder Run")
		pygame.display.set_icon(self.gameIcon)

		#Buttons - Main Menu
		self.startButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((250, 150),(300, 75)), text="Start Game", manager=self.guiManager)
		self.optionsButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((250, 275),(300, 75)), text="Options", manager=self.guiManager)
		self.quitButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((250, 400),(300, 75)), text="Quit Game", manager=self.guiManager)

		#Buttons/Sliders - Options
		self.healthSlider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((125, 200), (250, 25)), start_value=100, value_range=[50, 200], manager=self.guiManager)
		self.movementSlider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((425, 200), (250, 25)), start_value=3, value_range=[1, 5], manager=self.guiManager)
		self.themeSlider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((275, 355), (250, 25)), start_value=0, value_range=[0, 2], manager=self.guiManager)

		self.healthSliderText = self.healthSlider.get_current_value()
		self.movementSliderText = self.movementSlider.get_current_value()
		self.themeSliderText = "Grass"

		self.healthSliderNumber = pygame_gui.elements.UITextBox(html_text="<font face=’Agency FB’>{}</font>".format(self.healthSliderText), relative_rect=pygame.Rect((210, 230), (80, 35)), manager=self.guiManager)
		self.movementSliderNumber = pygame_gui.elements.UITextBox(html_text="<font face=’Agency FB’>{}</font>".format(self.movementSliderText), relative_rect=pygame.Rect((510, 230), (80, 35)), manager=self.guiManager)
		self.themeSliderNumber = pygame_gui.elements.UITextBox(html_text="<font face=’Agency FB’>{}</font>".format(self.themeSliderText), relative_rect=pygame.Rect((350, 385), (100, 35)), manager=self.guiManager)

		self.backToMenuButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((275, 450),(250, 50)), text="Back", manager=self.guiManager)

		self.healthSliderNumber.hide()
		self.movementSliderNumber.hide()
		self.themeSliderNumber.hide()

		self.healthSlider.hide()
		self.movementSlider.hide()
		self.themeSlider.hide()

		self.backToMenuButton.hide()

	def MenuDraw(self):
		self.guiManager.update(self.model.deltaTime)
		self.screen.fill((255, 255, 255))
		self.screen.blit(self.menuBackground, (0,0))
		self.guiManager.draw_ui(self.screen)

		pygame.display.update()

class GameController():
	def __init__(self):
		#Initializing pygame and pygame sound settings
		pygame.init()
		pygame.mixer.init(frequency = 44100, size = -16, channels = 20, buffer = 2**12)

		self.model = GameModel()
		self.view = GameView()

		#Misc
		self.done = False
		self.menuDone = False
		self.paused = False

		#Start with main menu
		self.UpdateMainMenu()

	def MainMenuEventHandler(self):
		self.model.deltaTime = self.model.clock.tick(60)/1000

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.menuDone = True
				self.done = True

			if event.type == pygame.USEREVENT:
				if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
					if event.ui_element == self.view.startButton:
						self.model.theme = self.view.themeSlider.get_current_value()

						if(self.model.theme == 0):
							self.view.background = self.view.grassBG
						elif(self.model.theme == 1):
							self.view.background = self.view.desertBG
						elif(self.model.theme == 2):
							self.view.background = self.view.snowBG

						self.model.player.maxHealth = self.view.healthSlider.get_current_value()
						self.model.player.health = self.model.player.maxHealth

						self.menuDone = True
						self.UpdateGame()
	
					elif event.ui_element == self.view.optionsButton:
						self.view.menuBackground = self.view.optionsBackground
						self.view.startButton.hide()
						self.view.optionsButton.hide()
						self.view.quitButton.hide()

						self.view.healthSliderNumber.show()
						self.view.movementSliderNumber.show()
						self.view.themeSliderNumber.show()

						self.view.healthSlider.show()
						self.view.movementSlider.show()
						self.view.themeSlider.show()

						self.view.backToMenuButton.show()

					elif event.ui_element == self.view.quitButton:
						self.done = True

					if event.ui_element == self.view.backToMenuButton:
						self.view.menuBackground = self.view.mainMenuBackground

						self.view.startButton.show()
						self.view.optionsButton.show()
						self.view.quitButton.show()

						self.view.healthSliderNumber.hide()
						self.view.movementSliderNumber.hide()
						self.view.themeSliderNumber.hide()

						self.view.healthSlider.hide()
						self.view.movementSlider.hide()
						self.view.themeSlider.hide()

						self.view.backToMenuButton.hide()						
				
				if event.user_type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
					if event.ui_element == self.view.healthSlider:
						self.view.healthSliderText = self.view.healthSlider.get_current_value()
						self.view.healthSliderNumber.kill()
						self.view.healthSliderNumber = pygame_gui.elements.UITextBox(html_text="<font face=’Agency FB’>{}</font>".format(self.view.healthSliderText), relative_rect=pygame.Rect((210, 230), (80, 35)), manager=self.view.guiManager)
					elif event.ui_element == self.view.movementSlider:
						self.view.movementSliderText = self.view.movementSlider.get_current_value()
						self.view.movementSliderNumber.kill()
						self.view.movementSliderNumber = pygame_gui.elements.UITextBox(html_text="<font face=’Agency FB’>{}</font>".format(self.view.movementSliderText), relative_rect=pygame.Rect((510, 230), (80, 35)), manager=self.view.guiManager)
					elif event.ui_element == self.view.themeSlider:
						val = self.view.themeSlider.get_current_value()
						self.view.themeSliderText = self.NumToString(val)

						self.view.themeSliderNumber.kill()
						self.view.themeSliderNumber = pygame_gui.elements.UITextBox(html_text="<font face=’Agency FB’>{}</font>".format(self.view.themeSliderText), relative_rect=pygame.Rect((350, 385), (100, 35)), manager=self.view.guiManager)

			self.view.guiManager.process_events(event)

	def GameEventHandler(self):
		for event in pygame.event.get():
			key = pygame.key.get_pressed()

			if event.type == pygame.QUIT:
				self.menuDone = True
				self.done = True

			if key[pygame.K_w]:
				self.model.player.movementSpeed = -self.view.movementSlider.get_current_value()
			elif key[pygame.K_s]:
				self.model.player.movementSpeed = self.view.movementSlider.get_current_value()
			else:
				self.model.player.movementSpeed = 0

			if key[pygame.K_a]:
				self.model.player.rotationSpeed = -self.view.movementSlider.get_current_value()
			elif key[pygame.K_d]:
				self.model.player.rotationSpeed = self.view.movementSlider.get_current_value()
			else:
				self.model.player.rotationSpeed = 0

			if key[pygame.K_ESCAPE]:
				self.paused = not self.paused

	def UpdateMainMenu(self):
		while not self.done and not self.menuDone:
			self.MainMenuEventHandler()
			self.view.MenuDraw()

	def UpdateGame(self):
		while not self.done and self.menuDone:
			self.GameEventHandler()

			if(not self.paused):
				self.model.GameEnviroment()
				self.model.GameEnemySpawner()
				self.model.GameLogic()
				self.model.GameDraw(self.view)


	def NumToString(self, num):
		strng = ""

		if num == 0:
			strng = "Grass"
		elif num == 1:
			strng = "Desert"
		elif num == 2:
			strng = "Snow"
		
		return strng

if __name__ == "__main__":
	GameController()
	pygame.quit()
