# Genius Snake
This project implements classic game Snake and various algorithms trying to win it.

## How to start?
This program is in Python and uses Conda to manage environment. So, make sure Conda and Python3 are on your computer. Go to the cloned folder. Then, create the environment:
**conda env create -f environment.yml**
Activate it:
**conda activate geniusSnake**
And run it:
**python3 ./**

## What does the project contain?
**Basic game** - Key-controlled snake with classic rules, so you can compare your skills with AI
**Genetic programming** - In this mode, breeding of a driver function for snake starts. You can watch snakes becoming better and better through evolution
**A\* algorithm** - In each step, snake uses A* algorithm to find the apple and to avoid obstacles
**Hamiltonian cycle** - Snake avoids death by running in the cycle covering the whole game field (if possible)

**Settings** - implemented as a file with many constants affecting behavior of the whole app, warning: there are very limited controls for meaningful values in the settings, so use them wisely!