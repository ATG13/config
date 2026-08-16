#!/bin/bash
#

#exec /usr/local/bin/launch.sh &
#ssh-add &
#swww query || swww init & 
#pypr &
#exec ~/.config/hypr/scripts/suspend.sh &
#flatpak run com.nextcloud.desktopclient.nextcloud &
#flatpak run com.borgbase.Vorta &
#flatpak run com.core447.StreamController &
#dunst & 
#hyprctl setcursor Bibita-Modern-Ice 24 &
#/usr/libexec/polkit-gnome-autentication-agent-1 &

monitors=$(hyprctl monitors -j | jq -r '.[] | .name')

if [[ $monitors == *"DP-1"* ]]; then
  # DP-1 is connected, configure both monitors
  hyprctl monitor DP-1,1920x1080@74.97,0x0,1.0, workspace, 1-10
  #hyprctl monitor eDP-1,1920x1080@60,-1920x0,1.5, workspace, 11
else
  # DP-1 is not connected, configure only eDP-1
  hyprctl monitor eDP-1,1920x1080@60,0x0,1.5, workspace, 1-10
fi 

flatpak run app.zen_browser.zen

swaybg --image ~/Pictures/Wallpapers/gruvbox_forest-4.png
