#!/bin/bash

# Stop on first failure
# set -e

# Show each command
set -x

# Kiosk browser CHROME
# KIOSK_BROWSER_COMMAND="google-chrome"
# KIOSK_BROWSER_CONFIG="${HOME}/.config/google-chrome"
# KIOSK_BROWSER_CONFIG_TMP="/dev/shm/google-chrome"
# Copy chrome config dir to 
# cp -Rf $KIOSK_BROWSER_CONFIG $KIOSK_BROWSER_CONFIG_TMP

# Kiosk browser CHROOMIUM
KIOSK_BROWSER_COMMAND="chromium-browser"
KIOSK_BROWSER_CONFIG="${HOME}/snap/chromium"
KIOSK_BROWSER_CONFIG_TMP="/dev/shm/chromium"

START_URL="https://panel-hala.astem.pl"

# Check this instructions
# Clean up previously running apps, gracefully at first then harshly
killall -TERM $KIOSK_BROWSER_COMMAND 2>/dev/null;
# killall -TERM matchbox-window-manager 2>/dev/null;
sleep 2;
killall -9 $KIOSK_BROWSER_COMMAND 2>/dev/null;
# killall -9 matchbox-window-manager 2>/dev/null;

# Turn off blank screen after 
xset s noblank
xset s off
# Turn off power managment of monitor
xset -dpms

# Turn off mouse courser after 0.5 se
unclutter -idle 0.5 -root &

# Run simple window manager without title bar
# matchbox-window-manager -use_titlebar no &

$KIOSK_BROWSER_COMMAND \
                --user-data-dir=$KIOSK_BROWSER_CONFIG_TMP \
                --disk-cache-dir=/dev/null \
                --remote-debugging-port=9222 \
                --noerrdialogs \
                --disable-infobars \
                --disable-translate \
                --disable-features=TranslateUI \
                --disable-save-password-bubble \
                --disable-ios-password-suggestions \
                --no-default-browser-check \
                --no-first-run \
                --fast \
                --fast-start \
                --disable-pinch \
                --kiosk $START_URL \

unclutter -reset