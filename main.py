#Imports
import pygame, sys
from pygame.locals import *
import random, time
 
#Initialzing 
pygame.init()
 
#Setting up FPS 
FPS = 1
FramePerSec = pygame.time.Clock()
 
#Creating colors
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
 
#Other Variables for use in the program
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1200
SPEED = 5
SCORE = 0
BONUS = 0
 
#Setting up Fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)
restart_msg = font.render("Press 'space' to restart", True, BLACK)
 
#load office background
office_bg = pygame.image.load("office.png")
bg = office_bg

#idle bg
r_hall = pygame.image.load("ab_near.png")
l_hall = pygame.image.load("ab_near.png")

#bg with enemy
r_hall_enemy = pygame.image.load("kb_near.png")
l_hall_enemy = pygame.image.load("kb_near.png")

#bg idle
r_hall_idle = pygame.image.load("ab_near.png")
l_hall_idle = pygame.image.load("ab_near.png")

#Create a white screen 
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")

#enemy position
enemy1_position = 0
enemy2_position = 0
enemy3_position = 0
enemy4_position = 0

#agro level
agro = 1
#timer
curr_time = 0
end_time = 100

def main_menu():
    pass

def options():
    pass

def game():
    pass



running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False
        

    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT]:
        if enemy1_position == -5:
            bg = l_hall_enemy
            enemy1_position = 0
        elif enemy2_position == -5:
            bg = l_hall_enemy
            enemy2_position = 0
        elif enemy3_position == -5:
            bg = l_hall_enemy
            enemy3_position = 0
        elif enemy4_position == -5:
            bg = l_hall_enemy
            enemy4_position = 0
        else:
            bg = l_hall_idle

    elif key[pygame.K_RIGHT]:
        if enemy1_position == 5:
            bg = r_hall_enemy
            enemy1_position = 0
        elif enemy2_position == 5:
            bg = r_hall_enemy
            enemy2_position = 0
        elif enemy3_position == 5:
            bg = r_hall_enemy
            enemy3_position = 0
        elif enemy4_position == 5:
            bg = r_hall_enemy
            enemy4_position = 0
        else:
            bg = r_hall_idle
    else:
        bg = office_bg

    
    DISPLAYSURF.blit(bg, (0,0))

    enemy1_position += random.randint(-1, 1)
    enemy2_position += random.randint(-1, 1)
    enemy3_position += random.randint(-1, 1)
    enemy4_position += random.randint(-1, 1)

    score = font_small.render(str(curr_time), True, BLACK)
    DISPLAYSURF.blit(score, (10,10))

    pygame.display.update()
    FramePerSec.tick(FPS)

pygame.quit()