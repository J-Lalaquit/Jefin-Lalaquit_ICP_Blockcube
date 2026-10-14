#Pygame

import pygame as pg

#Heights, Widths, & More !

WIDTH = 1024
HEIGHT = 768
TITLE = "Square Gangularis"
TILESIZE = 32
FPS = 30

#Colors

Bg_Color = (255, 50, 50)
Yellow = (255, 255, 0)
Black = (0, 0, 0)
Blue = (50, 50, 255)
White = (255,255,255)
Green = (50, 255, 50)

#Player Settings

PLAYER_SPEED = 300
PLAYER_HIT_RECT = pg.Rect(0,0, TILESIZE-5, TILESIZE-5)

#Enemy Settings

ENEMY_SPEED = 300
ENEMY_HIT_RECT = pg.Rect(0,0, TILESIZE-5, TILESIZE-5)