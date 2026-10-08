#This file was created by: Jefin Lalaquit
#Content inspired by: Chris Bradfield
#I do solemnly swear to create concise and informative comments

#funny comment #grrr mondays
 
"""
The game engine consists of four basic components:
 
Input: keys, buttons, voice, mouse, touch
Process: input processes direction of control
Output: draw pixels, sound, haptic
Store:
 
Goals:Get fish to make mony
Rules: Dunno 
Feedback: 
Freedom:You can go fishing :/

"""

import pygame as pg
from Settings import *
from Sprites import *
from Utills import *

from os import path

class Game:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        print('game class initialized')
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.playing = True
       

    def load_data(self, map):
        self.game_dir = path.dirname(__file__)
        self.img_dir = path.join(self.game_dir, 'images')
        self.map = Map(path.join(self.game_dir, map))
 
    def new(self):

        self.load_data("level1.txt")

        self.all_sprites = pg.sprite.Group()
        self.all_walls = pg.sprite.Group()
        # self.all_enemys = pg.sprite.Group()

        print(self.map.data)

        # Wall Creator
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    #Creates Wall
                    Wall(self, col, row)

        #Player Creator
        for row, tiles in enumerate(self.map.data):
            for col, tile, in enumerate(tiles):
                if tile == 'P':
                    #Makes Player
                    Player(self, col, row)
        
    def run(self):
        self.playing = True
        while self.running:
            self.dt = self.clock.tick(FPS) /1000
            self.events() #this gets player input
            self.update() #this updates
            self.draw() #this draws sprites
 
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
    #this line of code handles changes based on input
 
    def update(self):
        self.all_sprites.update()

#Draw_text basically helps draws text on the screen anywhere
    def draw_text(self, text, size, color, x, y):
        font_name = pg.font.match_font("arial")
        #instantiates the Font class
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        self.screen.blit(text_surface, text_rect)

    def draw(self):
        self.screen.fill(Blue) #Changes color of bg/bd
        self.all_sprites.draw(self.screen)
        self.draw_text("Frames Per Second (FPS): " + str(floor(1/self.dt)), 24, White, WIDTH/2, HEIGHT/4)
        pg.display.flip()
 
if __name__ == "__main__":
    g = Game()
 
while g.running:
    g.new()
    g.run()

pg.quit()