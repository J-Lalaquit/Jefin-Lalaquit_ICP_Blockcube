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
Rules: You can't go in the ocean or you will drown 
Feedback: Keybinds to Move and Spacebar to Jump
Freedom:You can go fishing

"""

import pygame as pg
from Settings import *
from Sprites import *
from Utills import *

from os import path

#this is the Game class. it's pretty much runs the whole game ( which is why it's called game :) )
class Game:

    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        print('game class initialized')
        self.clock = pg.time.Clock()
        self.running = True
        self.playing = True

    def load_data(self, map):
        self.game_dir = path.dirname(__file__)
        self.img_dir = path.join(self.game_dir, 'images')
        self.map = Map(path.join(self.game_dir, map))

    def new(self):
        self.load_data('level1.txt')
        self.all_sprites = pg.sprite.Group()
        self.all_walls = pg.sprite.Group()
        self.all_enemys = pg.sprite.Group()
        
        self.wall = Wall(self,6,7)
        print(self.map.data)

        # Wall Creator
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row)
                if tile == 'M':
                    Enemy(self,col,row)

        # Player Creator
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == 'P':
                    self.player = Player(self, col, row)

    def run(self):
        while self.running:
            self.dt = self.clock.tick(FPS) / 1000
            self.events() # this gets player input
            self.update() # this updates the game
            self.draw() # this draws sprites
    
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
    # this block of code handles changes based on input

    def update(self):
        self.all_sprites.update()
    # makes text on the screen anywhere using x and y
    def draw_text(self, text, size, color, x, y):
        #changes fontof the text
        font_name = pg.font.match_font('comicsans')
        # instantiate the Font class
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        self.screen.blit(text_surface, text_rect)

    def draw(self):
        self.screen.fill(Blue) #changes color of bg
        self.all_sprites.draw(self.screen)
        self.draw_text("Frames Per Second (FPS): " + str(floor(1/self.dt) ), 24, White, WIDTH/2, HEIGHT/4)
        pg.display.flip()

if __name__ == "__main__":
    g = Game()

while g.running:
    g.new()
    g.run()

pg.quit()