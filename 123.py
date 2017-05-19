######################################################
# 
# Project: Magic wand
# File:     123.py win.sh lumos.sh stupefy.sh
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
    #Invoke IoT (or any other) actions here
    #cv2.putText(frame, spell, (5, 25),cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0,255,0),2)
    
    if (spell=="Wingardium Leviosa" ):
        #print "GPIO trinket"
        subprocess.call("./win.sh")
        #pi.write(trinket_pin,0)
        #time.sleep(1)
        #pi.write(trinket_pin,1)
    if (spell=="Lumos" ):
        #print "GPIO ON"
        subprocess.call("./lumos.sh")
        #print("123")
        #pi.write(switch_pin,1)
    if (spell=="Stupefy" ):
        #print "GPIO OFF"
        #pi.write(switch_pin,0)
        subprocess.call("./stupefy.sh")
    open('stt.txt','w').close()
def IsGesture(a,b,c,d):
    #record basic movements - TODO: trained gestures
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
#	for event in pygame.event.get():
#	 if(event.type is pygame.MOUSEBUTTONDOWN):
#	  pos=pygame.mouse.get_pos()
#	  x,y=pos
#	  if x<80:
#		print "start"
		rval, frame = cam.read()
		frame=cv2.flip(frame,0)
		frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		b,g,r = cv2.split(frame)
		frame_gray=b
		#edge=cv2.Canny(frame_gray,n,n/2)
		ret,thresh=cv2.threshold(frame_gray,th,255,cv2.THRESH_BINARY)
		contours,hier=cv2.findContours(thresh,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
		cv2.drawContours(frame_gray,contours,-1,(0,0,255))
		p0=[]
		mask = np.zeros_like(frame_gray)
		#if len(contours)>1:
		#cv2.putText(frame, "Too bright to cast dark spells", (80,220), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0),2)
		for cnt in contours:
		   cx_old=cx
		   cy_old=cy
		   p=cv2.arcLength(cnt,True)
                   s=cv2.contourArea(cnt)
		   if s!=0:
                   	c=p*p/s
		   if 4<cv2.contourArea(cnt):# and c<25:
			try:
				M=cv2.moments(cnt)
				#cy_old=cy
				#cx_old=cx
				#p=cv2.arcLength(cnt,True)
				#s=cv2.contourArea(cnt)
				#c=p*p/s
				cy=int(M['m01']/M['m00'])
				cx=int(M['m10']/M['m00'])
				#dist = math.hypot(cx - cx_old, cy - cy_old)
				#if movement distance > value && <80, consider it is a pattern movement
				#if 5<dist<80:
					#cv2.line(mask, (a,b),(c,d),(0,255,0), 2)
					#IsGesture(a,b,c,d,i)
				cv2.circle(frame,(cx,cy),2,(0,0,255),2)
				p0.append([cx,cy])
			except:
				pass
		#if first:
		#p0=[p0]
		#cx_old=cx
		#cy_old=cy
#		pygame.display.set_caption('Hello World!')
#		clip = VideoFileClip('Untitled.mp4')
#		clip.preview()
#		omxplayer /home/pi/Untitled.mp4
		for event in pygame.event.get():
		 if(event.type is pygame.MOUSEBUTTONDOWN) :
                  pos=pygame.mouse.get_pos()
      		  x,y=pos
		  if x<80:
		   print "start"
		   subprocess.Popen("./speak.sh")
                   #with open("stt.txt") as f:
                    #data="".join(line.rstrip() for line in f)
                   #font=pygame.font.Font(None,50)
                   #text_surface=font.render(data,True,GREEN)
                   #rect=text_surface.get_rect(center=(100,100))
                   #screen.blit(text_surface,rect)
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

		#print(p0)
		#print("\n")
			#first=0	
		#circle=minEnclosingCircle(contours)	
		#cv2.circle(frame_gray,circle,(0,0,255),1)
		#p0 = cv2.HoughCircles(frame_gray,cv2.cv.CV_HOUGH_GRADIENT,3,100,param1=100,param2=30,minRadius=4,maxRadius=15)
		#a=cv2.add(frame_gray)
		cv2.imshow('test',frame)
		#cv2.imshow('gray',frame_gray)
		cv2.waitKey(1)
