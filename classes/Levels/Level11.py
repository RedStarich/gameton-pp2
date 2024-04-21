import pygame
from classes.GameMap.GameMap import GameMap

W = H = 1000
TILE_SIZE = 40

# Level11 Class
class Level11(GameMap):
  def __init__(self, screen):
    super().__init__("assets\map\level_11\\floor.png", screen)
  
  def add_collisions(self, is_candle_available):
    self.add_collision("assets\map\level_11\walls\wall_1.png", 0, 0, "wall")
    self.add_collision("assets\map\level_11\walls\wall_2.png", 0, 5 * TILE_SIZE, "wall")
    self.add_collision("assets\map\level_11\walls\wall_3.png", 22 * TILE_SIZE, 4 * TILE_SIZE, "wall")
    self.add_collision("assets\map\level_11\walls\wall_4.png", 22 * TILE_SIZE, 10 * TILE_SIZE, "wall")
    self.add_collision("assets\map\level_11\walls\wall_5.png", 3 * TILE_SIZE, 23 * TILE_SIZE, "wall")
    self.add_collision("assets\map\level_11\decoration\\tables_group_1.png", 3 * TILE_SIZE, 10 * TILE_SIZE, "wall")
    self.add_collision("assets\map\level_11\decoration\\tables_group_2.png", 3 * TILE_SIZE, 13 * TILE_SIZE, "wall")
    self.add_collision("assets\map\level_11\decoration\\tables_group_3.png", 3 * TILE_SIZE, 16 * TILE_SIZE, "wall")
    self.add_collision("assets\map\level_11\decoration\\tables_group_4.png", 3 * TILE_SIZE, 19 * TILE_SIZE, "wall")
    self.add_collision("assets\map\level_11\decoration\\tables_group_5.png", 16.2 * TILE_SIZE, 10 * TILE_SIZE, "wall")
    self.add_collision("assets\map\level_11\decoration\\tables_group_6.png", 16.2 * TILE_SIZE, 13 * TILE_SIZE, "wall")
    self.add_collision("assets\map\level_11\decoration\\tables_group_7.png", 16.2 * TILE_SIZE, 16 * TILE_SIZE, "wall")
    self.add_collision("assets\map\level_11\decoration\\tables_group_8.png", 16.2 * TILE_SIZE, 19 * TILE_SIZE, "wall")
    self.add_collision("assets\map\level_11\decoration\\board.png", 3.4 * TILE_SIZE, 5.6 * TILE_SIZE, "wall")
    self.add_collision("assets\map\level_11\decoration\\teachers_table.png", 19 * TILE_SIZE, 6 * TILE_SIZE, "wall")
    self.add_collision("assets\\teacher\Kelgenbayev_Arnur.png", 12 * TILE_SIZE, 7 * TILE_SIZE, "teacher")

  def render_collision(self):
    super().render_collision()
    teacher_image, teacher_rect = self.teacher
    self.add_shadow(teacher_rect)
    self.screen.blit(teacher_image, teacher_rect)

  def add_portal(self):
    """"""