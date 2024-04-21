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
    self.candles = []
    self.teacher = ()
  
  def update(self):
    self.screen.blit(self.game_map, self.game_map_rect)
  
  # Rendering the collision images
  def render_collision(self):
    for (image, rect) in self.obstacles:
      self.screen.blit(image, rect)
    for (image, rect) in self.students:
      self.add_shadow(rect)
      self.screen.blit(image, rect)
    for (image, rect) in self.candles:
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
    elif type == "candle":
      self.candles.append((collision_obj, collision_obj_rect))
    elif type == "teacher":
      self.teacher = (collision_obj, collision_obj_rect)

  # Adding shadow
  def add_shadow(self, rect):
    shadow = pygame.image.load("assets\player\shadow.png")
    shadow = pygame.transform.scale(shadow, (shadow.get_width() * 4, shadow.get_height() * 4))

    shadow_rect = shadow.get_rect()
    shadow_rect.center = (rect.centerx, rect.bottom)

    self.screen.blit(shadow, shadow_rect)