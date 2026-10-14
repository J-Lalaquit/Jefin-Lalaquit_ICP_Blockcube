import pygame as pg
from pygame.sprite import Sprite
from Settings import *
from Utills import *
from os import path

vec = pg.math.Vector2

# create player class with Sprite as super Class

def collide_hit_rect(one, two):
    return one.hit_rect.colliderect(two.rect)

def collide_with_walls(sprite, group, dir):
    if dir == 'x':

        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
            if hits[0].rect.centerx < sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2 
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x
            return True
        
    if dir == 'y':

        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centery > sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
            if hits[0].rect.centery < sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2 
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y

class Player(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        self.game = game
        # this provides us wtih raster images
        self.spritesheet = SpriteSheet(path.join(self.game.img_dir, "Spritesheet(3).png"))
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image = self.spritesheet.get_image(0,0,TILESIZE, TILESIZE)
        self.image.set_colorkey(Black)

        # self.image.fill(White)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        # self.vx, self.vy = 0,0
        self.vel = vec(0,0)
        self.pos = vec(x,y) * TILESIZE
        self.hit_rect = PLAYER_HIT_RECT
        self.current_frame = 0
        self.last_update = 0
        # The states of the player
        self.jumping = False
        self.moving = False
        print("player instance created")
        self.load_images()

    #gets player inputs
    def get_keys(self):
        self.vel = vec(0,0)
        # self.vx, self.vy = 0,0
        keys = pg.key.get_pressed()

        if keys[pg.K_a]:
            self.vel.x = -PLAYER_SPEED

        if keys[pg.K_d]:
            self.vel.x = PLAYER_SPEED

        if keys[pg.K_w]:
            self.vel.y = -PLAYER_SPEED

        if keys[pg.K_s]:
            self.vel.y = PLAYER_SPEED

    def jump(self):
        pass

    def load_images(self):
        self.idle_frames = [self.spritesheet.get_image(0,0, TILESIZE,TILESIZE), self.spritesheet.get_image(32,0, TILESIZE,TILESIZE)]
    def animate(self):
        now = pg.time.get_ticks()
        if not self.jumping and not self.moving:
            if now - self.last_update > 350:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.idle_frames)
                bottom = self.rect.bottom
                self.image = self.idle_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
        elif self.moving:
            if now - self.last_update > 350:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.moving_frames)
                bottom = self.rect.bottom
                self.image = self.moving_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
            
    def update(self):
        self.get_keys()
        self.animate()
        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.all_walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.all_walls, 'y')
        self.rect.center = self.hit_rect.center

#Copied all the code from the Player class but changed some stuff
class Enemy(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_enemys
        Sprite.__init__(self, self.groups)
        self.game = game
        # this provides us wtih raster images
        self.spritesheet = SpriteSheet(path.join(self.game.img_dir, "Spritesheet(3).png"))
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image = self.spritesheet.get_image(0, 32,TILESIZE, TILESIZE)
        self.image.set_colorkey(Black)
        # self.image.fill(White)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        # self.vx, self.vy = 0,0
        #speed of the enemy
        self.speed = 100
        self.vel = vec(0,0)
        self.pos = vec(x,y) * TILESIZE
        self.hit_rect = ENEMY_HIT_RECT
        self.current_frame = 0
        self.last_update = 0
        # The states of the enemy
        self.jumping = False
        self.moving = False
        print("enemy instance created")
        self.load_images()

    def load_images(self):
        self.idle_frames = [self.spritesheet.get_image(0,32, TILESIZE,TILESIZE), self.spritesheet.get_image(32,32, TILESIZE,TILESIZE)]
    def animate(self):
        now = pg.time.get_ticks()
        if not self.jumping and not self.moving:
            if now - self.last_update > 350:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.idle_frames)
                bottom = self.rect.bottom
                self.image = self.idle_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
        elif self.moving:
            if now - self.last_update > 350:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.moving_frames)
                bottom = self.rect.bottom
                self.image = self.moving_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

    #Makes the enemy chase the player
    def follow(self, obj):
        Direction = vec(obj.rect.centerx - self.rect.centerx, obj.rect.centery - self.rect.centery)
        if Direction.length() > 0:
            Direction = Direction.normalize()
        self.vel = Direction
            
    def update(self):
        self.animate()
        self.follow(self.game.player)
        self.rect.center = self.pos
        self.pos += self.vel * self.speed * self.game.dt
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.all_walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.all_walls, 'y')
        self.rect.center = self.hit_rect.center

class Wall(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_walls
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(Green) #changes color of wall :)
        self.rect = self.image.get_rect()
        self.vel = vec(0,0)
        self.pos = vec(x,y) * TILESIZE
        self.rect.center = self.pos
        print("wall instance created")

class Coin(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_coins
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        pg.draw.circle(self.image, (Yellow), (TILESIZE/2, TILESIZE/2), TILESIZE/2)
        self.image.set_colorkey(Black)
        
        #self.image.fill(Yellow) #changes color of coin :)
        
        #setup the rect/pos
        self.rect = self.image.get_rect()
        self.vel = vec(0,0)
        self.pos = vec(x,y) * TILESIZE
        self.rect.center = self.pos
        print("Coin instance created")