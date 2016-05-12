import pygame
import config
import random
import bullet
import gameObj
from types import MethodType

#List of function for each wave
waveList = []

class Wave:
	def __init__(self, subWaves = 8):
		self.endWave = False
		self.spawnEnemies = True
		self.direction = -1
		self.waveSoundDelay = 9
		self.subWaves = subWaves
		self.spawnDelay = 120
		self.currentWait = 0
		self.counter = 0
		self.angles = []
		self.vars = {}
		
		self.bulletList = []
		
	def update(self):
		self.currentWait += 1
		self.waveSoundDelay += 1
		if( self.subWaves <= 0 and config.currentWave != len(waveList
		)):
			config.currentWave +=1
			bullet.clearBullets()
			gameObj.clearEnemies()
			self.subWaves = 4
		
def waveInit():
	
	
	#================
	# Wave 1
	#================
	w = Wave()
	w.subWaves = 8
	config.waveInfo.append(w)
	w.spawnDelay = 180
	w.counter = 0
	def wave1() :
		w = config.waveInfo[0]
		w.update()
		
	
		#enemy spawner
		if( w.currentWait >= w.spawnDelay ):
			w.currentWait = 0
			w.counter += 1
			numEnemies = 2**w.counter
			for n in range(numEnemies):
				destx = n * (config.GAME_WIDTH / numEnemies )
				desty = 150
				startx = n * (config.GAME_WIDTH / numEnemies )
				starty = -10
				vel = 2 + ( -1.5 * random.random() )
		
				e = gameObj.Enemy( config.gameArea, config.get_image('enemy.png'), (startx , starty ), (destx, desty ), vel, config.attacks['smallSingle'].copy() )
				config.enemies.append(e)
			for n in range(numEnemies):
				destx = config.GAME_WIDTH - (n * (config.GAME_WIDTH / numEnemies ) )
				desty = 200
				startx =config.GAME_WIDTH - (n * (config.GAME_WIDTH / numEnemies ) )
				starty = -10
				vel = 2 + ( -1.5 * random.random() )
		
				e = gameObj.Enemy( config.gameArea, config.get_image('enemy.png'), (startx , starty ), (destx, desty ), vel, config.attacks['smallSingle'].copy() )
				config.enemies.append(e)
			w.subWaves -= 1
			
	waveList.append(wave1)
	
	#================
	# Wave 2
	#================
	
	w = Wave()
	config.waveInfo.append(w)
	w.subWaves = 3
	
	def wave2() :
		w = config.waveInfo[1]
		w.update()
		
		w.spawnDelay = 65
	
		if( w.endWave ):
			if len(config.bullets) < 20 :
				w.endWave = False
				w.direction = w.direction * (-1)
				w.spawnEnemies = True
				w.subWaves -= 1
	
		#Bullet Spawner
		elif(  len(config.bullets) < 100 ):
			if(w.currentWait >= w.spawnDelay ):
				w.currentWait = 0
				if(w.waveSoundDelay <= 9 ):
					config.play_sound("Attack2.wav")
					w.waveSoundDelay = 0
					
				for n in range(25):
					b = bullet.Bullet( config.gameArea, config.get_image("bullet_small2.png"), (300, 4) )
					
					x = (n * ((config.GAME_WIDTH - 125) / 25 ) ) + (125 * w.direction)
					y = 0
					b.pos = (x,y)
					b.vel = 2.5
					config.bullets.append( b )
				for n in range(5):
					b = bullet.Bullet( config.gameArea, config.get_image("bullet_big.png"), (300, 4) )
					
					x = config.GAME_WIDTH * random.random()
					y = -10
					b.pos = (x,y)
					b.vel = 2
					b.aVel = 0.2 * w.direction
					b.vx = 0.25
					config.bullets.append( b )
				w.direction *= -1
		else:
			w.endWave = True
			
	waveList.append(wave2)
	
	#================
	# Wave 3
	#================
	
	w = Wave()
	config.waveInfo.append(w)
	w.subWaves = 4
	w.angles.append(135)
	w.angles.append(225)
	w.vars['aVel'] = 0.2 * random.random()
	
	def wave3() :
		w = config.waveInfo[2]
		w.update()
		w.spawnDelay = 6
		
		if( w.endWave ):
			if len(config.bullets) < 150 :
				w.endWave = False
				w.direction = w.direction * (-1)
				w.spawnEnemies = True
				w.subWaves -= 1
				w.angles[0] = 120 + (50 * random.random() )
				w.angles[1] = 240  - (50 * random.random() )
				w.vars['aVel'] = 0.2 * random.random()
	
		#Bullet Spawner
		elif(  len(config.bullets) < 600 ):
			if(w.currentWait >= w.spawnDelay ):
				w.currentWait = 0
				if(w.waveSoundDelay >= 8 ):
					config.play_sound("Attack2.wav")
					w.waveSoundDelay = 0
				for n in range(5):
					b = bullet.Bullet( config.gameArea, config.get_image("bullet_small.png"), (300, 4) )
					
					x = 0
					y = 0
					b.pos = (x,y)
					b.vel = 3
					b.angle = (w.angles[0]) - 50 + (n * 20)
					b.aVel = w.vars['aVel']
					b.vx = 0.75
					b.vy = -0.50
					config.bullets.append( b )
					
				for n in range(4):
					b = bullet.Bullet( config.gameArea, config.get_image("bullet_small.png"), (300, 4) )
					
					x = config.GAME_WIDTH
					y = 0
					b.pos = (x,y)
					b.vel = 3
					b.angle = (w.angles[1]) - 50 + (n * 20)
					b.aVel = w.vars['aVel'] * -1
					config.bullets.append( b )
					b.vx = -0.75
					b.vy = -0.5
					
				for n in range(4):
					b = bullet.Bullet( config.gameArea, config.get_image("bullet_small2.png"), (300, 4) )
					
					x = config.GAME_WIDTH * random.random()
					y = 0
					b.pos = (x,y)
					b.vel = 1 + 1.5 * random.random()
					#b.aVel = 0.075 * random.random()
					config.bullets.append( b )
					
				w.direction *= -1
		else:
			w.endWave = True
			
	waveList.append(wave3)
	
	#================
	# Wave 4
	#================
	w = Wave()
	config.waveInfo.append(w)
	w.subWaves = 8
	def wave4() :
		w = config.waveInfo[3]
		w.update()
	
		#enemy spawner
		if( w.currentWait >= w.spawnDelay and len(config.enemies) <= 15 ):
			w.currentWait = 0
			#small bullets
			for n in range(15):
				destx =n * 40
				desty = 150 + (50 * (n % 2 ) )
				startx = n * 30
				starty = -10
				vel = 2
		
				e = gameObj.Enemy( config.gameArea, config.get_image('enemy.png'), (startx , starty ), (destx, desty ), vel, config.attacks['smallStream'].copy() )
				config.enemies.append(e)
			#big bullets
			for n in range(5):
				destx = n * ( config.GAME_WIDTH / 5 )
				desty = 150 + (50 * (n % 2 ) )
				startx = n * ( config.GAME_WIDTH / 5 )
				starty = -10
				vel = 3
				
				attack = config.attacks['bigSingle'].copy()
				attack.magicBullets = True
		
				e = gameObj.Enemy( config.gameArea, config.get_image('enemy.png'), (startx , starty ), (destx, desty ), vel, attack )
				e.attackList[0].image = config.get_image('bullet_big2.png')
				config.enemies.append(e)
			
			for b in config.magicBullets:
				b.setDest(config.collidables[0].pos)
				#b.vel = b.vel + 0.2
			
			w.subWaves -= 1
			
	waveList.append(wave4)
	
	#================
	# Wave 5
	#================
	w = Wave()
	config.waveInfo.append(w)
	w.subWaves = 6
	w.spawnDelay = 20
	w.vars['angle'] = 180
	w.vars['angle2'] = 90
	w.vars['extraBullets'] = []
	w.vars['extraDelay'] = 15
	w.vars['extraWait'] = 0
	
	def wave5() :
		w = config.waveInfo[4]
		w.update()
		
		if( w.endWave ):
			if len(config.bullets) < 80 + len(config.magicBullets) + len(w.vars['extraBullets']) :
				w.endWave = False
				w.direction = w.direction * (-1)
				w.spawnEnemies = True
				w.subWaves -= 1
				#w.vars['angle'] = 90 + ( 135 * random.random() )
				#w.vars['angle2'] = 360 * random.random()
	
		#Homing Corner Spawners
		elif(  len(config.bullets) < 120 + len(config.magicBullets) + len(w.vars['extraBullets']) ):
			if(w.currentWait >= w.spawnDelay ):
				w.currentWait = 0
				if(w.waveSoundDelay >= 8 ):
					config.play_sound("Attack2.wav")
					w.waveSoundDelay = 0
					
				
				for n in range(3):
					b = bullet.Bullet( config.gameArea, config.get_image("bullet_small2.png"), (300, 4) )
					
					x = 0
					y = 0
					b.pos = (x,y)
					b.vel = 2
					 
					
					(x, y) = config.collidables[0].pos
					x += ( n *  200 ) - 200
					b.setDest((x,y))
					#b.angle = 90 + (random.random() * 90)
				
					config.bullets.append( b )
					
				for n in range(3):
					b = bullet.Bullet( config.gameArea, config.get_image("bullet_small2.png"), (300, 4) )
					
					x = config.GAME_WIDTH
					y = 0
					b.pos = (x,y)
					b.vel = 2
					#b.angle = 180 + (random.random() * 90)
					(x, y) = config.collidables[0].pos
					x += ( n*  200 ) - 200
					b.setDest((x,y))
				
					config.bullets.append( b )
					
				w.direction *= -1
		else:
			w.endWave = True
		
		
		w.vars['extraWait'] += 1
		if( w.vars['extraWait'] >= w.vars['extraDelay'] ):
			w.vars['extraWait'] = 0
			#spawn small bullets on big bullets
			for n in config.magicBullets:
					b = bullet.Bullet( config.gameArea, config.get_image("bullet_small.png"), (300, 4) )
					
					x = n.pos[0]
					y = n.pos[1]
					b.pos = (x,y)
					b.addToList(w.vars['extraBullets'])
					b.vel = 0
					config.bullets.append(b)
					
			
			if( len( config.magicBullets ) == 0):
				#w.vars['angle2'] = 45 + ( random.random() * 90 )
				#spawn big bullets
				for n in range(6):
					b = bullet.Bullet( config.gameArea, config.get_image("bullet_big.png"), (300, 4) )
					
					x = config.GAME_WIDTH / 2
					y = config.GAME_HEIGHT / 20
		
					b.pos = (x,y)
					w.vars['angle2'] = config.angle( b.pos, config.collidables[0].pos)
					b.vel = 4
					b.angle = w.vars['angle2'] + ((n - 3) * ( 235 / 6 ) )
					b.aVel = 0
					
					b.addToList(config.magicBullets)
					config.bullets.append( b )
					
				#move spawned bullets
				for n in range(len( w.vars['extraBullets'] ) )[::-1]:
					b = w.vars['extraBullets'][n]
					if( b.vel == 0 ):
						(x, y) = config.collidables[0].pos
						if( b.pos[0] < config.GAME_WIDTH / 3.0 ):
							x += 100
						elif( b.pos[0] > (config.GAME_WIDTH * 2) / 3.0):
							x -= 100
						b.setDest((x,y) )
						 
						#b.vel = 0.25 + ( config.distance( b.pos, (x,y) ) / 240 )
						b.vel = 2
 					
					#w.vars['extraBullets'][n].removeFromList(w.vars['extraBullets'] )
			
		#spawn big bullets
		#w.vars['angle2'] = 360 * random.random()
		
			
	waveList.append(wave5)
	
	
	#================
	# Final Wave
	#================
	
	w = Wave()
	config.waveInfo.append(w)
	w.spawnEnemies = False
	
	def waveFinal() :
		w = config.waveInfo[5]
		w.update()
	
		#enemy spawner
		if( w.spawnEnemies ):
			for n in range(15):
				destx =n * 40
				desty = 150 + (50 * (n % 2 ) )
				startx = n * 30
				starty = -10
				vel = 2
		
				e = gameObj.Enemy( config.gameArea, config.get_image('enemy.png'), (startx , starty ), (destx, desty ), vel, config.attacks['bigStream'].copy() )
				config.enemies.append(e)
			w.spawnEnemies = False
		
		
		if( w.endWave ):
			if len(config.bullets) < 150 :
				w.endWave = False
				w.direction = w.direction * (-1)
				w.spawnEnemies = True
				w.subWaves -= 1
	
		#Spiral Spawner
	
		#Bullet Spawner
		elif( len(config.bullets) < 800 ):
			if(w.waveSoundDelay <= 9 ):
				config.play_sound("Attack2.wav")
				w.waveSoundDelay = 0
				
			angle = 90 + (180 * random.random() )
			vel = 1 + (2 * random.random() )
			aAcc = -0.005 + (0.01 * random.random() )
			
			for n in range(5):
				b = bullet.Bullet( config.gameArea, config.get_image("bullet_small2.png"), (300, 4) )
				b.angle = angle - 25 + ( 10 * n )
				b.vel = vel
				
				b.vx = w.direction
				b.vy = 0.30
				b.aAcc = aAcc
				config.bullets.append( b )
		else:
			w.endWave = True
		
	waveList.append(waveFinal)

