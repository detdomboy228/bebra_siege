import sys

import pygame
import random
from os import path


img_dir = path.join(path.dirname(__file__), 'myg')
snd_dir = path.join(path.dirname(__file__), 'snd')

WIDTH = 800
HEIGHT = 480
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

POWERUP_TIME = 5000


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.speedx = 13
        self.image = bullet_img
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.top = y

    def update(self):
        self.rect.x += self.speedx

        if self.rect.left > WIDTH:
            self.kill()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.speedy = 0
        self.image = player_img
        self.image.set_colorkey(GREEN)
        self.rect = self.image.get_rect()
        self.rect.centery = HEIGHT / 2
        self.rect.left = 140
        self.shoot_delay = 300
        self.last_shot = pygame.time.get_ticks()
        self.ult1 = False
        self.ult = 0
        self.power_time = pygame.time.get_ticks()
        self.l_anim = pygame.time.get_ticks()

    def update(self):
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_UP]:
            self.speedy = -5
        if keystate[pygame.K_DOWN]:
            self.speedy = 5
        self.rect.y += self.speedy
        if keystate[pygame.K_SPACE]:
            self.shoot()

        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

        if self.ult1:
            self.shoot_delay = 100
        else:
            self.shoot_delay = 300

        if self.ult1 and pygame.time.get_ticks() - self.power_time > POWERUP_TIME:
            self.ult1 = False
            self.ult = 0
            self.power_time = pygame.time.get_ticks()

        if self.ult1 and pygame.time.get_ticks() - self.l_anim > 100:
            ul = UltAnim(background_rect.center)
            sprites.add(ul)
            self.l_anim = pygame.time.get_ticks()

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = Bullet(self.rect.right, self.rect.centery)
            expl = BullExpl(self.rect.midright)
            vshoot.play()
            sprites.add(expl)
            sprites.add(bullet)
            bullets.add(bullet)


