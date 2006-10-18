import pygame, math, time, soundmanager
from pygame.locals import *
from utilities.common import Describer
from os.path import join
from sys import exit
from random import randrange,randint


RGB_BLACK 	= 0,0,0
RGB_WHITE 	= 255,255,255
RGB_RED		= 255,0,0

GB_WIDTH	= 280
GB_HEIGHT	= 380

PADDLE_START_TOP = GB_HEIGHT - 30
PADDLE_START_LEFT = GB_WIDTH / 2

STARTSPEED = 5

class Ball(Describer):
	"Ball class, represents the ball object for the PyBreakout game"
	
	def __init__(self, imageFilename):
		"Ball __init__ method creates a ball in its default position with its default states"
		self.image = pygame.image.load(imageFilename)
		self.rect = self.image.get_rect()
		
		#the ball has an angle from 0 to 359 degrees
		self.angle = 135
		self.speed = 1
		self.x_dir = 1
		self.y_dir = -1
		self.stuck = True
		self.resetState()
	
	def resetState(self):
		"Ball is reset to sit motionless on top of paddle, launch with Spacebar"
		self.rect = self.rect.move(PADDLE_START_LEFT+30, PADDLE_START_TOP-self.rect.height)
						
	def moveDown(self, pixelsDown):
		"Move the ball image down pixelsDown worth"
		self.rect = self.rect.move(0,pixelsDown)
		
	def moveUp(self, pixelsUp):
		"Move the ball image up pixelsUp worth"
		self.rect = self.rect.move(0,-pixelsUp)
		
	def moveLeft(self, pixelsLeft):
		"Move the ball image left pixelsLeft worth"
		self.rect = self.rect.move(-pixelsLeft, 0)
		
	def moveRight(self, pixelsRight):
		"Move the ball image right pixelsRight worth"
		self.rect = self.rect.move(pixelsRight, 0)
		
	def autoMove(self):
		hitWall = False
		if self.stuck:
			return hitWall
		else:
			x_part = math.cos(math.radians(self.angle))/self.speed
			y_part = math.sin(math.radians(self.angle))/self.speed
			#print "x_part = %s , y_part = %s"%(x_part,y_part)
			
			if self.rect.left == 0:
				self.x_dir = 1
				hitWall = True
			if self.rect.right == GB_WIDTH:
				self.x_dir = -1
				hitWall = True
			if self.rect.top == 0:
				self.y_dir = 1
				hitWall = True
			
			#print "x_dir = %s, y_dir = %s, x = %s, y = %s"%(self.x_dir,self.y_dir,self.rect.x,self.rect.y)
			self.rect = self.rect.move(self.x_dir, self.y_dir)
			return hitWall

class Paddle(Describer):
	"A Paddle object"
	
	def __init__(self, imageFilename, ball):
		self.image = pygame.image.load(imageFilename)
		self.rect = self.image.get_rect()
		self.ball = ball
		self.resetState()
		
	def resetState(self):
		"Paddle object is reset to the bottom center of the screen"
		self.rect = self.rect.move(PADDLE_START_LEFT,PADDLE_START_TOP)
		
	def moveLeft(self, pixelsLeft):
		self.rect = self.rect.move(-pixelsLeft, 0)
		if self.ball.stuck:
			self.ball.rect = self.ball.rect.move(-pixelsLeft,0)
		
	def moveRight(self, pixelsRight):
		self.rect = self.rect.move(pixelsRight, 0)
		if self.ball.stuck:
			self.ball.rect = self.ball.rect.move(pixelsRight,0)

class Brick(Describer):
	"""every brick has the following
	an image: filename
	point value: int
	isDestructible: True/False
	isDestroyed: True/False
	a rectangular position: (x,y)"""
	
	def __init__(self, imageFilename, position, value=10, destructible=True, destroyed=False):
		self.image = pygame.image.load(imageFilename)
		self.rect = self.image.get_rect()
		self.position = position
		self.rect.move_ip(position)
		self.pointValue = value
		self.isDestructible = destructible
		self.isDestroyed = destroyed

