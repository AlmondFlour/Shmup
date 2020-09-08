import pygame
import bullet
import attack
import config
import math
import random

enemies = []
def clearEnemies():
	for n in range( len(config.enemies) ) :
		e = config.enemies.pop()
		del e

class Player :
	def __init__(self, window, image, pos, lives = 4 ):
		self.window = window
		self.image = image
		self.pos = pos
		self.vx = 0
		self.vy = 0
		self.focus = 0
		self.radius = image.get_width() / 8
		self.xOffset = image.get_width() / 2
		self.yOffset = image.get_height() / 2
		
		self.iFramesStart = 180
		self.iFrames = 0
		
		self.firing = False
		self.lives = lives
		self.graze = 0
		
		self.hitCount = 0 #dubugging only
		
	def draw(self):
		if( (self.iFrames % 2)  == 0 ):
			self.window.blit(self.image, (self.pos[0] - self.xOffset, self.pos[1] - self.yOffset ) )
		#pygame.draw.circle(self.window, pygame.Color( 50, 0, 255, 1 ), ( int(self.pos[0]) , int(self.pos[1] )) , self.radius)
		
	def update(self):
		pressed = pygame.key.get_pressed()
		
		if pressed[pygame.K_UP]: self.vy = -4
		elif pressed[pygame.K_DOWN]: self.vy = 4
		else: self.vy = 0
		if pressed[pygame.K_LEFT]: self.vx = -4
		elif pressed[pygame.K_RIGHT]: self.vx = 4
		else: self.vx = 0

		if pressed[pygame.K_LSHIFT]: self.focus = 0.5
		else : self.focus = 1
		
		x, y = self.pos
		x += self.vx * self.focus
		y += self.vy * self.focus
		
		if( x < 0) :  x = 0
		elif( x > self.window.get_width() - self.image.get_width()  ) : x = self.window.get_width() - self.image.get_width() 
		if( y < 0) :  y = 0
		elif( y > self.window.get_height() ) : y = self.window.get_height()
		
		self.pos = ( x, y )
#		self.pos = ( self.pos[0] + (self.vx * self.focus), self.pos[1] + (self.vy * self.focus) )
		
#		if( self.pos[0] < 0) :  self.pos[0] = 0
#		elif( self.pos[0] > self.window.get_width() ) : self.pos[0] = self.window.get_width()
#		if( self.pos[1] < 0) :  self.pos[1] = 0
#		elif( self.pos[1] > self.window.get_height() ) : self.pos[1] = self.window.get_height()

		if( self.iFrames > 0 ):
			self.iFrames -= 1

		if(self.firing):
			self.fire()
		
	def hit(self):
		if( self.iFrames <= 0 ):
			self.iFrames = self.iFramesStart
			self.hitCount += 1
			print( "Player has been hit", self.hitCount, "times!")
			config.clearBulletsFlag = True
			config.play_sound('Game Overold.wav')
			self.pos = config.PLAYER_START_POS
			self.lives += -1
		
class Enemy :
	currentId = 0
	def __init__(self, window, image, pos, destination, vel = 2, attack = None ):
		self.window = window
		self.image = image
		self.pos = pos
		self.vel = vel
		self.aVel = 0
		
		self.destination = destination
		#(dx, dy) = (destination[0] - pos[0], destination[1] + pos[1] )
		#self.angle = math.atan(float(dx)/float(dy)) * (180/math.pi) + 180
		
		self.angle = config.angle(pos, destination)
		
		self.radius = image.get_width() / 2
		self.xOffset = image.get_width() / 2
		self.yOffset = image.get_height() / 2
		
		self.id = Enemy.currentId
		Enemy.currentId += 1
		
		self.attackList = []
		if( attack != None ):
			self.attackList.append(attack)
		
	def draw(self):
		self.window.blit(self.image, (self.pos[0] - self.xOffset, self.pos[1] - self.yOffset ) )
#		pygame.draw.circle(self.window, pygame.Color( 50, 255, 50, 1 ), ( int(self.pos[0]) , int(self.pos[1] )) , self.radius)

	def update(self):
		self.angle = self.angle + self.aVel
		vx = self.vel * math.sin( math.radians( self.angle) )
		vy = self.vel * math.cos( math.radians( self.angle) )
		
		x = self.pos[0] + vx
		y = self.pos[1] - vy
		
		#snap to destination
		if( self.destination != None ):
			x2, y2 = self.destination
			if( ((x - x2)**2 + (y - y2)**2) <= (self.vel * 2) **2 ):
				self.pos = self.destination
				self.attackList[0].firing = True
			else:
				self.pos = (x,y)
		else:
			self.pos = (x, y)
			
		if( self.destination != None and self.attackList[0].finishedFiring):
			self.destination = None
			self.angle = 90 - ( 180 * random.random() )
			if( self.vel < 1.5 ):
				self.vel = 1.5
		
		#offscreen
		if(  0 - 50 > x or x > config.window.get_width() + 50 or  0 - 50 > y or y > config.window.get_height() + 50 ):
			return self.id
		
		#check player colision
		for n in config.collidables :
			x2, y2 = n.pos
			if( ((x - x2)**2 + (y - y2)**2) < (self.radius + n.radius - 1) **2 ):
				n.hit()
				return self.id
				
		for a in self.attackList :
			a.update(self.pos)
			
		return -1
		
	def __eq__(self, other):
		if self.id == other.id:
			return True
		return False
		
	#fires given attack at a position
	def fire(self, attack, pos):
		pass
		
		