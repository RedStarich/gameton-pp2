import pygame
from classes.GameMap.GameMap import GameMap

W = H = 1000
TILE_SIZE = 40

class Level6(GameMap):
  def __init__(self, screen):
    super().__init__("assets\map\level_6\\floor.png", screen)
  
  def add_collisions(self):
    self.add_collision("assets\map\level_6\walls\wall_1.png", 4 * TILE_SIZE, 0, "wall")
    self.add_collision("assets\map\level_6\walls\wall_2.png", 0, 15 * TILE_SIZE, "wall")
    self.add_collision("assets\map\level_6\walls\wall_3.png", 16 * TILE_SIZE, 0, "wall")
    self.add_collision("assets\map\level_6\decoration\chair.png", 9 * TILE_SIZE, 20 * TILE_SIZE, "wall")
    self.add_collision("assets\map\level_6\decoration\chair.png", 9 * TILE_SIZE, 3 * TILE_SIZE, "wall")

  def add_portal(self):
    portal = pygame.Rect(0, 8 * TILE_SIZE, 4 * TILE_SIZE, TILE_SIZE)
    self.portals.append((7, portal, (21 * TILE_SIZE, 14 * TILE_SIZE)))

    portal = pygame.Rect(9 * TILE_SIZE, 24 * TILE_SIZE, 7 * TILE_SIZE, TILE_SIZE)
    self.portals.append((5, portal, (12 * TILE_SIZE, 2 * TILE_SIZE)))