import pygame
from classes.GameMap.GameMap import GameMap

W = H = 1000
TILE_SIZE = 40

# Level4 Class
class Level4(GameMap):
  def __init__(self, screen):
    super().__init__("assets\map\level_4\\floor.png", screen)

  def add_collisions(self):
    self.add_collision("assets\map\level_4\walls\wall_1.png", 0, 0, "wall")
    self.add_collision("assets\map\level_4\walls\wall_2.png", 9 * TILE_SIZE, 0, "wall")
    self.add_collision("assets\map\level_4\walls\wall_3.png", 23 * TILE_SIZE, 0, "wall")
    self.add_collision("assets\map\level_4\walls\wall_4.png", 15 * TILE_SIZE, 15 * TILE_SIZE, "wall")
    self.add_collision("assets\map\level_4\walls\wall_5.png", 0, 21 * TILE_SIZE, "wall")
    self.add_collision("assets\students\student_1.png", 10 * TILE_SIZE, 10 * TILE_SIZE, "student")
    self.add_collision("assets\students\student_2.png", 21.5 * TILE_SIZE, 12 * TILE_SIZE, "student")
    self.add_collision("assets\students\student_3.png", 21 * TILE_SIZE, 8 * TILE_SIZE, "student")
    self.add_collision("assets\students\student_1.png", 13.5 * TILE_SIZE, 19 * TILE_SIZE, "student")
    self.add_collision("assets\students\student_2.png", 17.5 * TILE_SIZE, 5 * TILE_SIZE, "student")
  
  def add_portal(self):
    portal = pygame.Rect(0, 15 * TILE_SIZE, TILE_SIZE, 6 * TILE_SIZE)
    self.portals.append((3, portal, (23 * TILE_SIZE, 18 * TILE_SIZE)))

    portal = pygame.Rect(17 * TILE_SIZE, 0, 6 * TILE_SIZE, TILE_SIZE)
    self.portals.append((5, portal, (12 * TILE_SIZE, 22 * TILE_SIZE)))