import pygame
import bullet
import config
import copy

#this is a base class with default behaviors; meant to be overwritten in attackInit
class Attack:
	def __init__(self, window, image, target, delay = 20, waves = 3, vel = 2):
		self.image = image
		self.target = target
		self.delay = delay
		self.waves = waves
		self.window = window
		self.vel = vel
		
		self.magicBullets = False
		
		self.finishedFiring = False
		self.firing = False
		self.tick = delay #counts up to delay between firing
		
		self.firedBullets = []
		
		
	#doesn't need to do anything here, just a place holder
	#used for modifying in flight bullets
	def update(self, pos):
		self.tick += 1
		if( not self.finishedFiring and self.firing and self.tick >= self.delay ):
			self.tick = 0
			self.fire(pos, self.target.pos)
			self.waves -= 1
			if( self.waves <= 0 ):
				self.finishedFiring = True
			
	
	def startFiring(self) :
		self.firing = True
		
	def stopFiring(self):
		self.firing = False
	
	#not meant to be called from outside
	#fires one bullet
	def fire(self, pos, dest):
		b = bullet.Bullet( self.window, self.image, pos, dest )
		b.vel = self.vel
		config.bullets.append(b)
		config.play_sound('Attack.wav')
		if( self.magicBullets):
			b.addToList(config.magicBullets)
		
		#firedBullets.append(b) #need a way to remove them
		
	def copy(self):
		a = Attack(self.window, self.image, self.target, self.delay, self.waves, self.vel )
		#a.target = self.target
		#a.image = self.image
		#a.window = self.window
		#a.tick = copy.deepcopy(self.tick)
		#a.waves = copy.deepcopy(self.waves)
		return a
		
		
		
		