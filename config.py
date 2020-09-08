import os
import pygame
import math
import random

#size of the final display
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

#total size of the screen before scaling
TOTAL_WIDTH = 1300
TOTAL_HEIGHT = 1000

BORDER_WIDTH = 200
BORDER_HEIGHT = 100

#area of the playable area
GAME_WIDTH = 600
GAME_HEIGHT = 800

INFO_WIDTH = 200
INFO_HEIGHT = TOTAL_HEIGHT

PLAYER_START_POS = ( GAME_WIDTH / 2.0, GAME_HEIGHT - 50)

window = 0
gameArea = 0

startLives = 4

bullets = []
deadBullets = [] #bullets slated for removal
magicBullets = [] #they can change their path mid-flight!!
enemies = []
collidables = []
attacks = {}
waveInfo = []
clearBulletsFlag = False
currentWave = 3
font = 0




#===============
#	Functions
#===============
#contains all images loaded by get_image
_image_library = {}

#Gets specified image, initializes if necessary
def get_image(path):
	global _image_library
	image = _image_library.get(path)
	if image == None:
		canonicalized_path = ('Images\\' + path).replace('/', os.sep).replace('\\', os.sep)
		image = pygame.image.load(canonicalized_path).convert_alpha()
		_image_library[path] = image
	return image
	
_sound_library = {}
def play_sound(path):
  global _sound_library
  sound = _sound_library.get(path)
  if sound == None:
    canonicalized_path = ('Sounds/' + path)
    sound = pygame.mixer.Sound(canonicalized_path)
    _sound_library[path] = sound
  sound.play()
  
#angle between two points
def angle( p1, p2):
	(dx, dy) = (p2[0] - p1[0], p2[1] - p1[1] )
	angle = math.degrees( math.atan2(dy, dx) ) + 180 - 90
	
	return angle
	
def distance(p1, p2):
	return math.sqrt( (p1[0] - p2[0] )**2 + (p1[1] - p2[1] )**2 ) 
	
	

	