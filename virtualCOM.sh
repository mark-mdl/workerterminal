#!/bin/bash

# Create virtual com and link them to ttyUSB0 and ttyUSB1.
# Data which are writed  to ttyUSB1 (ex. echo "lorem" > ttyUSB1) are read by ttyUSB0 (cat < ttyUSB0)
# Can by used to emulate communication with RFID reader 
# https://stackoverflow.com/questions/52187/virtual-serial-port-for-linux
#
# Check parameters of virtual com
# stty -F ./ttyUSB[0-1]
# https://stackoverflow.com/questions/34831131/pyserial-does-not-play-well-with-virtual-port
socat -dd pty,raw,echo=0,b19200,link=ttyUSB0 pty,raw,echo=0,b19200,link=ttyUSB1