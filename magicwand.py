######################################################
# 
# Project: Magic wand
# File:     123.py speechtotext.sh win.sh lumos.sh stupefy.sh
# Authors:	Shuhui Ding(sd784) Yilong Zhong(yz995)
# Date:     May 2017
#
# “use Google speech recognition and opencv to do voice and gesture recognition and translate the combo to a certain movie”
######################################################

import io
import cv2
import os
import pygame
import time
import subprocess
from cv2 import *
from cv import *
import picamera
import numpy as np
import threading
import sys
import math
import time
import pigpio
cam = cv2.VideoCapture(0)
cam.set(3, 320)
cam.set(4, 240)
th=125
n=100
first=1
def Spell(spell):
    #clear all checks
    global ig
    ig=[]
    #Invoke actions here    
    if (spell=="Wingardium Leviosa" ):
        subprocess.call("./win.sh")
    if (spell=="Lumos" ):
        subprocess.call("./lumos.sh")
    if (spell=="Stupefy" ):
        subprocess.call("./stupefy.sh")
    open('stt.txt','w').close()
def IsGesture(a,b,c,d):
    #record basic movements 
    if ((a<(c-5))&(abs(b-d)<5)):
        ig.insert(0,"left")
    elif ((c<(a-5))&(abs(b-d)<5)):
        ig.insert(0,"right")
    elif ((b<(d-5))&(abs(a-c)<5)):
        ig.insert(0,"up")
    elif ((d<(b-5))&(abs(a-c)<5)):
        ig.insert(0,"down")
    #check for gesture patterns in array
    astr = ''.join(map(str, ig))
    with open("stt.txt") as f:
            data="".join(line.rstrip() for line in f)
    if "rightup" in astr and data == "lumos":
        Spell("Lumos")
    elif "rightdown" in astr and (data == "Stupify" or data == "Stupefy" or data == "stupify"):
        Spell("Stupefy")
    elif "leftdown" in astr and data == "Wingardium Leviosa":
        Spell("Wingardium Leviosa")
    #print astr


cx=0
cy=0
ig=[]
#the following codes are used only on piTFT
#os.putenv('SDL_VIDEODRIVER', 'fbcon') # Display on piTFT
#os.putenv('SDL_FBDEV', '/dev/fb1') #
#os.putenv('SDL_MOUSEDRV', 'TSLIB') # Track mouse clicks on piTFT
#os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')
pygame.init()
size=width,height=320,240
WHITE=(255,255,255)
BLACK=(0,0,0)
RED=(255,0,0)
GREEN=(0,255,0)
screen=pygame.display.set_mode(size)
#pygame.mouse.set_visible(False)
pygame.mouse.set_visible(True)
my_buttons={'Start':(60,200),'Quit':(260,200)}
img=pygame.image.load("cover.jpg")
imgrect=img.get_rect()
screen.blit(img,imgrect)
for my_text, text_pos in my_buttons.items():
 font=pygame.font.Font(None,50)
 text_surface=font.render(my_text,True,WHITE)
 rect=text_surface.get_rect(center=text_pos)
 screen.blit(text_surface,rect)
while True:

		rval, frame = cam.read()
		frame=cv2.flip(frame,0)
		#convert to grayscale image
		frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		b,g,r = cv2.split(frame)
		frame_gray=b
		#a way to detect wand tip is to use canny edge operator
		#edge=cv2.Canny(frame_gray,n,n/2)
		#do thresholding
		ret,thresh=cv2.threshold(frame_gray,th,255,cv2.THRESH_BINARY)
		#do contours finding
		contours,hier=cv2.findContours(thresh,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
		cv2.drawContours(frame_gray,contours,-1,(0,0,255))
		p0=[]
		for cnt in contours:
		   #assign old centroid coordinates
		   cx_old=cx
		   cy_old=cy
		   p=cv2.arcLength(cnt,True)
                   s=cv2.contourArea(cnt)
		   if s!=0:
			#compactness analysis, extract the blob which is more likely to a circle
                   	c=p*p/s
		   if 4<cv2.contourArea(cnt) and c<25:
			#Moments analysis, mainly for centroid drawing
			try:
				M=cv2.moments(cnt)
				cy=int(M['m01']/M['m00'])
				cx=int(M['m10']/M['m00'])
				cv2.circle(frame,(cx,cy),2,(0,0,255),2)
				p0.append([cx,cy])
			except:
				pass
		for event in pygame.event.get():
		 if(event.type is pygame.MOUSEBUTTONDOWN) :
                  pos=pygame.mouse.get_pos()
      		  x,y=pos
		  if x<80:
		   print "start"
		   #at the same time start speech recogition in background
		   subprocess.Popen("./speak.sh")

		 elif(event.type is pygame.MOUSEBUTTONUP):
                  pos=pygame.mouse.get_pos()
                  x,y=pos
                  if y>140:
                   if x>200:
                    quit()
                pygame.display.flip()
		try:
                        IsGesture(cx_old,cy_old,cx,cy)
                        if len(ig)>10:
                                ig.pop()
		except:
                        pass

		#display video by showing each frame
		cv2.imshow('test',frame)
		#cv2.imshow('gray',frame_gray)
		cv2.waitKey(1)
