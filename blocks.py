# комментарий
from pygame import *
import pygame
platfom_w = platform_h = 32
platfom_color = "#ff6262"
teleport_img = ["blocks/portal1.png", "blocks/portal2.png"]
princess_img=["blocks/princess_l.png","blocks/princess_r.png"]


class Platform(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = image.load("blocks/platform.png")
        self.rect = Rect(x, y, platfom_w, platform_h)


class Spick(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.image = image.load("blocks/dieBlock.png")


class BlockTeleport(Platform):
    def __init__(self, x, y, gox, goy):
        Platform.__init__(self, x, y)
        self.goy = goy
        self.gox = gox
        self.block_teleport=[]
        for image in teleport_img:
            self.block_teleport.append(pygame.image.load(image))
        self.index=0
        self.frame=0
    def update(self):
        self.index+=1
        if self.index>10:
            self.index=0
        if self.index<=5:
            self.frame=0
        else:
            self.frame=1
        self.image=self.block_teleport[self.frame]
class Princess(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.princess=[]
        for image in princess_img:
            self.princess.append(pygame.image.load(image))
        self.index=0
        self.frame=0
    def update(self):
        self.index+=1
        if self.index>200:
            self.index=0
        if self.index<=100:
            self.frame=0
        else:
            self.frame=1
        self.image=self.princess[self.frame]