class PyBreakout(Describer):
	"This is the main game class for PyBreakout"
	
	def __init__(self):
		self.running = False		
		
		self.size = GB_WIDTH, GB_HEIGHT
		self.height = self.size[1]
		self.width = self.size[0]
		
		self.soundManager = soundmanager.SoundManager()
		
		self.startGame()
		self.initializeScreen()
		
	def initializeScreen(self):
		#Create Gameboard with RGB_BLACK background
		self.screen = pygame.display.set_mode(self.size)
		self.updateScreen()
		
	def loadBricks(self):
		allBricks = []
		levelFile = open(join('resources','levels','level'+str(self.level)+".dat"))
		levelData = levelFile.readlines()
		self.drawLocation = [0,120]
		for levelLine in levelData:
			lineBricks = levelLine.strip().split(',')
			for brickChar in lineBricks:
				allBricks.append(self.createBrick(brickChar))
			self.drawLocation = 0,self.drawLocation[1]+10
		return allBricks
		
	def drawBricks(self):
		'''given all the Brick objects:
			1) Check to see if they are Destroyed
			2) if not Destroyed, draw currentBrick.image at currentBrick.position'''
		for currentBrick in self.bricks:
			if not currentBrick.isDestroyed:
				self.screen.blit(currentBrick.image, currentBrick.position)
			
	def createBrick(self, brickChar):
		"Given a brickChar, create the appropriate instance object of the Brick class and return it"
		
		newBrick = 0
		if brickChar == 'R':
			newBrick = Brick(join("resources","images","brick-red.png"), self.drawLocation)
		elif brickChar == 'P':
			newBrick = Brick(join("resources","images","brick-purple.png"), self.drawLocation)
		elif brickChar == 'G':
			newBrick = Brick(join("resources","images","brick-green.png"), self.drawLocation)
		elif brickChar == 'O':
			newBrick = Brick(join("resources","images","brick-orange.png"), self.drawLocation)
		elif brickChar == 'B':
			newBrick = Brick(join("resources","images","brick-blue.png"), self.drawLocation)
		elif brickChar == 'Q':
			newBrick = Brick(join("resources","images","brick-grey.png"), self.drawLocation, 0, False)
		elif brickChar == '.':
			newBrick = Brick(join("resources","images","brick-grey.png"), self.drawLocation, 0, True, True)
		if newBrick.isDestructible and not(newBrick.isDestroyed):
			self.numDestructibleBricks +=1
		self.drawLocation = self.drawLocation[0]+40,self.drawLocation[1]
		return newBrick
		
	def updateScreen(self):
		"Draw everything on the screen"
		
		self.screen.fill(RGB_BLACK)
		
		#Draw Paddle and Ball
		self.screen.blit(self.paddle.image, self.paddle.rect)
		self.screen.blit(self.ball.image, self.ball.rect)

		#Draw Points Label and Points String
		self.screen.blit(self.pointsLabel, (10,10))
		self.screen.blit(self.pointsString, (80,10))
		
		#Draw Level Label and Level String
		self.screen.blit(self.levelLabel, (200, 10))
		self.screen.blit(self.levelString, (250, 10))
		
		#Draw non-destroyed Bricks for current level
		self.drawBricks()
		
		#Draw Mini-paddles signifying lifes left
		self.drawMiniPaddles()
		
		pygame.display.flip()
	
	def drawMiniPaddles(self):
		if(self.numLives == 0):
			return
		drawPos = 0
		miniPaddleImage = pygame.image.load(join("resources","images","paddle-mini.png"))
		miniPaddleRect = miniPaddleImage.get_rect()
		for numLife in range(self.numLives):
			self.screen.blit(miniPaddleImage,(0+drawPos,GB_HEIGHT-miniPaddleRect.height))
			drawPos = drawPos + 22
		
	def reset(self):
		"Reset Ball, Paddle, and Speed to default positions and states. Called after a ball falls into the abyss."
		
		self.ball = Ball(join("resources","images","ball-mini.png"))
		self.paddle = Paddle(join("resources","images","paddle.png"),self.ball)
		
		self.pointsColor = RGB_WHITE
		self.running = True
		self.speed = 0
		
	def startGame(self):
		"Start a new game, reset everything to default positions and states"
		
		self.reset()
		self.points = 0
		self.level = 0
		#self.level = "TEST0"
		self.numDestructibleBricks = 0
		
		#Load bricks
		self.bricks = self.loadBricks()
		
		self.numLives = 2
		self.oneUpBonuses = [False,False]
		self.font = pygame.font.Font(join("resources","fonts","Verdana.TTF"),12)
		self.pointsLabel = self.font.render("Points: ", True, RGB_WHITE)
		self.pointsString = self.font.render(str(self.points), True, self.pointsColor)
		self.levelLabel = self.font.render("Level: ", True, RGB_WHITE)
		self.levelString = self.font.render(str(self.level), True, RGB_WHITE)
		self.gameOver = False
		
	def play(self):
		"The main game loop occurs here, checks for keyboard input, updates game state, etc..."
		self.running = True
		lastLevelUpTime = time.time()
		#Excellent suggestions from Peter Nosgoth to have tighter control over Mouse
		pygame.mouse.set_visible(False)
		pygame.event.set_grab(True)
		
		while 1:
			for event in pygame.event.get():
				if event.type == pygame.QUIT: exit()
				
			keys = pygame.key.get_pressed()
			mouse_x = pygame.mouse.get_pos()[0]
			button1,button2,button3 = pygame.mouse.get_pressed()
			
			#print "mouse_x = %s"%mouse_x
			mousePosEqual = True
			while mousePosEqual:
				mousePosEqual = mouse_x != self.paddle.rect.left
				if mouse_x < self.paddle.rect.left:
					self.paddle.moveLeft(1)
				elif mouse_x > self.paddle.rect.left:
					if self.paddle.rect.right < self.width:
						self.paddle.moveRight(1)
					else:
						mousePosEqual = False

			if keys[K_SPACE] or button1:
				if self.ball.stuck:
					self.ball.stuck = False
			elif keys[K_RETURN] or button2 or button3:
				if not self.ball.stuck:
					if self.numLives >=1:
						self.numLives -=1
						self.reset()
						#print "self.numLives = %s"%self.numLives
					else:
						self.running = False
						self.endgame()
			elif keys[K_y]:
				if self.gameOver:
					print "K_y pressed launch brand new game"
					self.startGame()
			elif keys[K_ESCAPE]:
				print "K_ESCAPE pressed launch brand new game"
				exit()
		
			if self.running:
				self.checkBallCollision()
				hitWall = self.ball.autoMove()
				if hitWall:
					self.soundManager.play('cartoon-spring-sound',[0.2,0.2])
					print self.ball
				
				self.pointsString = self.font.render(str(self.points), True, self.pointsColor)
				self.updateScreen()
				
				if not self.ball.stuck:
					if self.checkBallOffScreen():
						self.running = False
						self.pointsColor = RGB_RED
						if self.numLives == 0:
							self.endgame()
					
					if self.checkLevelUp():
						self.level += 1
						self.levelString = self.font.render(str(self.level), True, RGB_WHITE)
						self.bricks = self.loadBricks()
						self.speed = 1
						self.ball = Ball(join("resources","images","ball-mini.png"))
						self.paddle = Paddle(join("resources","images","paddle.png"),self.ball)
					

			
				#Wait a couple of milliseconds
				currentTime = time.time()
				if(currentTime - lastLevelUpTime > 15):
					lastLevelUpTime = currentTime
					if (STARTSPEED - self.speed > 0):
						#print "15 s elapsed increasing speed by 1"
						self.speed +=1
					#else:
						#print "reached max speed"
				
			pygame.time.wait(STARTSPEED - self.speed)
		
	def checkBallCollision(self):
		if(self.ball.rect.colliderect(self.paddle.rect)):
			#Check if it is a vertical collision or horizontal collision
			leftTen = self.paddle.rect.left + 10
			rightTen = self.paddle.rect.left + 30
			if self.ball.rect.left < leftTen:
				self.ball.x_dir = -1
				self.ball.y_dir = -1 * self.ball.y_dir
			elif self.ball.rect.left > rightTen:
				self.ball.x_dir = 1
				self.ball.y_dir = -1 * self.ball.y_dir				
			else:
				self.ball.y_dir = -1
			#paddle and ball collided, play appropriate sound
			self.soundManager.play('cartoon-blurp-sound',[0.3,0.3])
		#check for collision with any non-destroyed bricks
		for brick in self.bricks:
			if(brick.isDestroyed):
				pass
			elif(self.ball.rect.colliderect(brick.rect)):
				if not brick.isDestructible:
					#indestructible brick and ball collided, play appropriate sound
					self.soundManager.play('cartoon-blurp-sound',[0.3,0.3])
				testpointright = self.ball.rect.left+self.ball.rect.width+1,self.ball.rect.top
				testpointleft = self.ball.rect.left-1,self.ball.rect.top
				testpointtop = self.ball.rect.left,self.ball.rect.top-1
				testpointbottom = self.ball.rect.left,self.ball.rect.top+self.ball.rect.height+1
				
				if(brick.rect.collidepoint(testpointright)):
					#test if the right side of the ball collided with the brick
					self.ball.x_dir = -1
				elif(brick.rect.collidepoint(testpointleft)):
					#test if the left side of the ball collided with the brick
					self.ball.x_dir = 1
				
				if(brick.rect.collidepoint(testpointtop)):
					#test if top of ball collided with brick
					self.ball.y_dir = 1
				elif(brick.rect.collidepoint(testpointbottom)):
					#test if the bottom of the ball collided with the brick
					self.ball.y_dir = -1
				
				self.points += brick.pointValue
				
				if(brick.isDestructible):
					brick.isDestroyed = True
					self.numDestructibleBricks -=1
					self.soundManager.play('punchhard',[0.3,0.3])
					#only give out bonuses when a destructible brick is hit
					if (self.points == 500 and not self.oneUpBonuses[0]):
						self.numLives +=1
						self.soundManager.play('triangle',[0.3,0.3])
						self.oneUpBonuses[0] = True
					elif (self.points == 1500 and not self.oneUpBonuses[1]):
						self.numLives +=1
						self.soundManager.play('triangle',[0.3,0.3])
						self.oneUpBonuses[1] = True
					#print "numDestructibleBricks = %s"%self.numDestructibleBricks
				break
	
	def checkLevelUp(self):
		if self.numDestructibleBricks == 0:
			return True
		return False

	def checkBallOffScreen(self):
		if(self.ball.rect.top >= GB_HEIGHT):
			return True
		return False
	
	def endgame(self):
		#print "endgame called!"
		if self.gameOver:
			return
		self.gameOverLabel = self.font.render("GAME OVER", True, RGB_WHITE)
		self.playAgainLabel = self.font.render("Play Again?", True, RGB_WHITE)
		self.instructionsLabel = self.font.render("YES (y) / NO (ESC)", True, RGB_WHITE)
		self.screen.blit(self.gameOverLabel,(100, 40))
		self.pointsColor = RGB_RED
		self.screen.blit(self.playAgainLabel,(100, 75))
		self.screen.blit(self.instructionsLabel,(80, 95))
		self.gameOver = True
		pygame.display.flip()
			
if __name__ == '__main__':
	pygame.init()
	pygame.font.init()
	pygame.display.set_caption("PyBreakout")
	
	game = PyBreakout()
	game.initializeScreen()
	game.play()
				

