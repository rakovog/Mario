import pygame, random
from pygame import *
from playir import *
from blocks import *
from monsters import *

fps = 60
timer = pygame.time.Clock()
sc_w = 800
sc_h = 640
display = (sc_w, sc_h)
bg_color = "#004400"
g_level = 1


class Camera(object):
    def __init__(self, camera_funcs, width, hight):
        self.camera_funcs = camera_funcs
        self.state = Rect(0, 0, width, hight)

    def apply(self, turget):
        return turget.rect.move(self.state.topleft)

    def update(self, turget):
        self.state = self.camera_funcs(self.state, turget.rect)


def camera_config(camera, turget_rect):
    l, t, _, _ = turget_rect
    _, _, w, h = camera
    l, t = -l + sc_w / 2, -t + sc_h / 2
    l = min(0, l)
    l = max(-(camera.width - sc_w), l)
    t = max(-(camera.height - sc_h), t)
    t = min(0, t)
    return Rect(l, t, w, h)


def set_monster(x, y):
    global mm, platfoms
    left = random.randint(100, 300)
    up = random.randint(5, 20)
    mm = Monster(x, y, 2, 3, left, up)
    entities.add(mm)
    platfoms.append(mm)
    monsters.add(mm)


def set_teleport(x, y, x2, y2):
    global tp, platfoms
    tp = BlockTeleport(x, y, x2, y2)
    entities.add(tp)
    platfoms.append(tp)
    anym_entities.add(tp)


def load_level(lvl):
    global playerX, playerY, level
    levelFile = open(f"levels/{lvl}.txt")
    line = " "
    command = []
    while line[0] != "/":  # пока не нашли символ завершения файла
        line = levelFile.readline()  # считываем построчно
        if line[0] == "[":  # если нашли символ начала уровня
            while line[0] != "]":  # то, пока не нашли символ конца уровня
                line = levelFile.readline()  # считываем построчно уровень
                if line[0] != "]":  # и если нет символа конца уровня
                    endLine = line.find("|")  # то ищем символ конца строки
                    level.append(line[0: endLine])  # и добавляем в уровень строку от начала до символа "|"
        if line[0] != "":  # если строка не пустая
            commands = line.split()  # разбиваем ее на отдельные команды
            if len(commands) > 1:  # если количество команд > 1, то ищем эти команды
                if commands[0] == "player":  # если первая команда - playerd
                    playerX = int(commands[1])  # то записываем координаты героя
                    playerY = int(commands[2])


def main():
    global entities, platfoms, anym_entities, monsters, level, g_level
    pygame.init()
    level = []
    load_level(g_level)
    screen = pygame.display.set_mode(display)
    pygame.display.set_caption("Сантехник")
    bg = Surface(display)
    bg.fill(Color(bg_color))
    hero = Player(playerX, playerY)
    left = right = up = runing = False
    entities = pygame.sprite.Group()
    anym_entities = pygame.sprite.Group()
    monsters = pygame.sprite.Group()
    platfoms = []
    entities.add(hero)
    x = y = 0
    for row in level:
        for col in row:
            if col == "-":
                pf = Platform(x, y)
                entities.add(pf)
                platfoms.append(pf)
            if col == "*":
                bd = Spick(x, y)
                entities.add(bd)
                platfoms.append(bd)
            if col == "T":
                gox = x
                goy = y
            if col == "t":
                set_teleport(x, y, gox, goy)
            if col == "m":
                set_monster(x, y)
            if col == "p":
                pr = Princess(x, y)
                entities.add(pr)
                platfoms.append(pr)
                anym_entities.add((pr))
            x += platfom_w
        y += platform_h
        x = 0
    total_w = len(level[0]) * platfom_w
    total_h = len(level) * platform_h
    camera = Camera(camera_config, total_w, total_h)
    while True:  # основной циклa
        for e in pygame.event.get():
            if e.type == QUIT:
                exit()
            if e.type == KEYDOWN and e.key == K_a:
                left = True
            if e.type == KEYDOWN and e.key == K_d:
                right = True
            if e.type == KEYUP and e.key == K_a:
                left = False
            if e.type == KEYUP and e.key == K_d:
                right = False
            if e.type == KEYDOWN and e.key == K_SPACE:
                up = True
            if e.type == KEYUP and e.key == K_SPACE:
                up = False
            if e.type == KEYDOWN and e.key == K_LSHIFT:
                runing = True
            if e.type == KEYUP and e.key == K_LSHIFT:
                runing = False
        screen.blit(bg, (0, 0))
        hero.update(left, right, up, runing, platfoms)
        anym_entities.update()
        monsters.update(platfoms)
        camera.update(hero)
        for e in entities:
            screen.blit(e.image, camera.apply(e))
        if hero.win:
            if g_level < 2:  # количество уровней
                g_level += 1
            else:
                hero.win = False
                main()

        pygame.display.update()
        timer.tick(fps)


if __name__ == '__main__':
    main()
