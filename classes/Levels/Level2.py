import pygame
from classes.GameMap.GameMap import GameMap

W = H = 1000
TILE_SIZE = 40

# Level2 Class
class Level2(GameMap):
  def __init__(self, screen):
    super().__init__("assets\map\level_2\\floor.png", screen)

  def add_collisions(self):
    self.add_collision("assets\map\level_2\walls\wall_1.png", 0, 0, "wall")
    self.add_collision("assets\map\level_2\walls\wall_2.png", 17 * TILE_SIZE, 0, "wall")
    self.add_collision("assets\map\level_2\decoration\chair.png", 4 * TILE_SIZE, 15 * TILE_SIZE, "wall")
    self.add_collision("assets\map\level_2\decoration\chair.png", 7 * TILE_SIZE, 15.5 * TILE_SIZE, "wall")
    self.add_collision("assets\map\level_2\decoration\chair.png", 9.5 * TILE_SIZE, 15.3 * TILE_SIZE, "wall")
    self.add_collision("assets\map\level_2\decoration\chair.png", 13 * TILE_SIZE, 14.5 * TILE_SIZE, "wall")
    self.add_collision("assets\map\level_2\decoration\chair.png", 15 * TILE_SIZE, 15.7 * TILE_SIZE, "wall")
    self.add_collision("assets\map\level_2\decoration\chair.png", 19 * TILE_SIZE, 15 * TILE_SIZE, "wall")
    self.add_collision("assets\map\level_2\decoration\\tables.png", 3 * TILE_SIZE, 16.5 * TILE_SIZE, "wall")
    self.add_collision("assets\map\level_2\walls\wall_3.png", 0, 17 * TILE_SIZE, "wall")
  
  def add_portal(self):
    portal = pygame.Rect(8 * TILE_SIZE, 0, 9 * TILE_SIZE, 40)
    # pygame.draw.rect(screen, (255, 0, 0), portal, 5)
    self.portals.append((3, portal, (W // 2, H // 2)))