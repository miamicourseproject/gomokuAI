# gomokuAI
___
## Introduction
gomokuAI is a tic-tac-toe game with a built-in AI bot capable of evaluating and making smart moves based on current situation. 
The game is built on the idea of not just being a smart bot, but also fully functional game app with a friendly user interface with many features.
In this project, minimax algorithm with alpha beta prunning is implemented for AI player to make the next move. 
Minimax is one of the most popular algorithm, though not the best, in AI involved games like chess, checkers, tic-tac-toe
___
## Overview
### Here are some screenshots of the game:

### Start Screen 
![alt text](https://github.com/miamicourseproject/gomokuAI/blob/master/Images/Welcome%20Screen.PNG)

### SubStart Screen 
![alt text](https://github.com/miamicourseproject/gomokuAI/blob/master/Images/Substart%20Screen.PNG)

### Game Screen
![alt text](https://github.com/miamicourseproject/gomokuAI/blob/master/Images/Game%20Screen.PNG)
___
## How to play
### Option 1: Cloning from repo
You may want to try this option if you would like to have a deeper look into our code (and maybe play with it a bit). In order to do this, I would suggest you install Python and the Pygame libraries for the program to run:
* Python Installation:
<br />Install the lastest version of Python from this link: [Python Download](https://www.python.org/downloads/)

* Pip install/update:
<br />* Installation - Follow this link for further instruction: [Pip Install](https://pip.pypa.io/en/stable/reference/pip_install/)
<br />* Update - Your pip to the latest version: 
```
pip install --upgrade pip
```
For Windows:
```
python -m pip install --upgrade pip
```

* Pygame Installation:
```
pip install pygame
```
After cloning the repo, run gomoku.py file to try the game.

### Option 2: Directly download the executed version from DropBox
You should try this option if you just want to experience the game. 
<br />Here is the link to download: [Link](https://www.dropbox.com/s/89kuy8fn8mvy8za/GomokuAI.rar?dl=0).
___
## Credits
* Our pattern evaluation function is based on this research report on gomoku: https://linyanghe.github.io/projects/resources/Gomuku.pdf.
We would like to thank to authors of this paper for such useful information, which enable us to give our bot the ability to plan wisely ahead of time.
___
## License
gomokuAI is [MIT Licensed](https://github.com/miamicourseproject/gomokuAI/blob/master/LICENSE).
