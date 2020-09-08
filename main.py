import pygame
import animation
import bullet
import random
import gameObj
import attack
import config
import waves
import os

pygame.init()
pygame.font.init()
waves.waveInit()
os.environ['SDL_VIDEO_WINDOW_POS'] = str(0) + "," + str(0)

#===============
#	Setup
#===============

#====Gameloop Variables
#config.window = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT), pygame.FULLSCREEN)
config.window = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT), pygame.NOFRAME)
config.font = pygame.font.Font( pygame.font.get_default_font(), 18 )
done = False
pause = False
clock = pygame.time.Clock()
gameArea = pygame.Surface((config.GAME_WIDTH, config.GAME_HEIGHT))
config.gameArea = gameArea
infoArea = pygame.Surface( ( config.INFO_WIDTH, config.INFO_HEIGHT ) )
unscaledArea = pygame.Surface((config.TOTAL_WIDTH, config.TOTAL_HEIGHT))


info = pygame.display.Info()
print( info )

#===Initilize Sound

SONG_END = pygame.USEREVENT + 1
pygame.mixer.music.set_endevent(SONG_END)
pygame.mixer.music.load('Sounds/th06_02.ogg')
#pygame.mixer.music.load('Sounds/th06_14.wav')
pygame.mixer.music.play()
musicChange = True

#===Initialize Player
playerImage = config.get_image("player.png")
player = gameObj.Player(gameArea, playerImage, config.PLAYER_START_POS )
config.collidables.append(player) #things enemies can hit
player.lives = config.startLives

#===Initilize Bullets
bulletImage = config.get_image("bullet_small2.png")
bullets = [] #this is just a more convenient config.bullets
config.bullets = bullets

#===Initialize Attacks
bigStream = attack.Attack(gameArea, config.get_image("bullet_big.png"), player, 70, 5, 4)
bigSingle = attack.Attack(gameArea, config.get_image("bullet_big.png"), player, 20, 1, 1)
smallStream = attack.Attack(gameArea, config.get_image("bullet_small.png"), player, 20, 8, 3)
smallSingle = attack.Attack(gameArea, config.get_image("bullet_small.png"), player, 20, 1, 4)


config.attacks["bigStream"] = bigStream
config.attacks["smallStream"] = smallStream
config.attacks["smallSingle"] = smallSingle
config.attacks["bigSingle"] = bigSingle

#===Initialize Enemies
#e = gameObj.Enemy( gameArea, config.get_image('enemy.png'), (-5, 50 ), (config.GAME_WIDTH / 2, 50 ), 2, bigStream )
enemies = []



#waveSize = 25

#for n in range(waveSize):
#	b = bullet.Bullet(gameArea, bulletImage, ( n * (600 / waveSize ) , 25 ) )
#	#b.angle = 360 * random.random()
#	#b.vel = 0.5 + (2 * random.random())
#	b.aVel = 0.005 * n
#	#b.aAcc = 0.001 * n
#	b.acc = 0.0005 * n
#	
#	bullets.append (b)

#===============
# Game Loop
#===============
while not done:
	#============
	#	 Input
	#============
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True
		if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
			done = True
		if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
			pause = not pause
#		if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
#			sound.play()
		if event.type == SONG_END:
			if musicChange:
				pygame.mixer.music.play(-1, 19.08)
			if not musicChange:
				pygame.mixer.music.play(-1, 42.50)
	
	if(pause):
		continue
	
	
	#============
	#	Update 
	#============
	
	waves.waveList[config.currentWave]()
	
	for e in config.enemies:
		#update returns ID if it needs to be deleted
		if(e.update() != -1 ):
			config.enemies.remove(e)
			del e
	for b in bullets:
		#update returns ID if it needs to be deleted
		b.update()
			
	for n in range(len(config.deadBullets) )[::-1]:
		bullets.remove(config.deadBullets[n])
		config.deadBullets.remove(config.deadBullets[n])
		
	
	player.update()
	
	if( config.clearBulletsFlag ):
		config.clearBulletsFlag = False
		bullet.clearBullets()
	
	#============
	# Draw
	#============
	
	player.draw()
	
	for e in config.enemies:
		e.draw()
	
	for b in bullets:
		b.draw()
		
	infoArea.blit( config.font.render("Lives : " + str(player.lives), 0, (200,200,200) ), (50, 100) )
	infoArea.blit( config.font.render("Graze: " + str(player.graze), 0, (200,200,200) ), (50, 125) )
	infoArea.blit( config.font.render("Kills: ", 0, (200,200,200) ), (50, 150) )
	infoArea.blit( config.font.render("Wave: " + str(config.currentWave + 1), 0, (200,200,200) ), (50, 300) )
	if( player.lives < 0 ):
		done = True
	
	if( config.currentWave >= 2 and musicChange):
		pygame.mixer.music.load('Sounds/th06_09.ogg')
		musicChange = False
		pygame.mixer.music.play()
		
	unscaledArea.blit(gameArea, (config.BORDER_WIDTH, 0) )
	unscaledArea.blit(infoArea, (config.GAME_WIDTH + config.BORDER_WIDTH,0) )
	
	#config.window.blit( pygame.transform.scale(unscaledArea, (config.SCREEN_WIDTH, config.SCREEN_HEIGHT)), (0,0 ) )
	pygame.transform.scale(unscaledArea, (config.SCREEN_WIDTH, config.SCREEN_HEIGHT), config.window)
	#config.window.blit( unscaledArea, (0,0))
		
	pygame.display.flip()
	gameArea.fill((0, 0, 0))
	unscaledArea.fill( (76,80,136) )
	infoArea.fill( (76,80,136))
	clock.tick(60)
	#print len(config.enemies)
	#print len(bullets)
	#print clock.get_fps();
	#print pygame.mixer.music.get_busy()
