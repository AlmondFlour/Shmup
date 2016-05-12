import pygame
import math
import config

def clearBullets():
	for b in config.bullets :
		b.prepareRemoval()

#base bullet class, a lot of patterns will need a modified version
class Bullet:
	currentId = 0
	def __init__(self, window, image, pos, destination = None):
		self.image = image
		self.pos = pos
		self.window = window
		
		
		self.destination = destination
		if( destination == None ):
			self.angle = 180
		else:
			self.angle = config.angle( pos, destination)
		self.aVel = 0
		self.aAcc = 0
		self.vel = 2
		self.acc = 0
		self.radius = (image.get_width() * 3 ) / 8
		
		#these are applied in addition to angle based velocity (can be easier to control)
		self.vx = 0
		self.vy = 0
		
		self.id = Bullet.currentId
		Bullet.currentId += 1
		self.xOffset = image.get_width() / 2
		self.yOffset = image.get_height() / 2
		
		self.dead = False
		self.grazed = False
		
		#all lists this bullet is a member of aside from config.bulletList
		self.activeLists = [] 
		
	def draw( self):
		self.window.blit(self.image, (self.pos[0] - self.xOffset, self.pos[1] - self.yOffset ) )
		#pygame.draw.circle(self.window, pygame.Color( 255, 50, 50, 1 ), ( int(self.pos[0]) , int(self.pos[1] )) , self.radius)
		
	def update(self):
		self.aVel = self.aVel + self.aAcc
		self.angle = self.angle + self.aVel
		self.vel = self.vel + self.acc
	
		x = self.pos[0] + ( self.vel * math.sin( math.radians( self.angle) ) ) + self.vx
		y = self.pos[1] - ( self.vel * math.cos( math.radians( self.angle) ) ) + self.vy
		self.pos = (x, y)
		
		if(  0 - 50 > x or x > self.window.get_width() + 50 or  0 - 50 > y or y > self.window.get_height() + 50 ):
			self.prepareRemoval()
			return
			
		for n in config.collidables :
			x2, y2 = n.pos
			if( ((x - x2)**2 + (y - y2)**2) < (self.radius + n.radius - 1) **2 ):
				n.hit()
				self.prepareRemoval()
				return
				
			if not self.grazed and ( ((x - x2)**2 + (y - y2)**2) < ((self.radius + n.radius ) + 25 ) **2 ):
				n.graze += 1
				self.grazed = True
			
		return -1
		
	def __eq__(self, other):
		if self.id == other.id:
			return True
		return False
	
	#creates a copy with everything in base bullet class, except id
	def copy(self):
		b = Bullet(self.window, self.image, self.pos, self.destination)
		b.angle = self.angle
		b.aVel = self.aVel
		b.aAcc = self.aAcc
		b.vel = self.vel
		b.acc = self.acc
		b.radius = self.radius
		
	def setDest(self, dest):
		self.destination = dest
		self.angle = config.angle( self.pos, dest)
		
	#deletes from all lists except the main bulletList and sets delete flag
	def prepareRemoval(self):
		if( not self.dead ):
			self.dead = True
			config.deadBullets.append(self)
			for l in self.activeLists:
				l.remove(self)
			
	def addToList( self, list ):
			list.append(self)
			self.activeLists.append(list)
			
	def removeFromList( self, list ):
			list.remove(self)
			self.activeLists.remove(list)
		
	
def clearBullets():
	for b in config.bullets :
		b.prepareRemoval()

class PlayerBullet:
	currentId = 0
	def __init__(self, window, image, pos, destination = None):
		self.image = image
		self.pos = pos
		self.window = window
		
		
		self.destination = destination
		if( destination == None ):
			self.angle = 180
		else:
			self.angle = config.angle( pos, destination)
		self.aVel = 0
		self.aAcc = 0
		self.vel = 2
		self.acc = 0
		self.radius = (image.get_width() * 3 ) / 8
		
		#these are applied in addition to angle based velocity (can be easier to control)
		self.vx = 0
		self.vy = 0
		
		self.id = PlayerBullet.currentId
		PlayerBullet.currentId += 1
		self.xOffset = image.get_width() / 2
		self.yOffset = image.get_height() / 2
		
		self.dead = False
		self.grazed = False
		
		#all lists this bullet is a member of aside from config.bulletList
		self.activeLists = [] 
		
	def draw( self):
		self.window.blit(self.image, (self.pos[0] - self.xOffset, self.pos[1] - self.yOffset ) )
		#pygame.draw.circle(self.window, pygame.Color( 255, 50, 50, 1 ), ( int(self.pos[0]) , int(self.pos[1] )) , self.radius)
		
	def update(self):
		self.aVel = self.aVel + self.aAcc
		self.angle = self.angle + self.aVel
		self.vel = self.vel + self.acc
	
		x = self.pos[0] + ( self.vel * math.sin( math.radians( self.angle) ) ) + self.vx
		y = self.pos[1] - ( self.vel * math.cos( math.radians( self.angle) ) ) + self.vy
		self.pos = (x, y)
		
		if(  0 - 50 > x or x > self.window.get_width() + 50 or  0 - 50 > y or y > self.window.get_height() + 50 ):
			self.prepareRemoval()
			return
			
		for n in config.collidables :
			x2, y2 = n.pos
			if( ((x - x2)**2 + (y - y2)**2) < (self.radius + n.radius - 1) **2 ):
				n.hit()
				self.prepareRemoval()
				return
				
			if not self.grazed and ( ((x - x2)**2 + (y - y2)**2) < ((self.radius + n.radius ) + 25 ) **2 ):
				n.graze += 1
				self.grazed = True
			
		return -1
		
	def __eq__(self, other):
		if self.id == other.id:
			return True
		return False
	
	#creates a copy with everything in base bullet class, except id
	def copy(self):
		b = Bullet(self.window, self.image, self.pos, self.destination)
		b.angle = self.angle
		b.aVel = self.aVel
		b.aAcc = self.aAcc
		b.vel = self.vel
		b.acc = self.acc
		b.radius = self.radius
		
	def setDest(self, dest):
		self.destination = dest
		self.angle = config.angle( self.pos, dest)
		
	#deletes from all lists except the main bulletList and sets delete flag
	def prepareRemoval(self):
		if( not self.dead ):
			self.dead = True
			config.deadBullets.append(self)
			for l in self.activeLists:
				l.remove(self)
			
	def addToList( self, list ):
			list.append(self)
			self.activeLists.append(list)
			
	def removeFromList( self, list ):
			list.remove(self)
			self.activeLists.remove(list)		

		