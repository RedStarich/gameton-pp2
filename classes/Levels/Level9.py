import pygame
from classes.GameMap.GameMap import GameMap

W = H = 1000
TILE_SIZE = 40

class Level9(GameMap):
  def __init__(self, screen):
    super().__init__("assets\map\level_9\\floor.png", screen)
  
  def add_collisions(self, is_candle_available):
    self.add_collision("assets\map\level_9\walls\wall_1.png", 0, 0, "wall")
    self.add_collision("assets\map\level_9\walls\wall_2.png", 0, 5 * TILE_SIZE, "wall")
    self.add_collision("assets\map\level_9\walls\wall_3.png", 0, 13 * TILE_SIZE, "wall")
    self.add_collision("assets\map\level_9\walls\wall_4.png", 18 * TILE_SIZE, 0, "wall")
    self.add_collision("assets\map\level_9\walls\wall_5.png", 0, 24 * TILE_SIZE, "wall")
    self.add_collision("assets\map\level_9\decoration\chair_1.png", 16 * TILE_SIZE, 4 * TILE_SIZE, "wall")
    self.add_collision("assets\map\level_9\decoration\chair_1.png", 16 * TILE_SIZE, 5.75 * TILE_SIZE, "wall")
    self.add_collision("assets\map\level_9\decoration\chair_1.png", 16 * TILE_SIZE, 9 * TILE_SIZE, "wall")
    self.add_collision("assets\map\level_9\decoration\chair_1.png", 16 * TILE_SIZE, 14 * TILE_SIZE, "wall")
    self.add_collision("assets\map\level_9\decoration\chair_1.png", 16 * TILE_SIZE, 17 * TILE_SIZE, "wall")
    self.add_collision("assets\map\level_9\decoration\chair_2.png", 7 * TILE_SIZE, 15.2 * TILE_SIZE, "wall")
    self.add_collision("assets\map\level_9\decoration\chair_2.png", 6.75 * TILE_SIZE, 17 * TILE_SIZE, "wall")
    self.add_collision("assets\map\level_9\decoration\\table_1.png", 16.75 * TILE_SIZE, 0, "wall")
    self.add_collision("assets\map\level_9\decoration\\table_2.png", 6 * TILE_SIZE, 15 * TILE_SIZE, "wall")
    self.add_collision("assets\students\student_3_bottom.png", 15 * TILE_SIZE, 2 * TILE_SIZE, "student")
    self.add_collision("assets\students\student_2_top_right.png", 14.75 * TILE_SIZE, 7.5 * TILE_SIZE, "student")
    self.add_collision("assets\students\student_1_bottom_right.png", 15 * TILE_SIZE, 11.5 * TILE_SIZE, "student")
    self.add_collision("assets\students\student_1_right.png", 14.65 * TILE_SIZE, 16 * TILE_SIZE, "student")
    self.add_collision("assets\students\student_2_bottom.png", 6.25 * TILE_SIZE, 13.25 * TILE_SIZE, "student")
    self.add_collision("assets\students\student_1_top.png", 7  * TILE_SIZE, 22 * TILE_SIZE, "student")
    self.add_collision("assets\students\student_1_top_left.png", 14  * TILE_SIZE, 22.25 * TILE_SIZE, "student")
    
    if is_candle_available:
      self.add_collision("assets\candles\candle_2.png", 17 * TILE_SIZE, 22 * TILE_SIZE, "candle")

  def add_portal(self):
    portal = pygame.Rect(6 * TILE_SIZE, 0, 12 * TILE_SIZE, TILE_SIZE)
    self.portals.append((8, portal, (14 * TILE_SIZE, 23 * TILE_SIZE)))

    portal = pygame.Rect(0, 21 * TILE_SIZE, TILE_SIZE, 3 * TILE_SIZE)
    self.portals.append((10, portal, (23 * TILE_SIZE, 7 * TILE_SIZE)))