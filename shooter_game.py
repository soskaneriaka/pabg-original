#Создай собственный Шутер!

from pygame import *
from random import randint

background_img = 'galaxy.jpg'
win_width = 700
win_height = 500 
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(background_img), (win_width, win_height))

lost = 0 
score = 0
max_lost = 3

window = display.set_mode((win_width, win_height))
background = transform.scale(image .load(background_img,), (win_width, win_height))

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

font.init()
font2 = font.SysFont('Arial', 40)
win = font2.render('YOU WIN', True, (255, 255, 255))
lose = font2.render('YOU LOSE', True, (100, 0, 0))

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image),(65, 65))
        self.speed = player_speed 
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
        
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > self.speed:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 100:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15)
        bullets.add(bullet)



class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost += 1 

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()        

player = Player('rocket.png', 300, 400, 6)



monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy('ufo.png', randint(80, win_width - 80), -40, randint(1, 5))
    monsters.add(monster)

bullets = sprite.Group()

Player = Player('rocket.png', 300, 400, 10)

monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy('asteroid.png', randint(80, win_width - 80), -40, randint(1, 5))
    monsters.add(monster)

clock = time.Clock()
game = True 
finish = False
FPS = 90


while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()   
                player.fire()

    if not finish:
        window.blit(background, (0, 0))

        text = font2.render("Счёт:"+ str(score),
        1,(255, 255, 255))
        window.blit(text, (10, 20))

        text_lose = font2.render("Пропущено:"+ str(lost),
        1,(255, 255, 255))
        window.blit(text_lose, (10, 50))

        player.update()
        monsters.update()
        bullets.update()

        sprites_list = sprite.groupcollide(monsters, bullets, True, True)

        for c in sprites_list:
            score += 1 
            monster = Enemy('ufo.png', randint(80, win_width - 80), -40, randint(1, 5))
            monsters.add(monster)

        if sprite.spritecollide(player, monsters, False) or lost >= max_lost:
            finish = True
            

        if score >= 10:
            finish = True
            window.blit(win, (200, 200))
   
        player.reset()
        monsters.draw(window)
        bullets.draw(window)


        display.update()

    clock.tick(FPS)

    display.update()