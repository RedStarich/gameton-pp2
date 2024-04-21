import pygame
from classes.GameMap.GameMap import GameMap

W = H = 1000
TILE_SIZE = 40

class Level5(GameMap):
  def __init__(self, screen):
    super().__init__("assets\map\level_5\\floor.png", screen)
  
  def add_collisions(self, is_candle_available):
    self.add_collision("assets\map\level_5\walls\wall_1.png", 0, 0, "wall")
    self.add_collision("assets\map\level_5\walls\wall_2.png", 16 * TILE_SIZE, 0, "wall")
    self.add_collision("assets\map\level_5\decoration\chair_1.png", 9 * TILE_SIZE, 2 * TILE_SIZE, "wall")
    self.add_collision("assets\map\level_5\decoration\chair_2.png", 9 * TILE_SIZE, 9 * TILE_SIZE, "wall")
    self.add_collision("assets\map\level_5\decoration\chair_3.png", 9 * TILE_SIZE, 16 * TILE_SIZE, "wall")
    self.add_collision("assets\map\level_5\decoration\chair_4.png", 14.75 * TILE_SIZE, 7 * TILE_SIZE, "wall")
    self.add_collision("assets\students\student_3_bottom.png", 9.75 * TILE_SIZE, 6 * TILE_SIZE, "student")
    self.add_collision("assets\students\student_2_top_right.png", 9.5 * TILE_SIZE, 8 * TILE_SIZE, "student")
    self.add_collision("assets\students\student_2_bottom.png", 14.5 * TILE_SIZE, 2 * TILE_SIZE, "student")
    self.add_collision("assets\students\student_1_top_left.png", 14 * TILE_SIZE, 21 * TILE_SIZE, "student")

    if is_candle_available:
      self.add_collision("assets\candles\candle_4.png", 14 * TILE_SIZE, 18.5 * TILE_SIZE, "candle")

  def add_portal(self):
    portal = pygame.Rect(9 * TILE_SIZE, 0, 7 * TILE_SIZE, TILE_SIZE)
    self.portals.append((6, portal, (12 * TILE_SIZE, 22 * TILE_SIZE)))

    portal = pygame.Rect(9 * TILE_SIZE, 24 * TILE_SIZE, 7 * TILE_SIZE, TILE_SIZE)
    self.portals.append((4, portal, (20 * TILE_SIZE, 2 * TILE_SIZE)))