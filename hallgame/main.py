#Imports
import pygame, sys
from pygame.locals import *
import random, time
 
#Initialzing 
pygame.init()
 
#Setting up FPS 
FPS = 3
FramePerSec = pygame.time.Clock()
 
#Creating colors
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
 
#Other Variables for use in the program
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
SPEED = 5
SCORE = 0
BONUS = 0
 
#Setting up Fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)
restart_msg = font.render("Press 'space' to restart", True, BLACK)
 
#load office background
office_bg = pygame.image.load("assets\halls\office.png")
bg = office_bg
winscreen = pygame.image.load("assets\general\win.png")

#idle bg
kb = pygame.image.load("assets\halls\kb.png")
pf = pygame.image.load("assets\halls\pf.png")

#altair positions
far_altair = pygame.image.load("assets/altair/far.png")
mid_altair = pygame.image.load("assets/altair/mid.png")
close_altair = pygame.image.load("assets/altair/close.png")
mid_leave_altair = pygame.image.load("assets/altair/mid_leave.png")
far_leave_altair = pygame.image.load("assets/altair/far_leave.png")

altair = [kb, far_altair, mid_altair, close_altair, mid_leave_altair, far_leave_altair]

#daniyar positions
far_dan = pygame.image.load("assets/daniyar/far.png")
mid_dan = pygame.image.load("assets/daniyar/mid.png")
close_dan = pygame.image.load("assets/daniyar/close.png")
mid_leave_dan = pygame.image.load("assets/daniyar/mid_leave.png")
far_leave_dan = pygame.image.load("assets/daniyar/far_leave.png")

daniyar = [kb, far_dan, mid_dan, close_dan, mid_leave_dan, far_leave_dan]

characters = [altair, altair, altair, altair, altair]

character = 0
character_position = 0

#Create a white screen 
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")


#timer
curr_time = 0
end_time = 100
delayer = 0


running = True
winning = False
pygame.mixer.music.set_volume(0.2)
pygame.mixer.Sound('assets/music/bgsong.mp3').play()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False
        

    if character >= len(characters):
        bg = winscreen
    else:
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE] and character_position == 3:
            pygame.mixer.music.set_volume(0.01)
            pygame.mixer.Sound('assets/music/ypi.mp3').play()
            SCORE += 1
            character_position = 0
            character += 1


        if key[pygame.K_LEFT]:
            if character_position > 3 and character_position <= 5:
                bg = characters[character][character_position]
            else:
                bg = pf

        elif key[pygame.K_RIGHT]:
            if character_position > 5:
                character_position = 0

            if character_position < 3 and character < len(characters):
                bg = characters[character][character_position]
            else:
                bg = kb
        else:
            if character_position != 3:
                bg = office_bg
            else:
                if character < len(characters):
                    bg = characters[character][character_position]

        if character_position > 5:
            character_position = 0
        
        if delayer%5==0:
            character_position += 1
            delayer = 1
        delayer += 1

        



    DISPLAYSURF.blit(bg, (0,0))
    score = font_small.render(str(SCORE), True, WHITE)
    DISPLAYSURF.blit(score, (10,10))

    pygame.display.update()
    FramePerSec.tick(FPS)

pygame.quit()