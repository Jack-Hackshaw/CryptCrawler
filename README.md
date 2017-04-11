# CryptCrawler

CryptCrawler is a simple RPG made with Python 3. It uses an algorithm to generate a level before handing control to the player. The game currently uses ASCII characters for graphics but wil hopefully be updated with textures soon.

# Licence
Read LICENCE in the doc directory.

# Installation
## Dependancies
CryptCrawler's only dependancies are pygame and python 3 however, pygame has it's own dependancies which will be covered below.

### Instaling pygame
#### Linux
```
sudo apt-get install mercurial python3-dev python3-numpy libsdl-image1.2-dev libsdl-mixer1.2-dev libsdl-ttf2.0-dev libsmpeg-dev libsdl1.2-dev libportmidi-dev libswscale-dev libavformat-dev libavcodec-dev libfreetype6-dev
sudo apt-get install mercurial
hg clone https://bitbucket.org/pygame/pygame
cd pygame
python3 setup.py build
sudo python3 setup.py install
```
#### OS X
```
brew install mercurial
brew install sdl sdl_image sdl_mixer sdl_ttf portmidi
brew tap homebrew/headonly
brew install smpeg
sudo pip3 install hg+http://bitbucket.org/pygame/pygame
```
#### Windows
+ Download the wheel file [here][].
```
pip install wheel 
pip install pygame‑[version]‑[python version]‑none‑win_amd64.whl
```
[here]: http://www.lfd.uci.edu/~gohlke/pythonlibs/#pygame "here"

## Installing and Running CryptCrawler
```
git clone git://github.com/Jack-Hackshaw/CryptCrawler.git
cd CryptCrawler
python3 crypt_crawler.py
```
## How to play
When you start CryptCrawler the user interface will be displayed in command line and and a window entitled "pygame window" will open. In order to play you must divert your window manager's focus to it (either by clicking it or using some key combo like ALT+TAB). Now that you are focused on the pygame window you will be able to control your character as per the control scheme below.

### Controls
| Button | Effect                  | Note |
|--------|-------------------------|:----:|
|w       |Move Up                  |      |
|a       |Move Left                |      |
|s       |Move Down                |      |
|d       |Move Right               |      |
|Space   |Attack                   |      |
|e       |Enter Special Input Mode |(1)   |
|esc     |Exit the Game            |      |
|enter   |Execute Special Command  |(1)   |

### Notes
(1): Special input mode allows you to move diagonally by entering a key combination. It requires that you press e, change your focus to the terminal, type in the combination and press enter.
#### Combinations
| Combination | Effect                               |
|-------------|--------------------------------------|
|w+a or a+w   |Move Diagonally Up and to the Left    |
|s+a or a+s   |Move Diagonally Down and to the Left  |
|s+d or d+s   |Move Diagonally Down and to the Right |
|w+d or d+w   |Move Diagonally Up and to the Right   |
