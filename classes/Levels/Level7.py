import pygame
from classes.GameMap.GameMap import GameMap

W = H = 1000
TILE_SIZE = 40

class Level7(GameMap):
  def __init__(self, screen):
    super().__init__("assets\map\level_7\\floor.png", screen)
  
  def add_collisions(self, is_candle_available):
    self.add_collision("assets\map\level_7\walls\wall_1.png", 0, 0, "wall")
    self.add_collision("assets\map\level_7\walls\wall_2.png", 0, 7 * TILE_SIZE, "wall")
    self.add_collision("assets\map\level_7\walls\wall_3.png", 0, 14 *  TILE_SIZE, "wall")
    self.add_collision("assets\map\level_7\walls\wall_4.png", 0, 16 *  TILE_SIZE, "wall")
    self.add_collision("assets\map\level_7\walls\wall_5.png", 0, 23 *  TILE_SIZE, "wall")
    self.add_collision("assets\map\level_7\walls\wall_6.png", 4 * TILE_SIZE, 0, "wall")
    self.add_collision("assets\map\level_7\walls\wall_7.png", 12 * TILE_SIZE, 0, "wall")
    self.add_collision("assets\map\level_7\walls\wall_8.png", 17 * TILE_SIZE, 0, "wall")
    self.add_collision("assets\map\level_7\walls\wall_9.png", 12 * TILE_SIZE, 13 * TILE_SIZE, "wall")
    self.add_collision("assets\students\student_1_bottom.png", 10.5 * TILE_SIZE, 5.5 * TILE_SIZE, "student")
    self.add_collision("assets\students\student_2_bottom.png", 4.5 * TILE_SIZE, 14.25 * TILE_SIZE, "student")
    self.add_collision("assets\students\student_1_top.png", 5.25 * TILE_SIZE, 17 * TILE_SIZE, "student")

    if is_candle_available:
      self.add_collision("assets\candles\candle_2.png", 4.5 * TILE_SIZE, 5.25 * TILE_SIZE, "candle")

  def add_portal(self):
    portal = pygame.Rect(17 * TILE_SIZE, 16 * TILE_SIZE, 8 * TILE_SIZE, TILE_SIZE)
    self.portals.append((6, portal, (2 * TILE_SIZE, 10 * TILE_SIZE)))

    portal = pygame.Rect(4 * TILE_SIZE, 24 * TILE_SIZE, 8 * TILE_SIZE, TILE_SIZE)
    self.portals.append((8, portal, (8 * TILE_SIZE, 2 * TILE_SIZE)))