import pygame
from classes.Laser.Laser import Laser
from classes.Cake.Cake import Cake
from classes.Player.Player import Player
from classes.Levels.Level2 import Level2
from classes.Levels.Level3 import Level3
from classes.Levels.Level4 import Level4
from classes.Levels.Level5 import Level5
from classes.Levels.Level6 import Level6
from classes.Levels.Level7 import Level7
from classes.Levels.Level8 import Level8
from classes.Levels.Level9 import Level9
from classes.Levels.Level10 import Level10
from classes.GameOverScreen.GameOverScreen import GameOverScreen
from classes.MainMenu.MainMenu import MainMenu

pygame.init()

done = False
clock = pygame.time.Clock()
FPS = 60
W = H = 1000
TILE_SIZE = 40

screen = pygame.display.set_mode((W, H))

# Initializing
current_level = 2

initial_pos_x = W // 2
initial_pos_y = H // 2

gameMap = Level2(screen)
laser = Laser(initial_pos_x, initial_pos_y, screen)
player = Player(initial_pos_x, initial_pos_y, screen, gameMap, laser)
cake = Cake(initial_pos_y, initial_pos_y, screen, laser)

game_over_screen = GameOverScreen(screen)
main_menu = MainMenu(screen)

background_music = pygame.mixer.Sound("assets\\audio\\background_music.mp3")
background_music.play(-1)

transition_audio = pygame.mixer.Sound("assets\\audio\\transition.mp3")
transition_audio.set_volume(0.5)
is_transition_audio_playing = False

# Importing transition
transition = pygame.image.load("assets\\UI\\transition\\transition.png")
transition = pygame.transform.scale(transition, (transition.get_width() * 4, transition.get_height() * 4))
transition_rect = transition.get_rect()
transition_rect.topleft = (W, 0)
transition_x = W
is_transition = False

fl_game_restart = False

# Adding collision detectors to collision objects (Walls, Students, etc)
gameMap.add_collisions()

# Rendering portals to travel between levels
gameMap.add_portal()

def restart():
  global fl_game_restart, is_game_over_audio_playing, current_level, initial_pos_x, initial_pos_y, player, laser, cake, gameMap, game_over_screen

  # Initializing
  current_level = 2

  initial_pos_x = W // 2
  initial_pos_y = H // 2

  gameMap = Level2(screen)
  player = Player(initial_pos_x, initial_pos_y,  screen, gameMap, laser)
  laser = Laser(player.player_pos_x, player.player_pos_y, screen)
  cake = Cake(player.player_pos_x, player.player_pos_y, screen, laser)

  # Adding collision detectors to collision objects (Walls, Students, etc)
  gameMap.add_collisions()

  # Rendering portals to travel between levels
  gameMap.add_portal()

  game_over_screen.is_game_over = False
  game_over_screen.is_audio_playing = False
  fl_game_restart = False

while not done:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      done = True
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_r and game_over_screen.is_game_over:
        is_transition = True
        fl_game_restart = True
    if event.type == pygame.MOUSEBUTTONDOWN:
      x, y = pygame.mouse.get_pos()

      if pygame.Rect.collidepoint(main_menu.button_1_rect, x, y) and main_menu.is_main_menu:
        main_menu.click_button()
        is_transition = True

      if pygame.Rect.collidepoint(game_over_screen.button_1_rect, x, y) and game_over_screen.is_game_over:
        game_over_screen.click_button()
        is_transition = True
        fl_game_restart = True

  # Drawing map (without collisions)
  gameMap.update()
  
  player.add_shadow()

  # Rendering collision objects (Walls, Students, etc)
  gameMap.render_collision()

  # Priority of layer of laser and player
  if player.direction == "down":
    if not game_over_screen.is_game_over and not is_transition:
      player.move()
      laser.move(player.player_pos_x, player.player_pos_y)
      cake.move(player.player_pos_x, player.player_pos_y)

    player.render()
    laser.render()
    cake.render()
  else:
    if not game_over_screen.is_game_over and not is_transition:
      laser.move(player.player_pos_x, player.player_pos_y)
      cake.move(player.player_pos_x, player.player_pos_y)
      player.move()
  
    laser.render()
    cake.render()
    player.render()
  
  laser.make_visible()
  
  fl_collision = False

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
  for (student, student_rect) in gameMap.students:
    laser.detect_collision(student_rect)
    ray_length = laser.ray_length
    if ray_length < closest_collision_distance:
      closest_collision_distance = ray_length
      closest_collision = student_rect
      closest_collision_type = "student"
  
  if closest_collision:
    if closest_collision_type == "student" and laser.is_visible:
      game_over_screen.play_audio()
      game_over_screen.is_game_over = True

    laser.detect_collision(closest_collision)
    laser.add_splash()
  
  # Collision detection of portals to travel between levels
  for portal in gameMap.portals:
    if pygame.Rect.colliderect(player.player_rect, portal[1]):
      current_level = portal[0]
      initial_pos_x, initial_pos_y = portal[2]
      is_transition = True

  if main_menu.is_main_menu:
    main_menu.render()

  if game_over_screen.is_game_over:
    game_over_screen.render()

  # Transition between levels
  if is_transition:
    if not is_transition_audio_playing:
      transition_audio.play()
      is_transition_audio_playing = True

    transition_x -= 35
    spike_width = 140
    if transition_x <= -spike_width:
      laser = Laser(initial_pos_x, initial_pos_y, screen)
      player = Player(initial_pos_x, initial_pos_y, screen, gameMap, laser)
      cake = Cake(initial_pos_x, initial_pos_y, screen, laser)

      laser.is_visible = False
      main_menu.is_main_menu = False

      if game_over_screen.is_game_over and fl_game_restart:
        restart()

      # if current_level == 1:
      #   gameMap = Level1()
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

      laser.move(initial_pos_x, initial_pos_y)
      cake.move(initial_pos_x, initial_pos_y)

      gameMap.add_portal()
      gameMap.add_collisions()
    if transition_x <= -(W + 2 * spike_width):
      is_transition_audio_playing = False
      is_transition = False
      transition_x = W

    transition_rect.topleft = (transition_x, 0)
    screen.blit(transition, transition_rect)

  pygame.display.flip()
  clock.tick(FPS)