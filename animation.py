import pygame
import config

START_FRAME = 0
END_FRAME = 1
FRAME_TIME = 2

animationList = {}
animationList["idle"] = (0,0,-1)

def setAnimation( name, startFrame, endFrame, frameTime):
	animationList[name] = (startFrame, endFrame, frameTime)

class Animator:
	def __init__(self, image, window, clipx, clipy, x, y):
		self.image = image
		self.window = window
		self.x = x
		self.y = y
		self.defaultAnim = "idle"
		self.anim = setAnimation
		self.animPos = 0
		self.animFrame = 0
		self.image.set_clip((0,0), (image.get_width(), image.get_height() ) )

	def draw(self):
		window.blit( self.image, (self.x, self.y) )

	#copies variables from animationList given a name
	def setAnimation(self, aName ):
		self.anim = animationList[aName]
		self.animPos = 0
		self.animFrame  = 0
		
		
	#this updates the clip area based on current held information
	def updateFrame(self):
		#something
		a
	
	#this updates information, calls updateFrame if necessary
	def update(self):
		#move animation forward one frame
		self.animFrame+= 1
		
		if(animationList(self.anim[FRAME_TIME] == self.animFrame ) ):
			#go to clip area
			animPos += 1
			self.updateFrame()
			
			