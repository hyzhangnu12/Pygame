import pygame
import sprites
import random
import os

# static parameters
WIDTH = 500
HEIGHT = 600
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# game init
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("test game")
clock = pygame.time.Clock()

# 
back_img = pygame.image.load(os.path.join("imgs", "space.png")).convert()
ship_img = pygame.image.load(os.path.join("imgs", "ship.png")).convert()
rock_img = pygame.image.load(os.path.join("imgs", "rock.png")).convert()

# roles
players = pygame.sprite.Group()
rocks = pygame.sprite.Group()
bullets = pygame.sprite.Group()

player = sprites.Player((WIDTH / 2, HEIGHT - 40), ship_img)
players.add(player)
for i in range(8):
    rock = sprites.Rock(WIDTH, rock_img)
    rocks.add(rock)


running = True
live = 1000

while running:
    clock.tick(FPS)
     
    # get events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet = player.shoot()
                bullets.add(bullet)
    
    # update status
    players.update(pygame.key.get_pressed(), (0, WIDTH))
    rocks.update(0, WIDTH, HEIGHT)
    bullets.update()
    
    hits = pygame.sprite.groupcollide(rocks, bullets, True, True)
    for _ in hits:
        rock = sprites.Rock(WIDTH, rock_img)
        rocks.add(rock)

    hits = pygame.sprite.spritecollide(player, rocks, False, pygame.sprite.collide_circle)
    live -= len(hits)
    print(len(hits))
    if live < 0:
        running = False

    # display game
    screen.fill(BLACK)
    screen.blit(back_img, (0, 0))
    players.draw(screen)
    rocks.draw(screen)
    bullets.draw(screen)
    pygame.display.update()

pygame.quit()