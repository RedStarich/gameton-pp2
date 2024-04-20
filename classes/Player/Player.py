import pygame
import random
from functions.getMouseAngle import get_mouse_angle

# Player Class
class Player:
  def __init__(self, x, y, screen, game_map, laser):
    self.screen = screen
  
    self.game_map = game_map
    self.laser = laser
  
    self.player = pygame.image.load("assets\player\player_right_1.png")
    self.player = pygame.transform.scale(self.player, (self.player.get_width() * 4, self.player.get_height() * 4))
    self.player_pos_x = x
    self.player_pos_y = y
    self.player_width = 50
    self.player_rect = self.player.get_rect()
    self.player_rect.center = (self.player_pos_x, self.player_pos_y)
    self.player_speed = 5

    # Player movement animation
    self.direction = "right"
    self.is_moving = False
    self.animation_cooldown = 250
    self.frame = 1
    self.last_update = pygame.time.get_ticks()

    self.footstep_audio_1 = pygame.mixer.Sound("assets\\audio\\footstep_1.mp3")
    self.footstep_audio_2 = pygame.mixer.Sound("assets\\audio\\footstep_2.mp3")
    self.footstep_audio_3 = pygame.mixer.Sound("assets\\audio\\footstep_3.mp3")
    self.footstep_audio_1.set_volume(0.5)
    self.footstep_audio_2.set_volume(0.5)
    self.footstep_audio_3.set_volume(0.5)

  def move(self):
    pressed_keys = pygame.key.get_pressed()

    # Detecting collision direction (so player will not move in that direction)
    colliding_obstacle = None
    collision_type = {
      "top": 0,
      "bottom": 0,
      "right": 0,
      "left": 0
    }
    for (obstacle, obstacle_rect) in self.game_map.obstacles:
      if pygame.Rect.colliderect(self.player_rect, obstacle_rect):
        colliding_obstacle = obstacle_rect
        if abs(self.player_rect.top - obstacle_rect.bottom) < 5:
          collision_type["top"] = 1
        if abs(self.player_rect.bottom - obstacle_rect.top) < 5:
          collision_type["bottom"] = 1
        if abs(self.player_rect.right - obstacle_rect.left) < 5:
          collision_type["right"] = 1
        if abs(self.player_rect.left - obstacle_rect.right) < 5:
          collision_type["left"] = 1

    if pressed_keys[pygame.K_w]:
      if collision_type["top"]:
        if self.player_pos_y > colliding_obstacle.bottom:
          self.is_moving = False
      else:
        self.is_moving = True
        self.player_pos_y -= self.player_speed
    if pressed_keys[pygame.K_s]:
      if collision_type["bottom"]:
        if self.player_pos_y < colliding_obstacle.top:
          self.is_moving = False
      else:
        self.is_moving = True
        self.player_pos_y += self.player_speed
    if pressed_keys[pygame.K_d]:
      if collision_type["right"]:
        if self.player_pos_y > colliding_obstacle.bottom:
          self.is_moving = False
      else:
        self.is_moving = True
        self.player_pos_x += self.player_speed
    if pressed_keys[pygame.K_a]:
      if collision_type["left"]:
        if self.player_pos_y > colliding_obstacle.bottom:
          self.is_moving = False
      else:
        self.is_moving = True
        self.player_pos_x -= self.player_speed
    if not pressed_keys[pygame.K_w] and not pressed_keys[pygame.K_s] and not pressed_keys[pygame.K_d] and not pressed_keys[pygame.K_a]:
      self.is_moving = False

    # Rotation player accourding to the angle
    angle = get_mouse_angle(self.laser)
    if 315 <= angle and angle < 360 or 0 <= angle and angle < 45:
      self.direction = "right"
    elif 45 <= angle and angle < 135:
      self.direction = "up"
    elif 145 <= angle and angle < 225:
      self.direction = "left"
    elif 225 <= angle and angle < 315:
      self.direction = "down"

    self.rotate()

  def render(self):
    self.player_rect.center = (self.player_pos_x, self.player_pos_y)
    self.screen.blit(self.player, self.player_rect)
  
  # Adding shadow
  def add_shadow(self):
    pygame.draw.ellipse(self.screen, (150, 150, 150), (self.player_rect.centerx - 35, self.player_rect.bottom - 15, 70, 30))
  
  def rotate(self):
    if not self.is_moving:
      self.player = pygame.image.load(f"assets\player\player_{self.direction}.png")
    else:
      # Changing the frame after the cooldown
      current_time = pygame.time.get_ticks()
      if current_time - self.last_update >= self.animation_cooldown:
        self.frame += 1

        rand = random.randint(1, 3)
        
        if rand == 1:
          self.footstep_audio_1.play()
        if rand == 2:
          self.footstep_audio_2.play()
        if rand == 3:
          self.footstep_audio_3.play()

        if self.frame > 2:
          self.frame = 1
        self.last_update = current_time
  
      self.player = pygame.image.load(f"assets\player\player_{self.direction}_{self.frame}.png")
    
    self.player = pygame.transform.scale(self.player, (self.player.get_width() * 4, self.player.get_height() * 4))