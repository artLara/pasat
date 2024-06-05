#!/bin/sh

conda create --name pasat-pyqt5 -y
conda activate pasat-pyqt5
conda install python=3.8
conda install qt -y
conda install pyqt -y
pip install pygame
pip install opencv-python-headless
sudo apt-get install -y build-essential checkinstall 
sudo apt install portaudio19-dev
pip3 install pyaudio
conda install -c anaconda pyaudio
pip3 install keyboard
pip3 install pynput
#pyuic5 -x pasat.ui -o pasat_ui.py
