#!/bin/sh

conda create --name pasat-pyqt5 -y
conda activate pasat-pyqt5
conda install qt -y
conda install pyqt -y
pip install pygame
pip install opencv-python-headless
sudo apt-get install -y build-essential checkinstall 
pip install pyaudio
pip3 install keyboard
#pyuic5 -x pasat.ui -o pasat_ui.py