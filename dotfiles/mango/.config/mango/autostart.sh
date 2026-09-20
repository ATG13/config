#!/usr/bin/bash

# 1. Start the keyring daemon
eval $(gnome-keyring-daemon --start --components=secrets,ssh,pkcs11)
export SSH_AUTH_SOCK

# 2. Export session environment variables
export XDG_CURRENT_DESKTOP=wlroots
export XDG_SESSION_TYPE=wayland

# 3. Synchronize environment with systemd and DBus
dbus-update-activation-environment --all
systemctl --user import-environment WAYLAND_DISPLAY XDG_CURRENT_DESKTOP XDG_SESSION_TYPE SSH_AUTH_SOCK

# 4. Start kanshi FIRST so monitors are configured before portals query outputs
kanshi -c ~/.config/kanshi/config &
sleep 1

# 5. Restart portal services via systemd (do not run the binary directly)
systemctl --user restart xdg-desktop-portal-wlr
systemctl --user restart xdg-desktop-portal

# 6. Background user applications
open-whispr &
duplicati &
kdeconnectd &
