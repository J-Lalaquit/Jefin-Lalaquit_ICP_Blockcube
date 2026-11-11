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
 
Goals: Get fish to make money
Rules: You can't go in the ocean or you will drown 
Feedback: Keybinds to move
Freedom:You can go fishing

"""

#importing pygame as pg to give it the nickname "pg"
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
        #whether fullscreen is enabled or not. in this case, it's on (True) but if it's off it would be False.
        self.fullscreen = True
        #Changes to fullscreen mode
        self.screen = pg.display.set_mode((WIDTH, HEIGHT), pg.FULLSCREEN)
        print('game class initialized')
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.playing = True
        self.score = 0
        self.highscore = 0
        #Next Level set to None so that it doesn't load a level when the game starts (I can switch it to level2.txt if I want to test the next level feature)
        self.next_level = None

    def load_data(self):
        self.game_dir = path.dirname(__file__)
        self.game_save_dir = path.join(self.game_dir, "highscore.txt")

        self.img_dir = path.join(self.game_dir, 'images')

        #Sound Handling
        self.snd_dir = path.join(self.game_dir, 'sounds_coolski')
        self.pickupcoin_snd = pg.mixer.Sound(path.join(self.snd_dir, "Coin_Collection.wav"))

    #Checks if the file exists and if it doesn't it makes one
        try:
            with open(self.game_save_dir, "x", encoding="utf-8") as file:
                file.write("Hello 67!")
            print("file created succesfully")
        except FileExistsError:
            print("File already exists. no action taken")

        with open(self.game_save_dir, 'r') as f:
            try:
                self.highscore = int(f.read())
                print("Highscore Created")
            except:
                self.highscore = 0
                # print("Dunno but this is commented out")

    def load_level(self, level_name):
        #Checks if the player exist and if it doesnt the coins are set to 0
        if getattr(self, "player", None) != None:
            player_coins = self.player.coins
        else:
            player_coins = 0
        #Pretty straightforward. It sets the current level to the level name and loads the map from the file. (For example, if the level name is level1.txt then it will load the map from level1.txt)
        self.current_level = level_name
        self.map = Map(path.join(self.game_dir, level_name))
        self.all_sprites = pg.sprite.Group()
        self.all_walls = pg.sprite.Group()
        self.all_enemys = pg.sprite.Group()
        self.all_coins = pg.sprite.Group()
        self.all_partickles = pg.sprite.Group()
        self.all_tiles = pg.sprite.Group()

        if level_name == 'level1.txt':
            self.wall = Wall(self,6,7)

            #Block of coins
            self.coin = Coin(self,3,2)
            self.coin = Coin(self,3,1)
            self.coin = Coin(self,2,1)
            self.coin = Coin(self,2,2)

        print(self.map.data)

        # Create objects listed in the level map.
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row)
                elif tile == 'C':
                    Coin(self,col,row)
                elif tile == 'M':
                    Enemy(self,col,row)
                elif tile == 'I':
                    f = FloorTile(self,col,row, Black)
                    f.variant = 'ice'
                elif tile == 'T':
                    f = FloorTile(self,col,row, Yellow)
                    f.variant = 'teleporter'
                elif tile == 'P':
                    self.player = Player(self, col, row)
                    self.player.coins = player_coins

    def new(self):
        self.load_data()
        self.player = None
        self.load_level('level1.txt')

        # pg.mixer.music.load(path.join(self.snd_dir, "Nothing yet :/"))

    def run(self):
        while self.running:
            self.dt = self.clock.tick(FPS) / 1000
            self.events() # this gets player input
            self.update() # this updates the game
            self.draw() # this draws sprites
    
    def events(self):
        #found this code from this website called zenva: https://gamedevacademy.org/pygame-fullscreen-tutorial-complete-guide/
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.fullscreen = False
                elif event.key == pg.K_F11:
                    self.fullscreen = not self.fullscreen

                if event.key in (pg.K_ESCAPE, pg.K_F11):
                    #Did some research for this one. Flags helps changes the display setup. If fullscreen is true then it will be fullscreen if not then it will be normal
                    flags = pg.FULLSCREEN if self.fullscreen == True else 0
                    self.screen = pg.display.set_mode((WIDTH, HEIGHT), flags)

            if event.type == pg.QUIT:

                #Checks if score/coins is greater than previous highscore
                if self.score > self.highscore:
                    with open(path.join(self.game_dir, self.game_save_dir), 'w') as f:
                        f.write(str(self.score))
                    
                if self.playing:
                    self.playing = False
                self.running = False
    # this block of code handles changes based on input

    def update(self):
        self.all_sprites.update()
        if self.next_level is not None:
            next_level = self.next_level
            self.next_level = None
            self.load_level(next_level)
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
        self.all_tiles.draw(self.screen)
        self.all_sprites.draw(self.screen)
        self.draw_text("Frames Per Second (FPS): " + str(floor(1/self.dt) ), 24, White, WIDTH/2, HEIGHT/4)
        self.draw_text(f"Coins: {self.player.coins}", 24, Yellow, WIDTH/2, WIDTH/10)
        self.draw_text(f"Highscore: {self.highscore}", 24, Red, WIDTH/6, WIDTH/32)

        pg.display.flip()

if __name__ == "__main__":
    g = Game()

while g.running:
    g.new()
    g.run()

pg.quit()