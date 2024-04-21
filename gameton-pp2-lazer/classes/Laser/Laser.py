import pygame
import math
from functions.getMouseAngle import get_mouse_angle
from functions.collision import collide_rect_polygon

# Laser Class
class Laser:
  def __init__(self, x, y, screen):
    self.screen = screen
  
    self.laser = pygame.image.load("assets\laser\laser.png")
    self.laser = pygame.transform.scale(self.laser, (self.laser.get_width() * 10, self.laser.get_height() * 4))

    self.splash = pygame.image.load("assets\laser\splash.png")
    self.splash = pygame.transform.scale(self.splash, (self.splash.get_width() * 4, self.splash.get_height() * 4))

    self.ray_length = 500
    self.scaled_laser = pygame.transform.scale(self.laser, (self.ray_length, self.laser.get_height()))

    self.rotated_laser = pygame.transform.rotate(self.scaled_laser, 0)
    self.rotated_laser_rect = self.rotated_laser.get_rect()
    self.rotated_laser_rect.center = (250, 250)

    self.rotated_splash = pygame.transform.rotate(self.splash, 0)
    self.rotated_splash_rect = self.rotated_splash.get_rect()

    self.ray_x = x
    self.ray_y = y

    # Laser Ray need a polygon to detect collision
    # Here is the points of that polygon
    self.ray_point_1 = (0, 0)
    self.ray_point_2 = (0, 0)
    self.ray_point_3 = (0, 0)

    self.angle = 0
    self.collision_pos = None

    self.is_visible = True
    self.visibility_delay = 250
    self.last_update = pygame.time.get_ticks()
  
  def move(self, player_pos_x, player_pos_y):
    self.ray_x = player_pos_x
    self.ray_y = player_pos_y
  
    # Finding angle between mouse and initial laser position
    self.angle = get_mouse_angle(self)

    # Some mathematics to calculate the points of ray according to the angle
    self.ray_point_1 = (self.ray_x + 4.5 * math.cos(math.radians(90 - self.angle)), self.ray_y + 4.5 * 4 * math.sin(math.radians(90 - self.angle)))
    self.ray_point_2 = (self.ray_x - 4.5 * math.cos(math.radians(90 - self.angle)), self.ray_y - 4.5 * 4 * math.sin(math.radians(90 - self.angle)))
    self.ray_point_3 = (self.ray_x + 500 * math.cos(math.radians(self.angle)), self.ray_y - 500 * math.sin(math.radians(self.angle)))

  def make_visible(self):
    current_time = pygame.time.get_ticks()
    if current_time - self.last_update >= self.visibility_delay:
      self.is_visible = True
      self.last_update = current_time

  def render(self):
    # Scaling the laser by length (in order to make it shorter when it collides with object)
    self.scaled_laser = pygame.transform.scale(self.laser, (self.ray_length, self.laser.get_height()))

    # Rotation the laser
    self.rotated_laser = pygame.transform.rotate(self.scaled_laser, self.angle)
    self.rotated_splash = pygame.transform.rotate(self.splash, self.angle)

    self.rotated_laser_rect = self.rotated_laser.get_rect()
    self.rotated_laser_rect.center = (self.ray_x, self.ray_y)

    if self.is_visible:
      self.screen.blit(self.rotated_laser, self.rotated_laser_rect)
  
  # Collision detection
  def detect_collision(self, rect):
    self.collision_pos = collide_rect_polygon(rect, [self.ray_point_1, self.ray_point_2, self.ray_point_3], self)

    if self.collision_pos:
      # Some mathematics to calculate the length of the laser according to the point of collision
      self.ray_length = math.sqrt(math.pow(self.collision_pos[1] - self.ray_y, 2) + math.pow(self.collision_pos[0] - self.ray_x, 2)) * 2
    else:
      self.ray_length = 2000

  # Adding laser splash
  def add_splash(self):
    if self.collision_pos:
      self.rotated_splash_rect = self.rotated_splash.get_rect()
      self.rotated_splash_rect.center = self.collision_pos

      if self.is_visible:
        self.screen.blit(self.rotated_splash, self.rotated_splash_rect)