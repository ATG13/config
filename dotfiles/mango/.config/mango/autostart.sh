#!/usr/bin/bash
# Export Wayland session environment
export XDG_CURRENT_DESKTOP=wlroots
export XDG_SESSION_TYPE=wayland

# Import environment into systemd and DBus user session
dbus-update-activation-environment --systemd WAYLAND_DISPLAY XDG_CURRENT_DESKTOP XDG_SESSION_TYPE
systemctl --user import-environment WAYLAND_DISPLAY XDG_CURRENT_DESKTOP XDG_SESSION_TYPE

# Restart portal services so they pick up the fresh environment
systemctl --user restart xdg-desktop-portal-wlr
systemctl --user restart xdg-desktop-portal
/usr/libexec/xdg-desktop-portal -r &
kanshi -c ~/.config/kanshi/config &
open-whispr
