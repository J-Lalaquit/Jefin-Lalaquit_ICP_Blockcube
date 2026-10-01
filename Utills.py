import pygame as pg
from Settings import * 
from math import floor

class Map:
    def __init__(self, filename):
        self.data = []

        with open(filename, 'rt') as f:
            for line in f:
                self.data.append(line.strip())

        self.tilewidth = len(self.data[0])
        print(self.data)
        self.tileheight = len(self.data)
        self.width = self.tilewidth * Tilesize
        self.height = self.tileheight * Tilesize

class SpriteSheet:
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0,0), (x, y, height, width))
        #when applying pygame translation transformation & scale we need to pass the newley transformed object data
        new_image = pg.transform.scale(image, (width, height))
        image = new_image
        return image

        
