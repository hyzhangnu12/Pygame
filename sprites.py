import pygame
import random
import os

class Player(pygame.sprite.Sprite):
    def __init__(self, init_p, ship_img, speedx = 8):
        super(Player, self).__init__()
        self.image = pygame.transform.scale(ship_img, (50, 104))
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.radius = 25
        self.rect.center = init_p
        self.speedx = speedx

    def update(self, key_pressed, rangex):
        if key_pressed[pygame.K_RIGHT]:
            self.rect.x += self.speedx
        if key_pressed[pygame.K_LEFT]:
            self.rect.x -= self.speedx
        if self.rect.left > rangex[1]:
            self.rect.right = rangex[0]
        if self.rect.right < rangex[0]:
            self.rect.left = rangex[1]

    def shoot(self):
        return Bullet(self.rect.centerx, self.rect.top)

class Rock(pygame.sprite.Sprite):
    def __init__(self, width, rock_img):
        super(Rock, self).__init__()
        size = random.randrange(2, 13)
        self.image_ori = pygame.transform.scale(rock_img, (int(5 * size), int(5 * size)))
        self.image_ori.set_colorkey((255, 255, 255))
        self.image = self.image_ori.copy()
        self.rect = self.image.get_rect()
        self.radius = 25
        self._set_p(width)
        self.total_degree = 0
        self.rot_degree = random.randrange(-5, 5)

    def rotate(self):
        self.total_degree = (self.total_degree + self.rot_degree) % 360
        self.image = pygame.transform.rotate(self.image_ori, self.total_degree)
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center
    
    def update(self, x0, x1, y1):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.right < x0 or self.rect.left > x1 or self.rect.top > y1:
            self._set_p(x1)
    
    def _set_p(self, width):
        self.rect.x = random.randrange(0, width - 30)
        self.rect.y = random.randrange(-100, -40)
        self.speedx = random.randrange(-3, 3)
        self.speedy = random.randrange(2, 10)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, speedy=-10):
        super(Bullet, self).__init__()
        self.image = pygame.Surface((10, 20))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = speedy
    
    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()
        