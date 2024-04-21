#Imports
import pygame, sys
from pygame.locals import *
import random, time

# Import of modules
from classes.Laser.Laser import Laser
from classes.Cake.Cake import Cake
from classes.Player.Player import Player
from classes.GameMap.GameMap import GameMap
from classes.Levels.Level2 import Level2
from classes.Levels.Level3 import Level3
from classes.Levels.Level4 import Level4
from classes.Levels.Level5 import Level5
from classes.Levels.Level6 import Level6
from classes.Levels.Level7 import Level7
from classes.Levels.Level8 import Level8
from classes.Levels.Level9 import Level9
from classes.Levels.Level10 import Level10
from classes.Levels.Level11 import Level11
from classes.GameOverScreen.GameOverScreen import GameOverScreen
from classes.WinScreen.WinScreen import WinScreen
from classes.MainMenu.MainMenu import MainMenu

pygame.init()

# Changing icon and caption of the game
icon = pygame.image.load("assets\icon\icon.png") 
pygame.display.set_icon(icon)
pygame.display.set_caption("X-Day") 

# Constants
FPS = 60
W = H = 1000
TILE_SIZE = 40

# Initializing main variables
done = False
clock = pygame.time.Clock()
screen = pygame.display.set_mode((W, H))
font = pygame.font.Font("assets\\fonts\pixel.ttf", 25)

pygame.mouse.set_cursor(pygame.cursors.broken_x)

current_level = 2

initial_pos_x = W // 2
initial_pos_y = H // 2

gameMap = Level2(screen)
laser = Laser(initial_pos_x, initial_pos_y, screen)
player = Player(initial_pos_x, initial_pos_y, screen, gameMap, laser)
cake = Cake(initial_pos_y, initial_pos_y, screen, laser)

game_over_screen = GameOverScreen(screen)
win_screen = WinScreen(screen)
main_menu = MainMenu(screen)

background_music = pygame.mixer.Sound("assets\\audio\\background_music.mp3")
background_music.play(-1)

transition_audio = pygame.mixer.Sound("assets\\audio\\transition.mp3")
transition_audio.set_volume(0.5)
is_transition_audio_playing = False

candle_audio = pygame.mixer.Sound("assets\\audio\candle_collect.mp3")

# Importing transition
transition = pygame.image.load("assets\\UI\\transition\\transition.png")
transition = pygame.transform.scale(transition, (transition.get_width() * 4, transition.get_height() * 4))
transition_rect = transition.get_rect()
transition_rect.topleft = (W, 0)
transition_x = W
is_transition = False

is_game_restart = False

# List which value at the index shows if candle is collected in order to not to spawn in again
# 0 - collected
# 1 - not collected
available_candles = [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]
candles_score = 0

# Updating and rendering candles score
def update_candles_score():
  candles_text = font.render(f"{candles_score}/9", True, (255, 255, 255))
  candles_icon = pygame.image.load("assets\\UI\candles\candles_icon.png")
  candles_icon = pygame.transform.scale(candles_icon, (candles_icon.get_width() * 2, candles_icon.get_height() * 2))
  candles_icon_rect = candles_icon.get_rect()
  candles_icon_rect.left = 125
  candles_icon_rect.centery = 40

  screen.blit(candles_text, (25, 25))
  screen.blit(candles_icon, candles_icon_rect)

# Adding collision detectors to collision objects (Walls, Students, etc)
gameMap.add_collisions(available_candles[current_level])

# Rendering portals to travel between levels
gameMap.add_portal()

# Restart logic
def restart():
  global is_game_restart, current_level, initial_pos_x, initial_pos_y, player, laser, cake, gameMap, available_candles, candles_score, game_over_screen, background_music

  # Reseting values
  current_level = 2

  initial_pos_x = W // 2
  initial_pos_y = H // 2

  gameMap = Level2(screen)
  player = Player(initial_pos_x, initial_pos_y,  screen, gameMap, laser)
  laser = Laser(player.player_pos_x, player.player_pos_y, screen)
  cake = Cake(player.player_pos_x, player.player_pos_y, screen, laser)

  available_candles = [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]
  candles_score = 0

  gameMap.add_collisions(available_candles[current_level])

  gameMap.add_portal()

  game_over_screen = GameOverScreen(screen)
  game_over_screen.is_audio_playing = False
  is_game_restart = False

  background_music.play(-1)

