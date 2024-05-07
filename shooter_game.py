#Создай собственный Шутер!

from pygame import *
import sys
import time as tm
from random import randint
mixer.init()
font.init()

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, x, y, size_x, size_y, speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys_pressed[K_d] and self.rect.x < 700:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet("bullet.png", self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y >= 490:
            self.rect.x = randint(10, 640)
            self.rect.y = 0
            lost += 1
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y == 0:
            self.kill()
class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= 490:
            self.rect.x = randint(10, 640)
            self.rect.y = 0


window = display.set_mode((700, 500))
display.set_caption("Шутер")
background = transform.scale(image.load("galaxy.jpg"), (700, 500))

rocket = Player("rocket.png", 10, 390, 65, 100, 10)

enemies = sprite.Group()
for i in range(5):
    enemy = Enemy("ufo.png", randint(10, 640), 0, 75, 50, randint(1, 3))
    enemies.add(enemy)

asteroids = sprite.Group()
for i in range(randint (1, 2)):
    asteroid = Asteroid("asteroid.png", randint(10, 640), 0, 75, 50, randint(5, 7))
    asteroids.add(asteroid)

bullets = sprite.Group()

num_hearts = 4
hearts = sprite.Group()
heart_x = 500
hearts_list = list()
for i in range(num_hearts):
    heart = GameSprite("heart.png", heart_x, 0, 50, 75, 0)
    hearts_list.append(heart)
    heart_x += 40

mixer.music.load('space.ogg')
mixer.init()
mixer.music.play()
clock = time.Clock()
FPS = 60
game = True
finish = False
lost = 0
wins = 0
font1 = font.SysFont("Calibri", 31)
font2 = font.SysFont("Arial", 70)
shoot = mixer.Sound('new_shoot.ogg')

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
            sys.exit()
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                shoot.play()
                rocket.fire()
            if e.key == K_r:
                for enemy in enemies:
                    enemy.kill()
                for asteroid in asteroids:
                    asteroid.kill()
                for i in range(5):
                    enemy = Enemy("ufo.png", randint(10, 640), 0, 75, 50, randint(1, 3))
                    enemies.add(enemy)
                for i in range(randint (1, 2)):
                    asteroid = Asteroid("asteroid.png", randint(10, 640), 0, 75, 50, randint(5, 7))
                    asteroids.add(asteroid)
                rocket.rect.x = 350
                rocket.rect.y = 400
                num_hearts = 4
                lost = 0 
                heart_x = 500
                for i in range(num_hearts):
                    heart = GameSprite("heart.png", heart_x, 0, 50, 75, 0)
                    hearts_list.append(heart)
                    heart_x += 40
                finish = False
                mixer.music.play()
            if e.key == K_q:
                game = False
    if finish != True:    
        window.blit(background, (0, 0))
        rocket.reset()
        rocket.update()
        enemies.update()
        bullets.update()
        asteroids.update()
        bullets.draw(window)
        enemies.draw(window)
        asteroids.draw(window)
        for i in hearts_list:
            i.reset()

        collides = sprite.groupcollide(enemies, bullets, True, True)
        ast_collides = sprite.groupcollide(asteroids, bullets, False, True)
        for spr in collides:
            wins += 1
            spr.kill()
            enemy = Enemy("ufo.png", randint(10, 640), 0, 75, 50, randint(2, 4))
            enemies.add(enemy)
        rocket_ast = sprite.spritecollide(rocket, asteroids, False)
        rocket_enemies = sprite.spritecollide(rocket, enemies, False)
        if rocket_ast:
            for i in rocket_ast:
                num_hearts -= 1
                i.kill()
                asteroid = Asteroid("asteroid.png", randint(10, 640), 0, 75, 50, randint(5, 7))
                asteroids.add(asteroid)
                if len(hearts_list) > 0:
                    del hearts_list[len(hearts_list)-1]
                else:
                    finish = True
        if wins >= 10:
            finish = True
            win_font = font2.render("YOU WIN!", True, (255, 255, 255))
            window.blit(win_font, (200, 150))
            more_font = font2.render("Хотите сыграть снова? (R/Q)", True, (255, 255, 255))
            window.blit(more_font, (190, 250))
            mixer.music.stop()
        if rocket_enemies:
            num_hearts -= 1
            for i in rocket_enemies:
                i.kill()
                enemy = Enemy("ufo.png", randint(10, 640), 0, 75, 50, randint(2, 4))
                enemies.add(enemy)
            if len(hearts_list) > 0:
                del hearts_list[len(hearts_list)-1]
            else:
                finish = True
        if lost >= 6 or num_hearts <= 0:
            finish = True
            lose_font = font2.render("YOU LOSE!", True, (255, 255, 255))
            window.blit(lose_font, (200, 150))
            more_font = font1.render("Хотите сыграть снова? (R/Q)", True, (255, 255, 255))
            window.blit(more_font, (190, 250))
            mixer.music.stop()
        lost_text = font1.render((("Пропущено:") + str(lost)), 1, (255, 255, 255))
        shots_text = font1.render((("Сбито:") + str(wins)), 1, (255, 255, 255))
        window.blit(lost_text, (5, 5))
        window.blit(shots_text, (5, 40))

    clock.tick(FPS)
    display.update()