from pygame import *
import pygame
import  time
import blocks
import monsters

jupm_over = 10
graviti = 0.45
move_speed = 7
move_extre_speed = 2.5
jupm_extre_over = 1.5
width = 22
hight = 32
color = "#888888"
anym_dele = 100
anym_right = []
anym_left = []
for i in range(1, 6):
    anym_right.append(f"mario/r{i}.png")
    anym_left.append(f"mario/l{i}.png")
anym_left_jump = "mario/jl.png"
anym_right_jump = "mario/jr.png"
anym_jump = "mario/j.png"
anym_stoy = "mario/0.png"


class Player(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.xvel = 0
        self.yvel = 0
        self.ongroand = False
        self.win=False
        self.start_x = x
        self.start_y = y
        self.image = Surface((width, hight))
        self.image.fill(Color(color))
        self.rect = Rect(x, y, width, hight)
        self.image.set_colorkey(Color(color))
        self.right_anim = []
        self.left_anim = []
        for image in anym_right:
            self.right_anim.append(pygame.image.load(image).convert())
        for image in anym_left:
            self.left_anim.append(pygame.image.load(image).convert())
        self.right_jump = pygame.image.load(anym_right_jump).convert()
        self.left_jump = pygame.image.load(anym_left_jump).convert()
        self.jump = pygame.image.load(anym_jump).convert()
        self.stoy = pygame.image.load(anym_stoy).convert()
        self.index = 0

    def update(self, left, right, up, runing, platforms):
        if up:
            if self.ongroand:
                self.yvel = -jupm_over
                if runing:
                    self.yvel-=jupm_extre_over
                self.image = self.jump
        if left:
            self.xvel = -move_speed
            if runing:
                self.xvel-=move_extre_speed
            if up:
                self.image = self.left_jump
            else:
                self.index += 1
                if self.index >= len(self.left_anim):
                    self.index = 0
                self.image = self.left_anim[self.index]
        if right:
            self.xvel = move_speed
            if runing:
                self.xvel+=move_extre_speed
            if up:
                self.image = self.right_jump
            else:
                self.index += 1
                if self.index >= len(self.right_anim):
                    self.index = 0
                self.image = self.right_anim[self.index]
        if not (left or right):
            self.xvel = 0
            if not up:
                self.image = self.stoy
        self.rect.x += self.xvel
        self.callide(self.xvel, 0, platforms)
        if not self.ongroand:
            self.yvel += graviti
        self.ongroand = False
        self.rect.y += self.yvel
        self.callide(0, self.yvel, platforms)

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def callide(self, xvel, yvel, platfoms):
        for p in platfoms:
            if sprite.collide_rect(self, p):
                if xvel > 0:
                    self.rect.right = p.rect.left
                if xvel < 0:
                    self.rect.left = p.rect.right
                if yvel > 0:
                    self.rect.bottom = p.rect.top
                    self.ongroand = True
                    self.yvel = 0
                if yvel < 0:
                    self.rect.top = p.rect.bottom
                    self.yvel = 0
                if isinstance(p,blocks.Spick) or isinstance(p,monsters.Monster):
                    self.die()
                elif isinstance(p, blocks.BlockTeleport):
                    self.teleporting(p.gox,p.goy)
                elif isinstance(p, blocks.Princess):
                    self.win=True
    def die(self):
        time.sleep(0.5)
        self.teleporting(self.start_x,self.start_y)
    def teleporting(self,gox,goy):
        self.rect.x=gox
        self.rect.y=goy