class UltAnim(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.image = sp[0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(sp):
                self.kill()
            else:
                center = self.rect.center
                self.image = sp[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


class Wall(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.hp = 100
        self.hp1 = 50
        self.image = wall_img
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.left = 90

    def update(self):
        if self.hp <= 0 and self.image == wall_img:
            self.image = walldestr_img
            self.image.set_colorkey(WHITE)


class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = mob_img
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.y = random.randrange(100, 300)
        self.rect.x = random.randrange(800, 840)
        self.speedx = -(random.randrange(3, 5))

    def update(self):
        self.rect.x += self.speedx
        if self.rect.left < 0:
            self.rect.y = random.randrange(100, 300)
            self.rect.x = random.randrange(810, 840)
            self.speedx = -(random.randrange(3, 5))


class BullExpl(pygame.sprite.Sprite):
    def __init__(self, midright):
        pygame.sprite.Sprite.__init__(self)
        self.image = exp_anim[0]
        self.rect = self.image.get_rect()
        self.rect.midright = midright
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 20

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(exp_anim):
                self.kill()
            else:
                midright = self.rect.midright
                self.image = exp_anim[self.frame]
                self.rect = self.image.get_rect()
                self.rect.midright = midright


class Iscrs(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.image = iscr[0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 60

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(iscr):
                self.kill()
            else:
                center = self.rect.center
                self.image = iscr[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


class EnDeath(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.image = death[0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 45

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(death):
                self.kill()
            else:
                center = self.rect.center
                self.image = death[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


class EnDeath2(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.image = death[0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 45

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(death1):
                self.kill()
            else:
                center = self.rect.center
                self.image = death1[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SIEGE (beta)")
clock = pygame.time.Clock()


background = pygame.image.load(path.join(img_dir, 'back.png')).convert()
background = pygame.transform.scale(background, (800, 480))
background_rect = background.get_rect()
player_img = pygame.image.load(path.join(img_dir, "player.png")).convert()
player_img = pygame.transform.scale(player_img, (player_img.get_rect().size[0] * 0.4166,
                                                 player_img.get_rect().size[1] * 0.4444))
wall_img = pygame.image.load(path.join(img_dir, 'wall.png')).convert()
wall_img = pygame.transform.scale(wall_img, (wall_img.get_rect().size[0] * 0.4166,
                                                 wall_img.get_rect().size[1] * 0.4444))
walldestr_img = pygame.image.load(path.join(img_dir, 'wall1.png')).convert()
walldestr_img = pygame.transform.scale(walldestr_img, (walldestr_img.get_rect().size[0] * 0.4166,
                                                 walldestr_img.get_rect().size[1] * 0.4444))
bullet_img = pygame.image.load(path.join(img_dir, 'bullet.png')).convert()
bullet_img = pygame.transform.scale(bullet_img, (bullet_img.get_rect().size[0] * 0.4166,
                                                 bullet_img.get_rect().size[1] * 0.4444))
mob_img = pygame.image.load(path.join(img_dir, 'enemy.png')).convert()
mob_img = pygame.transform.scale(mob_img, (mob_img.get_rect().size[0] * 0.4166,
                                                 mob_img.get_rect().size[1] * 0.4444))

vshoot = pygame.mixer.Sound(path.join(snd_dir, 'vshoot.wav'))
wall_destr = pygame.mixer.Sound(path.join(snd_dir, 'break.wav'))


exp_anim = []
for i in range(2, 4):
    filename = 'v{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img = pygame.transform.scale(img, (img.get_rect().size[0] * 0.4166,
                                                     img.get_rect().size[1] * 0.4444))
    img.set_colorkey(WHITE)
    exp_anim.append(img)

iscr = []
for i in range(1, 4):
    filename1 = 'i{}.png'.format(i)
    img1 = pygame.image.load(path.join(img_dir, filename1)).convert()
    img1 = pygame.transform.scale(img1, (img1.get_rect().size[0] * 0.4166,
                                       img1.get_rect().size[1] * 0.4444))
    img1.set_colorkey(WHITE)
    iscr.append(img1)

death = []
for i in range(1, 8):
    filename2 = 'e{}.png'.format(i)
    img2 = pygame.image.load(path.join(img_dir, filename2)).convert()
    img2 = pygame.transform.scale(img2, (img2.get_rect().size[0] * 0.4166,
                                       img2.get_rect().size[1] * 0.4444))
    img2.set_colorkey(WHITE)
    death.append(img2)

death1 = []
for i in range(1, 10):
    filename3 = 'e0{}.png'.format(i)
    img3 = pygame.image.load(path.join(img_dir, filename3)).convert()
    img3 = pygame.transform.scale(img3, (img3.get_rect().size[0] * 0.4166,
                                       img3.get_rect().size[1] * 0.4444))
    img3.set_colorkey(WHITE)
    death1.append(img3)

sp = []
for i in range(1, 3):
    filename4 = 'speed{}.png'.format(i)
    img4 = pygame.image.load(path.join(img_dir, filename4)).convert()
    img4 = pygame.transform.scale(img4, (img4.get_rect().size[0] * 0.4166,
                                       img4.get_rect().size[1] * 0.4444))
    img4.set_colorkey(WHITE)
    sp.append(img4)

font_name = pygame.font.match_font('comicsansms')


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def draw_shield_bar(surf, x, y, pct, lenght, maxhp):
    if pct < 0:
        pct = 0
    bar_length = lenght
    bar_height = 10
    fill = (pct / maxhp) * bar_length
    if fill > 0.25 * bar_length:
        color = GREEN
    else:
        color = RED
    outline_rect = pygame.Rect(x, y, bar_length, bar_height)
    fill_rect = pygame.Rect(x, y, fill, bar_height)
    pygame.draw.rect(surf, color, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)


def screeeen():
    screen.blit(background, background_rect)
    draw_text(screen, "CASTLE SIEGE", 64, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, "Updown keys move, Space to fire", 22,
              WIDTH / 2, HEIGHT / 2)
    draw_text(screen, "L_Alt to ULT", 22,
              WIDTH / 2, HEIGHT / 2 + 30)
    draw_text(screen, "Press any key to begin", 18, WIDTH / 2, HEIGHT * 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYUP:
                waiting = False


def game_over():
    pygame.mixer.music.set_volume(0)
    screen.blit(background, background_rect)
    draw_text(screen, "GAME", 64, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, "OVER", 64, WIDTH / 2, HEIGHT / 2)
    draw_text(screen, "press TAB to open menu", 18, WIDTH / 2, HEIGHT * 3.5 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_TAB:
                    waiting = False


sprites = pygame.sprite.Group()
wall = Wall()
sprites.add(wall)
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player()
sprites.add(player)
for i in range(8):
    m = Mob()
    sprites.add(m)
    mobs.add(m)
score = 0
ult = 0


# Цикл игры
gay_over = True
running = True
while running:
    clock.tick(FPS)
    if gay_over:
        gay_over = False
        screeeen()
        sprites = pygame.sprite.Group()
        mobs = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        wall = Wall()
        sprites.add(wall)
        player = Player()
        sprites.add(player)
        for i in range(8):
            m = Mob()
            sprites.add(m)
            mobs.add(m)
        score = 0
        ult = 0

    # Ввод
    for event1 in pygame.event.get():
        # check
        if event1.type == pygame.QUIT:
            running = False
        elif event1.type == pygame.KEYDOWN:
            if event1.key == pygame.K_SPACE:
                player.shoot()
            elif event1.key == pygame.K_DOWN:
                isc = Iscrs(player.rect.midbottom)
                sprites.add(isc)
            elif event1.key == pygame.K_UP:
                isc = Iscrs(player.rect.center)
                sprites.add(isc)
            elif event1.key == pygame.K_LALT:
                if player.ult == 100:
                    if player.ult1 is False:
                        player.ult1 = True
                        player.power_time = pygame.time.get_ticks()
            elif event1.key == pygame.K_BACKSPACE:
                sys.exit()

    # Обновление
    sprites.update()

    # check
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        score += 15
        if player.ult < 100:
            player.ult += 2
        m = Mob()
        sprites.add(m)
        mobs.add(m)
        deat = EnDeath(hit.rect.center)
        sprites.add(deat)

    hits = pygame.sprite.spritecollide(wall, mobs, True)
    for hit in hits:
        if wall.hp > 0:
            wall.hp -= 5
            m = Mob()
            sprites.add(m)
            mobs.add(m)
            deat = EnDeath2(hit.rect.center)
            sprites.add(deat)
            if wall.hp <= 0:
                wall_destr.play()
        else:
            wall.hp1 -= 5
            m = Mob()
            sprites.add(m)
            mobs.add(m)
            deat = EnDeath2(hit.rect.center)
            sprites.add(deat)
            if wall.hp1 <= 0:
                gay_over = True
                game_over()

    # Рендер
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    sprites.draw(screen)
    draw_text(screen, str(score), 18, WIDTH / 2, 10)
    draw_text(screen, ("ULT CHARGE: " + str(player.ult) + "%"), 18, WIDTH * 3 / 4 + 50, 10)
    if wall.hp > 0:
        draw_shield_bar(screen, 5, 5, wall.hp, 300, 100)
    else:
        draw_shield_bar(screen, 5, 5, wall.hp, 300, 100)
        draw_shield_bar(screen, 5, 20, wall.hp1, 150, 50)
    pygame.display.flip()
pygame.quit()
