FROM python:3.8

WORKDIR /code
EXPOSE 80
COPY . .

RUN apt update \
&& yes | apt-get install mesa-common-dev \
&& yes | apt-get install libglu1-mesa-dev \
&& yes | apt-get install qtbase5-dev qtchooser qt5-qmake qtbase5-dev-tools \
&& yes | apt-get install -y build-essential checkinstall \
&& yes | apt install portaudio19-dev \
&& yes | pip install --no-cache-dir -r requirements_pip.txt


CMD ["python3", "src/main.py"]