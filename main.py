from pygame import *
from pygame import rect
from random import randint
import time as time_module
font.init()
font = font.SysFont('Arial', 40)
mixer.init()
window = display.set_mode((1200, 800))
display.set_caption('Шутер')
background = transform.scale(image.load('galaxy.jpg'), (1200, 800))

mixer.music.load('space (1).ogg')
mixer.music.play(-1)
bullet_sound = mixer.Sound('fire (1).ogg')

enemy_x = randint(0, 500)
enemy_speed = randint(5, 7)



speed = 10

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, player_width, player_height):
        super().__init__()
        self.width = player_width
        self.height = player_height
        self.image = transform.scale(image.load(player_image), (player_width, player_height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
bullets = sprite.Group()
class Player(GameSprite):
    def update(self):
        key_pressed = key.get_pressed()
        if key_pressed[K_RIGHT] and self.rect.x < 1200 - 130 - 5:
            self.rect.x += speed
        if key_pressed[K_LEFT] and self.rect.x > 5:
            self.rect.x -= speed
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
    def fire(self):
        bullet = Bullet('bullet (1).png', self.rect.centerx - 15, self.rect.top, speed, 30, 40)
        bullets.add(bullet)

lost = 0

class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > 700:
            self.rect.y = 0
            self.rect.x = randint(0, 800)
            lost += 1

class Metiotits(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 700:
            self.rect.y = 0
            self.rect.x = randint(0, 800)


class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()

metiorit = Metiotits('asteroid (3).png', randint(0, 800), 0, randint(1,3), 100, 70)
metiorit2 = Metiotits('asteroid (3).png', randint(0, 800), 0, randint(1,3), 100, 70)
metiorit3 = Metiotits('asteroid (3).png', randint(0, 800), 0, randint(1,3), 100, 70)

metiorits = sprite.Group()
metiorits.add(metiorit)
metiorits.add(metiorit2)
metiorits.add(metiorit3)

monster = Enemy('ufo (1).png', randint(0, 800), 0, randint(1, 3), 130, 100)
monster2 = Enemy('ufo (1).png', randint(0, 800), 0, randint(1, 3), 130, 100)
monster3 = Enemy('ufo (1).png', randint(0, 800), 0, randint(1, 3), 130, 100)
monster4 = Enemy('ufo (1).png', randint(0, 800), 0, randint(1, 3), 130, 100)
monster5 = Enemy('ufo (1).png', randint(0, 800), 0, randint(1, 3), 130, 100)

monsters = sprite.Group()
monsters.add(monster)
monsters.add(monster2)
monsters.add(monster3)
monsters.add(monster4)
monsters.add(monster5)



player = Player('rocket.png', 320, 620, speed, 130, 170)

win = font.render('Ты выиграл', True, (255, 255, 255))
lose = font.render('Ты не выиграл', True, (255, 255, 255))

scet = 0


clock = time.Clock()
fps = 60
game = True
finish = False




rel_time = False
num_fire = 0
start = 0
while game:

    if finish != True:
        window.blit(background, (0, 0))
        player.reset()
        player.update()
        metiorits.update()
        metiorits.draw(window)
        monsters.update()
        monsters.draw(window)
        bullets.update()
        bullets.draw(window)
        schetchik1 = font.render('Пропущено: ' + str(lost), 1, (255, 255, 255))
        schetchik2 = font.render('Счёт: ' + str(scet), 1, (255, 255, 255))
        window.blit(schetchik1, (35, 35))
        window.blit(schetchik2, (35, 70))

        if lost == 5:
            finish = True
            window.blit(lose, (450, 250))

        if scet == 10:
            finish = True
            window.blit(win, (450, 250))

        if sprite.spritecollide(player, monsters, False):
            finish = True
            window.blit(lose, (450, 250))

        bullets_monsters = sprite.groupcollide(bullets, monsters, True, True)
        for monster in bullets_monsters:
            monster228 = Enemy('ufo (1).png', randint(0, 800), 0, randint(1, 3), 130, 100)
            monsters.add(monster228)
            scet += 1

        if sprite.spritecollide(player, metiorits, False):
            finish = True
            window.blit(lose, (450, 250))







    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    player.fire()
                    num_fire += 1
                    bullet_sound.play()
                if num_fire >= 5 and rel_time == False:
                    rel_time = True
                    start = time_module.time()
                    num_fire = 0

    end = time_module.time()
    if int(end - start) < 3:
        reload = font.render('Ждите перезарядку', True, (255, 255, 255))
        window.blit(reload, (370, 750))
    else:
        rel_time = False

    clock.tick(fps)
    display.update()