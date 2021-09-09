from pygame import *
import pygame

monster_w = monster_h = 32
monster_color = "#ff6262"
anym_left = []
anym_right = []
for i in range(1, 14):
    anym_left.append(f"monsters/booL{i}.png")
    anym_right.append(f"monsters/booR{i}.png")


class Monster(sprite.Sprite):
    def __init__(self, x, y, left, up, max_left, max_up):
        sprite.Sprite.__init__(self)
        self.image = Surface((monster_w, monster_h))
        self.rect = Rect(x, y, monster_w, monster_h)
        self.monster_left = []
        self.monster_right = []
        for image in anym_left:
            self.monster_left.append(pygame.image.load(image))
        for image in anym_right:
            self.monster_right.append(pygame.image.load(image))
        self.start_x = x
        self.start_y = y
        self.x_vel = left
        self.y_vel = up
        self.left = max_left
        self.up = max_up
        self.frame = 0
        self.der = "r"

    def update(self, platfoms):
        self.frame += 1
        if self.frame >= 13:
            self.frame = 0
        if self.der == "r":
            self.image = self.monster_right[self.frame]
        else:
            self.image = self.monster_left[self.frame]
        self.rect.y += self.y_vel
        self.rect.x += self.x_vel
        self.callide(platfoms)
        if (abs(self.start_x - self.rect.x) > self.left):
            self.x_vel = -self.x_vel
            if self.der == "r":
                self.der = "l"
            else:
                self.der = "r"
        if (abs(self.start_y - self.rect.y) > self.up):
            self.y_vel = -self.y_vel
    def callide(self,platfoms):
        for p in platfoms:
            if sprite.collide_rect(self,p) and self!=p:
                self.x_vel = -self.x_vel
                self.y_vel = -self.y_vel
                if self.der == "r":
                    self.der = "l"
                else:
                    self.der = "r"
