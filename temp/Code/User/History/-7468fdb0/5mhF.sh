#!/bin/bash
xrandr --output eDP-1 --off --output HDMI-1 --mode 1920x1080 --rotate normal --rate 75 --primary &
feh --bg-fill /home/atg/Pictures/Wallpapers/garrhet-sampson-CmF_5GYc6c0-unsplash.jpg &
dunst &
clipmenud &
/usr/lib/polkit-gnome/polkit-agent-helper-1 &