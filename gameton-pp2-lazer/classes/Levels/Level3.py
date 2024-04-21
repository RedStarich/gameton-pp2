import pygame
from classes.GameMap.GameMap import GameMap

W = H = 1000
TILE_SIZE = 40

# Level3 Class
class Level3(GameMap):
  def __init__(self, screen):
    super().__init__("assets\map\level_3\\floor.png", screen)

  def add_collisions(self, is_candle_available):
    self.add_collision("assets\map\level_3\walls\wall_1.png", 0, 0, "wall")
    self.add_collision("assets\map\level_3\walls\wall_2.png", 0, 5 * TILE_SIZE, "wall")
    self.add_collision("assets\map\level_3\walls\wall_3.png", 17 * TILE_SIZE, 0, "wall")
    self.add_collision("assets\map\level_3\walls\wall_4.png", 21 * TILE_SIZE, 5 * TILE_SIZE, "wall")
    self.add_collision("assets\map\level_3\decoration\chairs.png", 8 * TILE_SIZE, 20 * TILE_SIZE, "wall")
    self.add_collision("assets\map\level_3\decoration\chairs.png", 15 * TILE_SIZE, 20 * TILE_SIZE, "wall")
    self.add_collision("assets\map\level_3\walls\wall_5.png", 0, 21 * TILE_SIZE, "wall")
    self.add_collision("assets\map\level_3\decoration\panini_center.png", 4 * TILE_SIZE, 9 * TILE_SIZE, "wall")
    self.add_collision("assets\students\student_1_bottom.png", 5 * TILE_SIZE, 14 * TILE_SIZE, "student")
    self.add_collision("assets\students\student_2_bottom.png", 19 * TILE_SIZE, 10 * TILE_SIZE, "student")
    self.add_collision("assets\students\student_1_bottom_right.png", 18 * TILE_SIZE, 12 * TILE_SIZE, "student")
    self.add_collision("assets\students\student_1_top_left.png", 19.5 * TILE_SIZE, 13 * TILE_SIZE, "student")
    self.add_collision("assets\students\student_1_top.png", 19.5 * TILE_SIZE, 19 * TILE_SIZE, "student")
    self.add_collision("assets\students\student_1_top_right.png", 6.5 * TILE_SIZE, 19 * TILE_SIZE, "student")

    if is_candle_available:
      self.add_collision("assets\candles\candle_2.png", 1.5 * TILE_SIZE, 19 * TILE_SIZE, "candle")
  
  def add_portal(self):
    portal = pygame.Rect(8 * TILE_SIZE, 0, 9 * TILE_SIZE, 40)
    self.portals.append((2, portal, (W // 2, H // 2)))

    portal = pygame.Rect(24 * TILE_SIZE, 15 * TILE_SIZE, TILE_SIZE, 6 * TILE_SIZE)
    self.portals.append((4, portal, (2 * TILE_SIZE, 18 * TILE_SIZE)))