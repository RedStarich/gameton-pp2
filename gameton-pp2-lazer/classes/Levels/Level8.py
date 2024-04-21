import pygame
from classes.GameMap.GameMap import GameMap

W = H = 1000
TILE_SIZE = 40

class Level8(GameMap):
  def __init__(self, screen):
    super().__init__("assets\map\level_8\\floor.png", screen)
  
  def add_collisions(self):
    self.add_collision("assets\map\level_8\walls\wall_1.png", 0, 0, "wall")
    self.add_collision("assets\map\level_8\walls\wall_2.png", 0, 18 * TILE_SIZE, "wall")
    self.add_collision("assets\map\level_8\walls\wall_3.png", 12 * TILE_SIZE, 0, "wall")
    self.add_collision("assets\map\level_8\walls\wall_4.png", 18 * TILE_SIZE, 18 * TILE_SIZE, "wall")
    self.add_collision("assets\students\student_1.png", 12.5 * TILE_SIZE, 10.25 * TILE_SIZE, "student")
    self.add_collision("assets\students\student_2.png", 19.25 * TILE_SIZE, 15.75 * TILE_SIZE, "student")
    self.add_collision("assets\students\student_3.png", 11.25 * TILE_SIZE, 21 * TILE_SIZE, "student")

  def add_portal(self):
    portal = pygame.Rect(7 * TILE_SIZE, 0, 7 * TILE_SIZE, TILE_SIZE)
    self.portals.append((7, portal, (8 * TILE_SIZE, 23 * TILE_SIZE)))

    portal = pygame.Rect(11 * TILE_SIZE, 24 * TILE_SIZE, 7 * TILE_SIZE, TILE_SIZE)
    self.portals.append((9, portal, (12 * TILE_SIZE, 2 * TILE_SIZE)))