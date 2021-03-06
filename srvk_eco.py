import pygame
import time
import random
from os import path
import sys
import sqlite3

# основы
img_dir = path.join(path.dirname(__file__), 'myg')
snd_dir = path.join(path.dirname(__file__), 'snd')

WIDTH = 1920
HEIGHT = 1080
FPS = 60

WHITE = (255, 255, 255)
BLACK = (16, 16, 16)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GREEN1 = (0, 253, 0)

POWERUP_TIME = 5000

EX_MUS = pygame.time.get_ticks()

GIG = False
GIG_HP = 0

names = ['VICTORIAN', "VENIAMIN", "ROBERT", "IGNAT", "AINUR", "VOVA", 'CAEZAR', 'DUREMURR', "BEBROMAN THE GREAT"]
name = ''

# классы объектов игры

# класс пуль
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.one = pygame.time.get_ticks()
        if not player.slow:
            self.speedx = 36
        else:
            self.speedx = 18
        self.rect.left = x
        if not seconds:
            self.rect.top = y
        else:
            self.rect.top = y - 35

    def update(self):
        global GIG_HP
        if player.zaw and pygame.time.get_ticks() - self.one > random.randint(50, 85) and self.speedx > 0:
            self.speedx -= 12
            self.one = pygame.time.get_ticks()
        elif player.zaw is False:
            if not player.slow:
                self.speedx = 36
            else:
                self.speedx = 18
        if player.zaw and pygame.time.get_ticks() - player.last_call < 1000:
            self.kill()
        self.rect.x += self.speedx
        if self.rect.left > WIDTH:
            self.kill()
        if GIG and not player.zaw:
            if pygame.sprite.spritecollide(self, gigants, False) and seconds is False:
                floweyhit.play()
                floweyhit.set_volume(0.7)
                if not player.ult1:
                    GIG_HP -= 3
                else:
                    GIG_HP -= 1
                self.kill()

                
