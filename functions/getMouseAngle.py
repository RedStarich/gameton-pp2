import pygame
import math

def get_mouse_angle(laser):
  mousePos = pygame.mouse.get_pos()

  base_vector_len = math.sqrt(math.pow(250, 2))
  mouse_vector_len = math.sqrt(math.pow(mousePos[0] - laser.ray_x, 2) + math.pow(laser.ray_y -mousePos[1], 2))
  dot_product = 250 * (mousePos[0] - laser.ray_x)
  angle = math.degrees(math.acos(dot_product / (base_vector_len * mouse_vector_len)))

  if mousePos[1] >= laser.ray_y:
    angle = 360 - angle
  
  return angle