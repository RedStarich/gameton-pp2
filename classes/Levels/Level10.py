import pygame
from classes.GameMap.GameMap import GameMap

W = H = 1000
TILE_SIZE = 40

# Level10 Class
class Level10(GameMap):
  def __init__(self, screen):
    super().__init__("assets\map\level_10\\floor.png", screen)
  
  def add_collisions(self, is_candle_available):
    self.add_collision("assets\map\level_10\walls\wall_1.png", 0, 0, "wall")
    self.add_collision("assets\map\level_10\walls\wall_2.png", 0, 11 * TILE_SIZE, "wall")
    self.add_collision("assets\map\level_10\walls\wall_3.png", 0, 17 * TILE_SIZE, "wall")
    self.add_collision("assets\map\level_10\walls\wall_4.png", 14 * TILE_SIZE, 0, "wall")
    self.add_collision("assets\map\level_10\walls\wall_5.png", 19 * TILE_SIZE, 8 * TILE_SIZE, "wall")
    self.add_collision("assets\map\level_10\walls\wall_6.png", 18 * TILE_SIZE, 11 * TILE_SIZE, "wall")
    self.add_collision("assets\map\level_10\walls\wall_7.png", 21 * TILE_SIZE, 17 * TILE_SIZE, "wall")
    self.add_collision("assets\map\level_10\walls\wall_8.png", 12 * TILE_SIZE, 24 * TILE_SIZE, "wall")
    self.add_collision("assets\map\level_10\walls\wall_9.png", 5 * TILE_SIZE, 24 * TILE_SIZE, "wall")
    self.add_collision("assets\map\level_10\decoration\chair.png", 6 * TILE_SIZE, 17.75 * TILE_SIZE, "wall")
    self.add_collision("assets\map\level_10\decoration\chair.png", 5.75 * TILE_SIZE, 19.1 * TILE_SIZE, "wall")
    self.add_collision("assets\map\level_10\decoration\\table.png", 5 * TILE_SIZE, 17 * TILE_SIZE, "wall")

    if is_candle_available:
      self.add_collision("assets\candles\candle_3.png", 18 * TILE_SIZE, 21 * TILE_SIZE, "candle")

  def add_portal(self, candles_score):
    portal = pygame.Rect(24 * TILE_SIZE, 5 * TILE_SIZE, TILE_SIZE, 3 * TILE_SIZE)
    self.portals.append((9, portal, (3 * TILE_SIZE, 23 * TILE_SIZE)))

    if candles_score == 9:
      portal = pygame.Rect(9 * TILE_SIZE, 24 * TILE_SIZE, 3 * TILE_SIZE, TILE_SIZE)
      self.portals.append((11, portal, (23 * TILE_SIZE, 8 * TILE_SIZE)))