# Main part
while not done:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      done = True
    if event.type == pygame.MOUSEBUTTONDOWN:
      x, y = pygame.mouse.get_pos()

      # Check if "PLAY!" button in the main menu was clicked
      if pygame.Rect.collidepoint(main_menu.button_1_rect, x, y) and main_menu.is_main_menu:
        main_menu.click_button()
        is_transition = True

      # Check if "RESTART" button in the game over screen was clicked
      if pygame.Rect.collidepoint(game_over_screen.button_1_rect, x, y) and game_over_screen.is_game_over:
        game_over_screen.click_button()
        is_transition = True
        is_game_restart = True

  # Drawing map (without collisions)
  gameMap.update()
  
  # Adding shadow under player
  player.add_shadow()

  # Rendering collision objects (Walls, Students, etc)
  gameMap.render_collision()

  # Priority of layer of laser and player
  if player.direction == "down":
    # Stop moving if
    # 1) Main Menu
    # 2) Game is over
    # 3) Win screen
    # 4) Transition
    if not game_over_screen.is_game_over and not is_transition and not win_screen.is_win and not main_menu.is_main_menu:
      player.move()
      laser.move(player.player_pos_x, player.player_pos_y)
      cake.move(player.player_pos_x, player.player_pos_y)

    player.render()
    laser.render()
    cake.render()
  else:
    # Stop moving if
    # 1) Main Menu
    # 2) Game is over
    # 3) Win screen
    # 4) Transition
    if not game_over_screen.is_game_over and not is_transition and not win_screen.is_win and not main_menu.is_main_menu:
      laser.move(player.player_pos_x, player.player_pos_y)
      cake.move(player.player_pos_x, player.player_pos_y)
      player.move()
  
    laser.render()
    cake.render()
    player.render()
  
  # Make the laser invisible at the Level 11 (Final level, with Kelgenbayev Arnur)
  if current_level != 11:
    laser.make_visible()

  # Detect if player collected candle
  for i in range(len(gameMap.candles)):
    candle_rect = gameMap.candles[i][1]
    if pygame.Rect.colliderect(player.player_rect, candle_rect):
      gameMap.candles.pop(i)
      available_candles[current_level] = 0
      candles_score += 1
      candle_audio.play()
      if current_level == 10 and candles_score == 9:
        gameMap.add_portal(candles_score)
  
  # Detect if player collided with Kelgenbayev Arnur
  if current_level == 11 and not is_transition:
    teacher_rect = gameMap.teacher[1]

    if pygame.Rect.colliderect(player.player_rect, teacher_rect):
      win_screen.is_win = True
      background_music.stop()

  # Search for closest collision of the laser
  closest_collision_distance = 10000
  closest_collision = None
  closest_collision_type = None

  for (obstacle, obstacle_rect) in gameMap.obstacles:
    laser.detect_collision(obstacle_rect)
    ray_length = laser.ray_length
    if ray_length < closest_collision_distance:
      closest_collision_distance = ray_length
      closest_collision = obstacle_rect
      closest_collision_type = "wall"
  for (candle, candle_rect) in gameMap.candles:
    laser.detect_collision(candle_rect)
    ray_length = laser.ray_length
    if ray_length < closest_collision_distance:
      closest_collision_distance = ray_length
      closest_collision = candle_rect
      closest_collision_type = "candle"
  for (student, student_rect) in gameMap.students:
    laser.detect_collision(student_rect)
    ray_length = laser.ray_length
    if ray_length < closest_collision_distance:
      closest_collision_distance = ray_length
      closest_collision = student_rect
      closest_collision_type = "student"
  
  if closest_collision:
    if closest_collision_type == "student" and laser.is_visible:
      game_over_screen.is_game_over = True
      background_music.stop()

    laser.detect_collision(closest_collision)
    laser.add_splash()
  
  # Collision detection of portals to travel between levels
  for portal in gameMap.portals:
    if pygame.Rect.colliderect(player.player_rect, portal[1]):
      current_level = portal[0]
      initial_pos_x, initial_pos_y = portal[2]
      is_transition = True

  update_candles_score()

  # Rendering UI screens
  if main_menu.is_main_menu:
    main_menu.render()

  if game_over_screen.is_game_over:
    game_over_screen.render()

  if win_screen.is_win:
    done = True

  if current_level == 11:
    laser.is_visible = False

  # Transition between levels
  if is_transition:
    if not is_transition_audio_playing:
      transition_audio.play()
      is_transition_audio_playing = True

    transition_x -= 35
    spike_width = 140
    
    if transition_x <= -spike_width:
      # Actions if Transition fully covered screen
      laser = Laser(initial_pos_x, initial_pos_y, screen)
      player = Player(initial_pos_x, initial_pos_y, screen, gameMap, laser)
      cake = Cake(initial_pos_x, initial_pos_y, screen, laser)

      laser.is_visible = False
      main_menu.is_main_menu = False

      if game_over_screen.is_game_over and is_game_restart:
        restart()

      if current_level == 2:
        gameMap = Level2(screen)
      if current_level == 3:
        gameMap = Level3(screen)
      if current_level == 4:
        gameMap = Level4(screen)
      if current_level == 5:
        gameMap = Level5(screen)
      if current_level == 6:
        gameMap = Level6(screen)
      if current_level == 7:
        gameMap = Level7(screen)
      if current_level == 8:
        gameMap = Level8(screen)
      if current_level == 9:
        gameMap = Level9(screen)
      if current_level == 10:
        gameMap = Level10(screen)
      if current_level == 11:
        gameMap = Level11(screen)

      laser.move(initial_pos_x, initial_pos_y)
      cake.move(initial_pos_x, initial_pos_y)

      if current_level == 10:
        gameMap.add_portal(current_level)
      else:
        gameMap.add_portal()
      gameMap.add_collisions(available_candles[current_level])
    if transition_x <= -(W + 2 * spike_width):
      # Actions if Transition fully left screen
      is_transition_audio_playing = False
      is_transition = False
      transition_x = W

    transition_rect.topleft = (transition_x, 0)
    screen.blit(transition, transition_rect)

  pygame.display.flip()
  clock.tick(FPS)
 
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
winscreen = pygame.image.load("assets/UI/win_screen/win_screen.png")

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
sound = pygame.mixer.Sound("assets\\audio\win.mp3")
sound.play()

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