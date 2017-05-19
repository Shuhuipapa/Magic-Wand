#!/bin/bash
echo "stupefy video"
sudo SDL_VIDEODRIVER=fbcon SDL_FBDEV=/dev/fb1 mplayer -vo sdl -framedrop /home/pi/video/Stupefycast.mp4