# класс плота на второй локации
class Plot(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = plot
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = -600
        self.speedy = 0
        self.speedx = 0
        self.hp = 5

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx


# класс игрока нашей игры
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.speedy = 0
        self.speedx = 0
        self.image = player_img
        self.image.set_colorkey(GREEN)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.centery = HEIGHT / 2
        self.rect.left = 333
        self.slow = False
        if not self.slow:
            self.shoot_delay = 300
        else:
            self.shoot_delay = 500
        self.last_shot = pygame.time.get_ticks()
        self.last_slow = pygame.time.get_ticks()
        self.ult1 = False
        self.ult = 0
        self.zaw = False
        self.zawc = 3
        self.slowc = 0
        self.last_call = pygame.time.get_ticks()
        self.power_time = pygame.time.get_ticks()
        self.l_anim = pygame.time.get_ticks()
        self.plus = pygame.time.get_ticks()
        self.start = pygame.time.get_ticks()
        self.hod = 0

    def update(self):
        now = pygame.time.get_ticks()
        keystate = pygame.key.get_pressed()
        if not end:
            if not self.slow:
                if not self.ult1:
                    self.shoot_delay = 300
                else:
                    self.shoot_delay = 100
            else:
                self.shoot_delay = 600

            if keystate[pygame.K_UP]:
                if not self.slow:
                    self.speedy = -10
                else:
                    self.speedy = -7
            if keystate[pygame.K_DOWN]:
                if not self.slow:
                    self.speedy = 10
                else:
                    self.speedy = 7
        if not stop:
            self.rect.y += self.speedy
            self.rect.x += self.speedx
        if keystate[pygame.K_SPACE]:
            self.shoot()
        if not end:
            if not seconds:
                if self.rect.top < 0:
                    self.rect.top = 0
                if self.rect.bottom > HEIGHT:
                    self.rect.bottom = HEIGHT
            else:
                if self.rect.top < 150:
                    self.rect.top = 150
                if self.rect.bottom > 795:
                    self.rect.bottom = 795
        if not seconds:
            if self.ult1 and pygame.time.get_ticks() - self.power_time > POWERUP_TIME:
                self.ult1 = False
                self.image = player_img
                self.ult = 0
                self.power_time = pygame.time.get_ticks()

            if self.ult1 and pygame.time.get_ticks() - self.l_anim > 100:
                ul = UltAnim(background_rect.center)
                sprites.add(ul)
                self.l_anim = pygame.time.get_ticks()

            if self.zaw and pygame.time.get_ticks() - self.last_call > 9000:
                self.zaw = False
                self.image = player_img
                if wall.image == wall2:
                    wall.image = wall_img
                if wall.image == wall3:
                    wall.image = walldestr_img
                musik.set_volume(1)

            if not self.ult1:
                if now - self.last_shot > 100:
                    if self.zaw and now - self.last_call > 1000:
                        self.image = playerd
                        self.image.set_colorkey(GREEN)
                    else:
                        self.image = player_img
                        self.image.set_colorkey(GREEN)
            else:
                if now - self.last_shot > 80:
                    self.image = player_p_img
                    self.image.set_colorkey(GREEN)
        elif seconds:
            if self.speedx == 0 and self.speedy == 0 or (self.speedx == -1 and self.speedy == 3):
                self.image = player_hod
                self.mask = pygame.mask.from_surface(self.image)
            elif self.speedx != 0 and not self.hod:
                self.hod = pygame.time.get_ticks()
            elif self.speedx != 0 and self.hod:
                if now - self.hod >= 500:
                    if self.image == player_hod:
                        self.image = player_hod2
                        self.mask = pygame.mask.from_surface(self.image)
                    elif self.image == player_hod1:
                        self.image = player_hod
                        self.mask = pygame.mask.from_surface(self.image)
                    else:
                        self.image = player_hod1
                        self.mask = pygame.mask.from_surface(self.image)
                    self.hod = now
            elif self.speedx == 0 and self.speedy > 0:
                self.image = player_hod1
                self.mask = pygame.mask.from_surface(self.image)
            elif self.speedx == 0 and self.speedy < 0:
                self.image = player_hod2
                self.mask = pygame.mask.from_surface(self.image)
        self.speedy = 0

    def shoot(self):
        if not stop:
            now = pygame.time.get_ticks()
            if now - self.last_call > 2000 and self.zaw:
                if now - self.last_shot > self.shoot_delay:
                    bullet = Bullet(self.rect.right, self.rect.centery)
                    expl = BullExpl(self.rect.midright)
                    gilza = Gilza(self.rect.x, self.rect.y)
                    b_anims.add(gilza)
                    sprites.add(gilza)
                    if not self.slow:
                        vshoot.play()
                    else:
                        vshoot1.play()
                    sprites.add(expl)
                    sprites.add(bullet)
                    bullets.add(bullet)
                    self.last_shot = now
            elif self.zaw is False:
                if now - self.last_shot > self.shoot_delay:
                    bullet = Bullet(self.rect.right, self.rect.centery)
                    expl = BullExpl(self.rect.midright)
                    if not seconds:
                        gilza = Gilza(self.rect.x, self.rect.y)
                    else:
                        gilza = Gilza(self.rect.x + 100, self.rect.y - 25)
                    b_anims.add(gilza)
                    sprites.add(gilza)
                    if not self.slow:
                        vshoot.play()
                    else:
                        vshoot1.play()
                    sprites.add(expl)
                    sprites.add(bullet)
                    bullets.add(bullet)
                    self.last_shot = now
            if not seconds:
                if not self.zaw and not self.ult1:
                    self.image = player_otd
                    self.image.set_colorkey(GREEN)
                elif now - self.last_call > 2000 and self.zaw:
                    self.image = player_otd_d
                    self.image.set_colorkey(GREEN)
                elif self.ult1:
                    self.image = player_otd_p
                    self.image.set_colorkey(GREEN)


# анимация "ульты" - быстрые белые полосы у экрана                    
class UltAnim(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.image = sp[0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 40

    def update(self):
        if not abil_stop:
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
        else:
            self.kill()
            player.ult1 = False


# класс каменной стены в игре
class Wall(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.hp = 100
        self.hp1 = 50
        self.image = wall_img
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.left = 216

    def update(self):
        if self.hp <= 0 and self.image == wall_img:
            self.image = walldestr_img
            self.image.set_colorkey(WHITE)


# класс самых обычных врагов            
class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = mob_img
        self.image.set_colorkey(WHITE)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.y = random.randrange(200, 600)
        self.rect.x = random.randrange(1980, 2000)
        if not seconds:
            if not player.slow:
                self.speedx = -(random.randrange(8, 10))
            else:
                self.speedx = -(random.randrange(4, 6))
        else:
            self.speedx = -8
        self.recent = self.speedx
        self.speedy = 0

    def update(self):
        global score, gay_over
        if not stop:
            if player.zaw and pygame.time.get_ticks() - player.last_call > 375:
                self.speedx = 0
            else:
                if (not player.slow and self.recent <= -8) or seconds:
                    self.speedx = self.recent
                else:
                    if player.slow:
                        self.speedx = self.recent // 2
                    elif not player.slow and self.recent > -8:
                        self.recent = self.recent * 2
                        self.speedx = self.recent
            if GIG and self.speedx != 0:
                self.speedx -= 2
            if pygame.sprite.spritecollide(self, bullets, True):
                a = random.randrange(200, 600)
                if not player.slow:
                    bonk.play()
                else:
                    bonk1.play()
                score += 20
                if player.ult < 100:
                    player.ult += 2
                deat = EnDeath(self.rect.center)
                sprites.add(deat)
                if a:
                    self.rect.x = random.randrange(1980, 2100)
                    self.rect.y = a
            elif pygame.sprite.spritecollide(self, players, False) and seconds and player.rect.x <= 1300:
                bruh.play()
                score += 20
                deat = EnDeath2(self.rect.center)
                sprites.add(deat)
                m = Mob()
                sprites.add(m)
                mobs.add(m)
                self.kill()
                plotik.hp -= 1
            elif pygame.sprite.spritecollide(self, walls, False) and not seconds:
                if not player.slow:
                    taken.play()
                else:
                    taken1.play()
                a = random.randrange(200, 600)
                if GIG:
                    if wall.hp > 0:
                        wall.hp -= 6
                    else:
                        wall.hp1 -= 6
                else:
                    if wall.hp > 0:
                        wall.hp -= 5
                    else:
                        wall.hp1 -= 5
                if not player.zaw:
                    deat = EnDeath2(self.rect.center)
                    sprites.add(deat)
                if a:
                    self.rect.x = random.randrange(1980, 2100)
                    self.rect.y = a
                if wall.hp <= 0 and wall.hp1 == 50:
                    if not player.slow:
                        wall_destr.play()
                    else:
                        wall_destr1.play()
                if wall.hp1 <= 0:
                    if player.zawc > 0:
                        second()
                    else:
                        musik.set_volume(0)
                        gay_over = True
                        game_over()

            if seconds and self.rect.x <= 800:
                deat = EnDeath(self.rect.center)
                sprites.add(deat)
                self.kill()
                if plotik.speedx == 0:
                    plotik.hp -= 1
                bruh.play()
            self.rect.x += self.speedx
            self.rect.y += self.speedy


# класс взрыва у дула ружья при выстреле
class BullExpl(pygame.sprite.Sprite):
    def __init__(self, midright):
        pygame.sprite.Sprite.__init__(self)
        if not player.zaw:
            self.image = exp_anim[0]
        else:
            self.image = exp_anim1[0]
        self.rect = self.image.get_rect()
        if not seconds:
            self.rect.midright = midright
        else:
            self.rect.midright = midright
            self.rect.x += 35
            self.rect.y -= 35
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 20

    def update(self):
        if not abil_stop:
            now = pygame.time.get_ticks()
            if now - self.last_update > self.frame_rate:
                self.last_update = now
                self.frame += 1
                if self.frame == len(exp_anim):
                    self.kill()
                else:
                    midright = self.rect.midright
                    if not player.zaw:
                        self.image = exp_anim[self.frame]
                    else:
                        self.image = exp_anim1[self.frame]
                    self.rect = self.image.get_rect()
                    self.rect.midright = midright


# класс облаков, которые вылезают при слоумо
class Smoke(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = smoke
        self.rect = self.image.get_rect()
        self.sp = [(4, 2), (4, -2), (-4, -2), (-4, 2)]
        self.sp1 = [(-4, -2), (-4, 2), (4, 2), (4, -2)]
        self.timer = pygame.time.get_ticks()
        self.rect.x = 0
        self.rect.y = 0
        self.speedx = 0
        self.x = 0
        self.y = 0
        self.c = 0

    def update(self):
        if not abil_stop:
            now = pygame.time.get_ticks()
            if player.slow:
                if self.rect.left < background_rect.left and self.image == smoke:
                    self.rect.x += 8
                elif self.rect.right > background_rect.right and self.image == smoke1:
                    self.rect.x -= 8
            else:
                if self.rect.right < background_rect.left or self.rect.left > background_rect.right:
                    self.kill()
            if now - self.timer >= 150:
                if self.c <= 3:
                    if self.image == smoke:
                        self.x, self.y = self.sp[self.c]
                    else:
                        self.x, self.y = self.sp1[self.c]
                    self.c += 1
                if self.c == 4:
                    self.c = 0
                self.timer = now
            self.rect.x += self.x
            self.rect.y += self.y
            self.rect.x += self.speedx
        else:
            self.kill()
            player.slow = False
            slowing.stop()


# класс затемнения экрана при слоумо
class Sumrak(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = nigger
        self.rect = self.image.get_rect()

    def update(self):
        if abil_stop:
            self.kill()
            slowing.stop()
            player.slow = False


# класс вылетающей гильзы при выстреле
class Gilza(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        if not player.zaw:
            self.image = gilz_anim[0]
        else:
            self.image = gilz_anim1[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = pygame.mask.from_surface(self.image)
        self.centr = self.rect.center
        self.a = random.randrange(13, 30)
        self.b = random.randrange(-5, 5)
        self.rect.x -= self.a
        self.rect.y -= self.b
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.stopf = random.choice(range(1, 6))
        self.stop = False
        now = pygame.time.get_ticks()
        if not player.zaw:
            if not player.slow:
                self.frame_rate = 30
            else:
                self.frame_rate = 60
        elif player.zaw and now - player.last_call > 1000:
            self.frame_rate = 60
            self.image = gilz_anim1[self.frame]
            self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        if not stop and not abil_stop:
            if pygame.sprite.collide_mask(self, player) and self.frame + 1 == len(gilz_anim):
                self.image = empty
                self.image.set_colorkey(WHITE)
            else:
                now = pygame.time.get_ticks()
                if not player.zaw:
                    if not player.slow:
                        self.frame_rate = 30
                    else:
                        self.frame_rate = 60
                if player.zaw and now - player.last_call > 1000:
                    if self.stop:
                        self.frame_rate = 20000
                        self.image = gilz_anim1[self.frame]
                        self.mask = pygame.mask.from_surface(self.image)
                    else:
                        self.frame_rate = 60
                        self.image = gilz_anim1[self.frame]
                        self.mask = pygame.mask.from_surface(self.image)
                if self.frame == self.stopf:
                    self.stop = True

                if now - self.last_update > self.frame_rate:
                    self.last_update = now
                    self.frame += 1
                    if self.frame == len(gilz_anim):
                        self.frame -= 1
                        self.image = gilz_anim[self.frame]
                        self.mask = pygame.mask.from_surface(self.image)
                    else:
                        if not player.zaw:
                            self.image = gilz_anim[self.frame]
                            self.mask = pygame.mask.from_surface(self.image)
                        elif player.zaw and now - player.last_call > 1000:
                            self.image = gilz_anim1[self.frame]
                            self.mask = pygame.mask.from_surface(self.image)
                        self.rect = self.image.get_rect()
                        self.rect.center = self.centr
                        self.rect.x -= self.a
                        self.rect.y -= self.b


# класс искр, вылетающих при смене направления движения игрока
class Iscrs(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.image = iscr[0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        if not player.slow:
            self.frame_rate = 60
        else:
            self.frame_rate = 120

    def update(self):
        if not stop:
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


# класс анимации смерти обычного врага при попадании пули                    
class EnDeath(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.image = death[0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        if player.zaw is False:
            if not player.slow:
                self.frame_rate = 48
            else:
                self.frame_rate = 96
        else:
            self.frame_rate = 20000

    def update(self):
        if not stop:
            if player.zaw is False:
                if not player.slow:
                    self.frame_rate = 48
                else:
                    self.frame_rate = 96
            if player.zaw and pygame.time.get_ticks() - player.last_call > 375:
                self.frame_rate = 20000

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
        else:
            self.kill()


# класс анимации смерти обычного врага при ударе об стену           
class EnDeath2(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.image = death[0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        if player.zaw is False:
            if not player.slow:
                self.frame_rate = 45
            else:
                self.frame_rate = 90
        else:
            self.frame_rate = 15

    def update(self):
        if not stop:
            if player.zaw is False:
                if not player.slow:
                    self.frame_rate = 45
                else:
                    self.frame_rate = 90
            elif player.zaw and pygame.time.get_ticks() - player.last_call > 375:
                self.frame_rate = 20000

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
        else:
            self.kill()


# класс анимации таймстопа            
class DIO(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = dio[0]
        self.rect = self.image.get_rect()
        self.rect.center = x, y
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 60

    def update(self):
        if (not abil_stop and not seconds) or self.frame_rate == 15:
            now = pygame.time.get_ticks()
            if now - self.last_update > self.frame_rate:
                self.last_update = now
                self.frame += 1
                if self.frame == len(dio):
                    self.kill()
                else:
                    center = self.rect.center
                    self.image = dio[self.frame]
                    self.rect = self.image.get_rect()
                    self.rect.center = center
        else:
            self.kill()
            player.zaw = False
            zaward.stop()


# класс для босса мобов            
class Giant(pygame.sprite.Sprite):
    def __init__(self):
        global name
        pygame.sprite.Sprite.__init__(self)
        self.image = gig[0]
        self.rect = self.image.get_rect()
        self.rect.y = 150
        self.rect.x = 1980
        self.speedy = 0
        self.frame = 0
        if not player.slow:
            self.frame_rate = 500
        else:
            self.frame_rate = 1000
        self.last_update = pygame.time.get_ticks()
        self.last_spawn = pygame.time.get_ticks()
        name = random.choice(names)

    def update(self):
        global GIG_HP, GIG
        if not stop:
            now = pygame.time.get_ticks()
            if not player.slow:
                self.frame_rate = 500
            else:
                self.frame_rate = 1000
            if player.zaw and now - player.last_call > 375:
                self.speedx = 0
            elif not player.zaw and self.rect.right > background_rect.right and GIG_HP > 0:
                self.speedx = -4
            elif GIG_HP > 0 and self.rect.top <= background_rect.right:
                self.speedx = 0
            else:
                self.speedx = 3

            if not player.zaw and not stop:
                if now - self.last_update > self.frame_rate:
                    self.last_update = now
                    self.frame += 1
                    if self.frame == len(gig):
                        self.frame = -1
                    else:
                        center = self.rect.center
                        self.image = gig[self.frame]
                        self.rect = self.image.get_rect()
                        self.rect.center = center
            self.rect.x += self.speedx
            if self.rect.left >= background_rect.right and now - self.last_spawn > 1000:
                self.kill()
                GIG = False

# инициализация всех медиафайлов
                
a = True
if a:
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("BEBRA SIEGE")
    clock = pygame.time.Clock()
    con = sqlite3.connect("scores.sqlite")

    background = pygame.image.load(path.join(img_dir, 'back.png')).convert()
    back_main = pygame.image.load(path.join(img_dir, 'back_main.png')).convert()
    back_wow = pygame.image.load(path.join(img_dir, 'back_wow.png')).convert()
    scary = pygame.image.load(path.join(img_dir, 'scary.jpg')).convert()
    empty = pygame.image.load(path.join(img_dir, 'empty.png')).convert()
    background_rect = background.get_rect()
    back1 = pygame.image.load(path.join(img_dir, "back1.png")).convert()
    wall_img = pygame.image.load(path.join(img_dir, "wall.png")).convert()
    walldestr_img = pygame.image.load(path.join(img_dir, "wall1.png")).convert()
    wall2 = pygame.image.load(path.join(img_dir, "wall2.png")).convert()
    wall3 = pygame.image.load(path.join(img_dir, "wall3.png")).convert()
    player_img = pygame.image.load(path.join(img_dir, "player.png")).convert()
    plot = pygame.image.load(path.join(img_dir, "plot0.png")).convert()
    plot1 = pygame.image.load(path.join(img_dir, "plot1.png")).convert()
    plot2 = pygame.image.load(path.join(img_dir, "plot2.png")).convert()
    plot3 = pygame.image.load(path.join(img_dir, "plot3.png")).convert()
    smoke = pygame.image.load(path.join(img_dir, "smoke.png")).convert()
    smoke1 = pygame.image.load(path.join(img_dir, "smoke1.png")).convert()
    nigger = pygame.image.load(path.join(img_dir, "black.png")).convert_alpha()
    plotiks = [plot, plot1, plot2, plot3]
    bullet_img = pygame.image.load(path.join(img_dir, "bullet.png")).convert()
    mob_img = pygame.image.load(path.join(img_dir, "enemy.png")).convert()
    player_p_img = pygame.image.load(path.join(img_dir, "player_p.png")).convert()
    player_hod = pygame.image.load(path.join(img_dir, "player_hod.png")).convert_alpha()
    player_hod1 = pygame.image.load(path.join(img_dir, "player_hod_1.png")).convert_alpha()
    player_hod2 = pygame.image.load(path.join(img_dir, "player_hod_2.png")).convert_alpha()
    playerd = pygame.image.load(path.join(img_dir, "playerd.png")).convert()
    player_otd = pygame.image.load(path.join(img_dir, "player_otd.png")).convert()
    player_otd_p = pygame.image.load(path.join(img_dir, "player_otd_p.png")).convert()
    player_otd_d = pygame.image.load(path.join(img_dir, "player_otd_d.png")).convert()

    vshoot = pygame.mixer.Sound(path.join(snd_dir, "vshoot.wav"))
    vshoot1 = pygame.mixer.Sound(path.join(snd_dir, "vshoot1.wav"))
    end_mus = pygame.mixer.Sound(path.join(snd_dir, "end_mus.mp3"))
    tudududu = pygame.mixer.Sound(path.join(snd_dir, 'tudududu.mp3'))
    bruh = pygame.mixer.Sound(path.join(snd_dir, "bruh.wav"))
    wall_destr = pygame.mixer.Sound(path.join(snd_dir, "break.mp3"))
    wall_destr1 = pygame.mixer.Sound(path.join(snd_dir, "break1.mp3"))
    anv_12 = pygame.mixer.Sound(path.join(snd_dir, "anvil_land.mp3"))
    anv_3 = pygame.mixer.Sound(path.join(snd_dir, "anvil_break.mp3"))
    slowing = pygame.mixer.Sound(path.join(snd_dir, "slowingboom.wav"))
    papich = pygame.mixer.Sound(path.join(snd_dir, "papich.wav"))
    taken = pygame.mixer.Sound(path.join(snd_dir, "damage.wav"))
    taken1 = pygame.mixer.Sound(path.join(snd_dir, "damage1.wav"))
    zaward = pygame.mixer.Sound(path.join(snd_dir, "zaward.wav"))
    tosec = pygame.mixer.Sound(path.join(snd_dir, "travel.mp3"))
    zaward1 = pygame.mixer.Sound(path.join(snd_dir, "zaward1.wav"))
    tp = pygame.mixer.Sound(path.join(snd_dir, "tp.mp3"))
    bonk = pygame.mixer.Sound(path.join(snd_dir, "bonk.wav"))
    bonk1 = pygame.mixer.Sound(path.join(snd_dir, "bonk1.wav"))
    money = pygame.mixer.Sound(path.join(snd_dir, "money.wav"))
    money.set_volume(0.7)
    musik = pygame.mixer.Sound(path.join(snd_dir, "musik.wav"))
    musik2 = pygame.mixer.Sound(path.join(snd_dir, "musik2.mp3"))
    musik2.set_volume(0.05)
    floweyhit = pygame.mixer.Sound(path.join(snd_dir, "floweyhit.wav"))

    exp_anim = []
    for i in range(2, 4):
        filename = 'v{}.png'.format(i)
        img = pygame.image.load(path.join(img_dir, filename)).convert()
        img.set_colorkey(WHITE)
        exp_anim.append(img)

    back2_anim = []
    for i in range(0, 5):
        filename = 'back2_{}.png'.format(i)
        img = pygame.image.load(path.join(img_dir, filename)).convert()
        back2_anim.append(img)
    back2_rect = back2_anim[0].get_rect()

    exp_anim1 = []
    for i in range(2, 4):
        filename = 'v{}1.png'.format(i)
        img = pygame.image.load(path.join(img_dir, filename)).convert()
        img.set_colorkey(WHITE)
        exp_anim1.append(img)

    end_anim = []
    for i in range(1, 5):
        filename = 'backend_{}.png'.format(i)
        img = pygame.image.load(path.join(img_dir, filename)).convert()
        end_anim.append(img)

    gilz_anim = []
    for i in range(1, 7):
        filename = 'gilz{}.png'.format(i)
        img = pygame.image.load(path.join(img_dir, filename)).convert_alpha()
        gilz_anim.append(img)

    gilz_anim1 = []
    for i in range(1, 7):
        filename = 'gilz{}1.png'.format(i)
        img = pygame.image.load(path.join(img_dir, filename)).convert()
        img.set_colorkey(WHITE)
        gilz_anim1.append(img)

    gig = []
    for i in range(1, 5):
        filename = 'g{}.png'.format(i)
        img = pygame.image.load(path.join(img_dir, filename)).convert()
        img.set_colorkey(WHITE)
        gig.append(img)

    dio = []
    for i in range(1, 29):
        filename5 = '1 ({}).png'.format(i)
        img5 = pygame.image.load(path.join(img_dir, filename5)).convert()
        img5.set_colorkey(BLACK)
        dio.append(img5)

    iscr = []
    for i in range(1, 4):
        filename1 = 'i{}.png'.format(i)
        img1 = pygame.image.load(path.join(img_dir, filename1)).convert()
        img1.set_colorkey(WHITE)
        iscr.append(img1)

    death = []
    for i in range(1, 8):
        filename2 = 'e{}.png'.format(i)
        img2 = pygame.image.load(path.join(img_dir, filename2)).convert()
        img2.set_colorkey(WHITE)
        death.append(img2)

    death1 = []
    for i in range(1, 10):
        filename3 = 'e0{}.png'.format(i)
        img3 = pygame.image.load(path.join(img_dir, filename3)).convert()
        img3.set_colorkey(WHITE)
        death1.append(img3)

    sp = []
    for i in range(1, 3):
        filename4 = 'speed{}.png'.format(i)
        img4 = pygame.image.load(path.join(img_dir, filename4)).convert()
        img4.set_colorkey(WHITE)
        sp.append(img4)

    font_name = 'myg/minecraft.ttf'

    
# вспомогательные функции и функции, отвечающие за экраны и переходы между ними
   
    
# отрисовка текста


def draw_text(surf, text, size, x, y, color):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


# отрисовка различных шкал
    
    
def draw_shield_bar(surf, x, y, pct, lenght, maxhp):
    if pct < 0:
        pct = 0
    bar_length = lenght
    bar_height = 25
    fill = (pct / maxhp) * bar_length
    if GIG and pct == GIG_HP:
        color = RED
    elif (fill > 0.25 * bar_length and (pct == wall.hp or pct == wall.hp1)) or (seconds and
                                                                                fill > 0.25 * bar_length):
        color = GREEN
    elif pct == player.slowc and not seconds:
        if not player.slow:
            if player.slowc < 2000:
                color = (0, 0, 255)
            else:
                color = (148, 0, 211)
        else:
            color = (148, 0, 211)
    else:
        color = RED
    outline_rect = pygame.Rect(x, y, bar_length, bar_height)
    fill_rect = pygame.Rect(x, y, fill, bar_height)
    pygame.draw.rect(surf, color, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)


# функция главного экрана
    
    
def screeeen():
    screen.blit(back_main, background_rect)
    draw_text(screen, "BEBRA SIEGE", 100, WIDTH / 2, HEIGHT / 4, RED)
    draw_text(screen, "BACKSPACE - exit", 25, 140, 20, WHITE)
    draw_text(screen, "RSHIFT - records", 25, 1780, 20, WHITE)
    draw_text(screen, "Updown keys move, Space to fire", 50,
              WIDTH / 2, HEIGHT / 2, WHITE)
    draw_text(screen, "L_Alt to ULT", 50,
              WIDTH / 2, HEIGHT / 2 + 60, WHITE)
    draw_text(screen, "L_Ctrl to TIMESTOP", 50,
              WIDTH / 2, HEIGHT / 2 + 120, WHITE)
    draw_text(screen, "L_Shift to SLOWMO", 50,
              WIDTH / 2, HEIGHT / 2 + 180, WHITE)
    draw_text(screen, "Press any key to begin", 24, WIDTH / 2, HEIGHT * 3 / 4, WHITE)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_BACKSPACE:
                    sys.exit()
                elif event.key == pygame.K_RSHIFT:
                    records()
                else:
                    waiting = False


# класс окна после смерти игрока          
                    
                    
def game_over():
    global GIG, GIG_HP, con, toright, b, c
    musik.stop()
    bruh.play()
    tudududu.play()
    screen.blit(scary, background_rect)
    draw_text(screen, "YOU", 150, WIDTH / 2, HEIGHT / 4 - 100, RED)
    draw_text(screen, "DIED", 150, WIDTH / 2, HEIGHT / 2 - 100, RED)
    draw_text(screen, f"bruh... score is 0", 50, WIDTH / 2, HEIGHT * 3 / 4, WHITE)
    draw_text(screen, "press TAB to open menu", 24, WIDTH / 2, HEIGHT * 3.5 / 4, WHITE)
    for e in sprites:
        e.kill()
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                GIG = False
                GIG_HP = 0
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    waiting = False
                    GIG = False
                    GIG_HP, b, c = 0, 0, 0
                    toright = 600
                    tudududu.stop()
                    screeeen()
                elif event1.key == pygame.K_BACKSPACE:
                    sys.exit()


# класс экрана после побега игрока
                    
                    
def happy_over():
    global GIG, GIG_HP, con, toright, b, c
    musik2.stop()
    end_mus.play()
    end_mus.set_volume(0.2)
    screen.blit(end_anim[0], background_rect)
    con.execute(f"UPDATE Последний SET Колво = {score}")
    con.execute(f"INSERT INTO Рекорды(Коллво) VALUES({score})")
    con.commit()
    for e in sprites:
        e.kill()
    pygame.display.flip()
    take = pygame.time.get_ticks()
    counter = 0
    flag = False
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                GIG = False
                GIG_HP = 0
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    waiting = False
                    GIG = False
                    GIG_HP, b, c = 0, 0, 0
                    toright = 600
                    end_mus.stop()
                    screeeen()
                elif event1.key == pygame.K_BACKSPACE:
                    sys.exit()
        if pygame.time.get_ticks() - take >= 250:
            if counter < 3 and not flag:
                counter += 1
                if counter == 3:
                    flag = True
            elif flag and counter > 0:
                counter -= 1
                if counter == 0:
                    flag = False
            take = pygame.time.get_ticks()
        screen.blit(end_anim[counter], background_rect)
        draw_text(screen, "YOU", 150, WIDTH / 2, HEIGHT / 4 - 100, GREEN)
        draw_text(screen, "SURVIVED", 150, WIDTH / 2, HEIGHT / 2 - 100, GREEN)
        draw_text(screen, f"{score}", 50, WIDTH / 2, HEIGHT * 3 / 4, WHITE)
        draw_text(screen, "press TAB to open menu", 24, WIDTH / 2, HEIGHT * 3.5 / 4, WHITE)
        pygame.display.flip()


# класс паузы
        
        
def pause():
    if not seconds:
        musik.set_volume(0)
    else:
        musik2.set_volume(0)
    if player.zaw:
        zaward.set_volume(0)
    elif player.slow:
        slowing.set_volume(0)
    screen.blit(back_main, background_rect)
    draw_text(screen, "PAUSE", 128, WIDTH / 2, HEIGHT / 4, WHITE)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    sys.exit()
                elif event.key == pygame.K_ESCAPE:
                    waiting = False
                    if not seconds:
                        musik.set_volume(1)
                    else:
                        musik2.set_volume(0.05)
                    zaward.set_volume(1)


# класс окна рекордов
                    
                    
def records():
    global con
    screen.blit(back_wow, background_rect)
    draw_text(screen, "RECORDS", 100, WIDTH / 2, HEIGHT / 15, WHITE)
    ex = con.execute("""SELECT Коллво FROM Рекорды""").fetchall()
    sp = []
    for e in ex:
        sp.append(e[0])
    sp.sort(reverse=True)
    for i in range(5):
        draw_text(screen, str(i + 1) + ' - ' + str(sp[i]), 100, WIDTH / 2, (2 + i) * (HEIGHT / 10), WHITE)
    ex = con.execute("""SELECT Колво FROM Последний""").fetchall()
    draw_text(screen, 'Your last score is ' + str(ex[0][0]), 100, WIDTH / 2, 8 * (HEIGHT / 10), WHITE)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    sys.exit()
                elif event.key == pygame.K_ESCAPE:
                    waiting = False
                    screeeen()


# класс перехода с 1 локации на 2
                    
                    
def second():
    global seconds, sprites, players, player, gigant, plotik, mobs, stop, end, b_anims, abil_stop
    abil_stop = True
    run = True
    flag = False
    a = pygame.time.get_ticks()
    ab = 0
    wall.image = wall3
    wall.image.set_colorkey(WHITE)
    dior = DIO(960, 540)
    dior.frame_rate = 15
    sprites.add(dior)
    zaward1.play()
    musik.stop()
    for e in b_anims:
        e.image = gilz_anim1[e.frame]
    while run:
        for event1 in pygame.event.get():
            if event1.type == pygame.QUIT:
                sys.exit()
            elif event1.type == pygame.KEYDOWN:
                if event1.key == pygame.K_BACKSPACE:
                    sys.exit()
        if pygame.time.get_ticks() - a <= 2000:
            stop = True
        elif pygame.time.get_ticks() - a >= 700 and not flag:
            tosec.play()
            flag = True
        else:
            if not ab:
                ab = pygame.time.get_ticks()
        sprites.update()
        screen.fill(BLACK)
        screen.blit(back1, background_rect)
        sprites.draw(screen)
        if ab:
            if pygame.time.get_ticks() - ab <= 5000:
                screen.fill(BLACK)
            else:
                run = False
                stop = False
        pygame.display.flip()
    for e in sprites:
        e.rect.x = 1980
        e.kill()
    for e in players:
        e.kill()
    plotik = Plot()
    player = Player()
    players.add(player)
    player.image = player_hod1
    tp.play()
    sprites.add(plotik)
    sprites.add(player)
    player.rect.x = 1930
    player.speedx = -2
    seconds = True
    abil_stop = False
    musik2.play()


# Цикл игры + флаги и таймеры для него
gay_over, running, end, stop, abil_stop, seconds = True, True, False, False, False, False
c = 0
toright = 600
b = 0
b_last = pygame.time.get_ticks()
txt_anim = pygame.time.get_ticks()
pygame.mouse.set_visible(False)
txt_c = 1
txt_curr = 0
while running:
    clock.tick(FPS)
    start_time = time.time()
    # первый уровень
    if not seconds:
        screen.fill(WHITE)
        if gay_over:
            gay_over = False
            screeeen()
            musik.play()
            musik.set_volume(1)
            sprites = pygame.sprite.Group()
            mobs = pygame.sprite.Group()
            bullets = pygame.sprite.Group()
            gigants = pygame.sprite.Group()
            players = pygame.sprite.Group()
            b_anims = pygame.sprite.Group()
            walls = pygame.sprite.Group()
            wall = Wall()
            walls.add(wall)
            sprites.add(wall)
            player = Player()
            players.add(player)
            sprites.add(player)
            for i in range(8):
                m = Mob()
                sprites.add(m)
                mobs.add(m)
            score = 0
            ult = 0
        # Ввод
        for event1 in pygame.event.get():
            if event1.type == pygame.QUIT:
                running = False
            elif event1.type == pygame.KEYDOWN:
                if event1.key == pygame.K_SPACE:
                    player.shoot()
                elif event1.key == pygame.K_DOWN:
                    if not player.zaw:
                        isc = Iscrs(player.rect.midbottom)
                        sprites.add(isc)
                elif event1.key == pygame.K_UP:
                    if not player.zaw:
                        isc = Iscrs(player.rect.center)
                        sprites.add(isc)
                elif event1.key == pygame.K_LALT:
                    if player.ult1 is False and player.zaw is False and player.slow is False:
                        if player.ult == 100:
                            if player.ult1 is False:
                                player.ult1 = True
                                player.image = player_p_img
                                player.image.set_colorkey(GREEN)
                                papich.play()
                                player.power_time = pygame.time.get_ticks()
                elif event1.key == pygame.K_LCTRL:
                    if player.ult1 is False and player.zaw is False and player.slow is False:
                        if player.zawc > 0:
                            player.zawc -= 1
                            player.zaw = True
                            musik.set_volume(0)
                            player.last_call = pygame.time.get_ticks()
                            dioo = DIO(960, 540)
                            sprites.add(dioo)
                            zaward.play()
                elif event1.key == pygame.K_LSHIFT:
                    if player.slow is False and player.zaw is False and player.ult1 is False and player.slowc >= 2000:
                        player.slow = True
                        smoke2 = Smoke()
                        smoke2.image = smoke
                        smoke2.image.set_colorkey((0, 0, 0))
                        smoke2.rect.x = -1920
                        smoke3 = Smoke()
                        smoke3.image = smoke1
                        smoke3.image.set_colorkey((0, 0, 0))
                        smoke3.rect.x = 1920
                        player.last_slow = pygame.time.get_ticks()
                        sprites.add(smoke2)
                        sprites.add(smoke3)
                        slowing.play()
                        musik.set_volume(0)
                    else:
                        print(player.slow, player.zaw, player.ult1, player.slowc)
                elif event1.key == pygame.K_ESCAPE:
                    pause()
                elif event1.key == pygame.K_BACKSPACE:
                    sys.exit()

        # Обновление
        sprites.update()

        # различные проверки, изменения и т.д
        if not player.zaw:
            if len(b_anims) > 10:
                counter = 0
                for e in b_anims:
                    if counter == 0:
                        e.kill()
                        counter += 1

        if pygame.time.get_ticks() - EX_MUS > 96000:
            if not player.zaw and not player.slow:
                musik.play()
                musik.set_volume(1)
                EX_MUS = pygame.time.get_ticks()

        if score % 5000 == 0 and score and GIG is False:
            gigant = Giant()
            gigants.add(gigant)
            sprites.add(gigant)
            GIG = True
            GIG_HP = 45

        if pygame.time.get_ticks() - player.last_call > 1000 and player.zaw and (player.image != playerd or
                                                                                 player.image != player_otd_d):
            if wall.image == wall_img:
                wall.image = wall2
                wall.image.set_colorkey(WHITE)
            elif wall.image == walldestr_img:
                wall.image = wall3
                wall.image.set_colorkey(WHITE)

        if player.zaw:
            if pygame.time.get_ticks() - player.last_call > 1000:
                screen.blit(back1, background_rect)
            else:
                screen.blit(background, background_rect)
                if player.slowc < 2000 and not player.slow:
                    player.slowc += 1
        else:
            screen.blit(background, background_rect)
            if player.slowc < 2000 and not player.slow:
                player.slowc += 1

        # отрисовка

        sprites.draw(screen)
        draw_text(screen, str(score), 40, WIDTH / 2, 10, WHITE)
        draw_text(screen, ("TIMESTOPS: " + str(player.zawc)), 40, WIDTH * 3 / 4 + 50, 50, WHITE)
        draw_text(screen, ("ULT CHARGE: " + str(player.ult) + "%"), 40, WIDTH * 3 / 4 + 50, 10, WHITE)
        if GIG:
            draw_text(screen, "mob ATK+ SPD+", 40, WIDTH / 2, 60, WHITE)
            draw_text(screen, name, 55, WIDTH / 2, 800, RED)
            draw_shield_bar(screen, WIDTH / 2 - 225, 900, GIG_HP, 450, 45)

        if not player.zaw:
            a = random.randrange(1, 45000)
            if a in range(1, 11) and pygame.time.get_ticks() - player.start > 2000:
                player.zawc += 1
                money.play()
                player.plus = pygame.time.get_ticks()
            if (pygame.time.get_ticks() - player.plus <= 2000) and (pygame.time.get_ticks() - player.start > 2000):
                draw_text(screen, "+1", 40, WIDTH * 3 / 4 + 250, 50, GREEN)

        if wall.hp > 0:
            draw_shield_bar(screen, 10, 10, wall.hp, 600, 100)
        else:
            draw_shield_bar(screen, 10, 10, wall.hp, 600, 100)
            draw_shield_bar(screen, 10, 40, wall.hp1, 300, 50)
        draw_shield_bar(screen, WIDTH * 3 / 4 - 100, 90, player.slowc, 300, 2000)
        if pygame.time.get_ticks() - player.last_slow <= 12000:
            if pygame.time.get_ticks() - player.last_slow <= 80 and player.slow:
                screen.fill(BLACK)
            if pygame.time.get_ticks() - player.last_slow > 70 and player.slow:
                try:
                    niga.kill()
                except Exception:
                    pass
                niga = Sumrak()
                sprites.add(niga)
            else:
                try:
                    niga.kill()
                except Exception:
                    pass
            if player.slowc > 0 and player.slow:
                player.slowc -= 2.7777777777
                if player.slowc < 0:
                    player.slowc = 0
        else:
            if player.slow:
                player.slow = False
                niga.kill()
                smoke2.speedx = -8
                smoke3.speedx = 8
                slowing.stop()
                if not player.zaw:
                    musik.set_volume(1)
            else:
                if not player.zaw:
                    musik.set_volume(1)
    # второй уровень
    else:
        musik.stop()
        # ввод
        for event1 in pygame.event.get():
            if event1.type == pygame.QUIT:
                running = False
            elif event1.type == pygame.KEYDOWN:
                if event1.key == pygame.K_SPACE:
                    player.shoot()
                elif event1.key == pygame.K_ESCAPE:
                    pause()
                elif event1.key == pygame.K_BACKSPACE:
                    sys.exit()
        # обновление
        sprites.update()

        # проверки и т.д.

        if len(b_anims) > 20:
            counter = 0
            for e in b_anims:
                if counter == 0:
                    e.kill()
                    counter += 1
        if pygame.time.get_ticks() - b_last >= 200:
            b += 1
            if b > 4:
                b = 0
            b_last = pygame.time.get_ticks()
        if pygame.time.get_ticks() - txt_anim >= 1000:
            txt_anim = pygame.time.get_ticks()
            if txt_c % 2 == 0:
                txt_curr = 0
            else:
                txt_curr = 1
            txt_c += 1
        if toright >= 1:
            toright -= 1
            plotik.rect.x += 1
            for e in b_anims:
                e.rect.x += 1
        if player.rect.x <= 350 and player.speedx != 0:
            player.speedx = 0
            a = pygame.time.get_ticks()
        elif player.rect.x <= 1300 and len(mobs) == 0:
            pors = [2080, 2300, 2400, 2500, 2700, 2900, 2850, 2600]
            for i in range(8):
                m = Mob()
                m.rect.x = pors[i]
                m.speedx = 3
                sprites.add(m)
                mobs.add(m)
        elif player.rect.x > 1300 and len(mobs) == 0:
            plotik.hp = 5
        if player.rect.x <= 350 and player.speedx == 0:
            if c < 4:
                if pygame.time.get_ticks() - a >= 5000:
                    plotik.image = plotiks[c]
                    plotik.image.set_colorkey(WHITE)
                    c += 1
                    a = pygame.time.get_ticks()
                    if c != 1:
                        anv_12.play()
            else:
                if pygame.time.get_ticks() - a >= 5000:
                    anv_3.play()
                    end = True
        if end:
            plotik.speedx = -1
            plotik.speedy = 3
            player.speedx = -1
            player.speedy = 3
            for e in b_anims:
                if e.rect.x <= 875:
                    e.rect.x -= 1
                    e.rect.y += 3
        if plotik.rect.top >= HEIGHT and player.rect.top >= HEIGHT and len(mobs) == 0:
            gay_over = True
            seconds = False
            end = False
            musik2.stop()
            for e in sprites:
                e.kill()
            player.kill()
            happy_over()
        if plotik.hp <= 0:
            gay_over = True
            seconds = False
            end = False
            musik2.stop()
            for e in sprites:
                e.kill()
            player.kill()
            game_over()

        # отрисовка

        screen.fill(BLACK)
        screen.blit(back2_anim[b], (-toright, 0))
        draw_text(screen, str(score), 40, WIDTH / 2, 10, WHITE)
        if txt_curr == 0:
            draw_text(screen, "ЖИТЬ!ЖИТЬ!ЖИТЬ!", 40, WIDTH / 2, 70, WHITE)
        else:
            draw_text(screen, "ЖИТЬ!  ЖИТЬ!  ЖИТЬ!", 40, WIDTH / 2, 70, WHITE)
        draw_shield_bar(screen, 10, 10, plotik .hp, 300, 5)
        sprites.draw(screen)
    # счетчик фпс
    draw_text(screen, ("FPS:" + str(int(1.0 / (time.time() - start_time)))), 40, 100, 100, WHITE)
    pygame.display.flip()
sys.exit()
