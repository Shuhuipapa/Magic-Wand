#!/bin/bash
echo "wingardium leviosa video"
sudo SDL_VIDEODRIVER=fbcon SDL_FBDEV=/dev/fb1 mplayer -vo sdl -framedrop /home/pi/video/wingardium.mp4