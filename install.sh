#!/bin/sh

sudo apt-get install -y build-essential checkinstall 
sudo apt install portaudio19-dev
sudo docker run -v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=unix$DISPLAY --privileged cog_sw
#pyuic5 -x pasat.ui -o pasat_ui.py