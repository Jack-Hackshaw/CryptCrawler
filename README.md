# CryptCrawler

CryptCrawler is a simple RPG made with Python 3. It uses an algorithm to generate a level before handing control to the player. The game currently uses ASCII characters for graphics but wil hopefully be updated with textures soon.

# Running CryptCrawler

CryptCrawler's only dependancy is pygame.

### Instaling pygame

#### Linux
##### Dependancies
`sudo apt-get install mercurial python3-dev python3-numpy \
 libsdl-image1.2-dev libsdl-mixer1.2-dev libsdl-ttf2.0-dev libsmpeg-dev \
 libsdl1.2-dev  libportmidi-dev libswscale-dev libavformat-dev libavcodec-dev libfreetype6-dev`
##### Mercurial
`sudo apt-get install mercurial
 hg clone https://bitbucket.org/pygame/pygame`
##### Build and Install
`cd pygame
 python3 setup.py build
 sudo python3 setup.py install`

#### OS X


#### Windows
+ Download the wheel file [here][].
`pip install wheel 
 pip install pygame‑[version]‑[python version]‑none‑win_amd64.whl`

[here]: http://www.lfd.uci.edu/~gohlke/pythonlibs/#pygame "here"
