import pygame

# GameMap Class
class GameMap:
  def __init__(self, link, screen):
    self.screen = screen
  
    self.game_map = pygame.image.load(link)
    self.game_map = pygame.transform.scale(self.game_map, (self.game_map.get_width() * 4, self.game_map.get_height() * 4))
    self.game_map_rect = self.game_map.get_rect()
    self.obstacles = []
    self.students = []
    self.portals = []
  
  def update(self):
    self.screen.blit(self.game_map, self.game_map_rect)
  
  # Rendering the collision images
  def render_collision(self):
    for (image, rect) in self.obstacles:
      self.screen.blit(image, rect)
    for (image, rect) in self.students:
      self.screen.blit(image, rect)

  # Adding collision boxes
  def add_collision(self, link, x, y, type):
    collision_obj = pygame.image.load(link)
    collision_obj = pygame.transform.scale(collision_obj, (collision_obj.get_width() * 4, collision_obj.get_height() * 4))
    collision_obj_rect = collision_obj.get_rect()
    collision_obj_rect.topleft = (x, y)

    if type == "wall":
      self.obstacles.append((collision_obj, collision_obj_rect))
    elif type == "student":
      self.students.append((collision_obj, collision_obj_rect))