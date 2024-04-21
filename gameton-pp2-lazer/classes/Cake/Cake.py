import pygame
import math
from functions.getMouseAngle import get_mouse_angle

class Cake:
  def __init__(self, x, y, screen, laser):
    self.screen = screen
    self.laser = laser
  
    self.cake = pygame.image.load("assets\cake\cake.png")
    self.cake = pygame.transform.scale(self.cake, (self.cake.get_width() * 4, self.cake.get_height() * 4))
    self.cake_rect = self.cake.get_rect()
    self.cake_rect.center = (x, y)

    self.radius = 50
    self.angle = 0

    self.cake_x = x
    self.cake_y = y
  
  def move(self, player_pos_x, player_pos_y):
    self.angle = get_mouse_angle(self.laser)
    self.cake_x = self.radius * math.cos(math.radians(-self.angle)) + player_pos_x
    self.cake_y = self.radius * math.sin(math.radians(-self.angle)) + player_pos_y

  def render(self):
    self.cake_rect.center = (self.cake_x, self.cake_y)
    self.screen.blit(self.cake, self.cake_rect)