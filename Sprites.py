import pygame as pg
from pygame.sprite import Sprite
from Settings import *
from Utills import *

from os import path

vec = pg.math.Vector2
 
#create player class with sprite as Super Class
 
def collide_hit_rect(one, two):
    return one.hit_rect.colliderect(two.rect)

def collide_width_walls(sprite, group, dir):

    if dir == 'x':
         hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
         if hits:
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
            if hits[0].rect.centerx < sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x

    if dir == 'y':
        pass

class Player(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        self.game = game
        self.spritesheet = SpriteSheet(path.join(self.game.img_dir, "SpriteSheet.png"))
        self.image = pg.Surface((Tilesize, Tilesize))
        self.image = self.spritesheet.get_image(0, 0, Tilesize, Tilesize)
        #self.image.fill(White)
        self.rect = self.image.get_rect()
        self.hit_rect = PLAYER_HIT_RECT
        self.rect.x = x
        self.rect.y = y
        # self.vx, self.vy = 0, 0
        self.vel = vec(0,0) 
        self.pos = vec(x * Tilesize, y * Tilesize)
        self.current_frame = 0
        self.last_update = 0
        self.jumping = False
        print("player instance created")
 
 
#gets player input
    def get_keys(self):
        self.vel = vec(0,0)
        # self.vx, self.vy = 0,0
        keys = pg.key.get_pressed()
 
        if keys[pg.K_a]:
            self.vel.x = -player_speed
 
        if keys[pg.K_d]:
            self.vel.x = player_speed
 
        if keys[pg.K_w]:
            self.vel.y = -player_speed
 
        if keys[pg.K_s]:
            self.vel.y = player_speed

        if self.vel.x != 0 and self.vel.y != 0:
            self.vel *= 0.7071
       
 
    def jump(self):
        pass

    def load_image(self):
        self.idle_frames = [self.spritesheet.get_image(0,0, Tilesize,Tilesize), self.spritesheet.get_image(32,0, Tilesize,Tilesize)]
    def animate(self):
        now = pg.time.get_ticks()
        if not self.jumping and not self.moving:
            if now - self.last_update > 350:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
                bottom = self.rect.bottom
                self.image = self.standing_frames[self.current_frame]
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
        collide_width_walls(self, self.game.all_walls, 'x')
        self.rect.centery = self.pos.y
        collide_width_walls(self, self.game.all_walls, 'y')
        self.rect.center = self.hit_rect.center
 
class Wall(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_walls
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((Tilesize, Tilesize))
        self.image.fill(Green) #Changes color of Wall
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vx, self.vy = 0, 0
        self.x = x * Tilesize
        self.y = y * Tilesize
        self.rect.x = self.x
        self.rect.y = self.y
        print("wall instance created")