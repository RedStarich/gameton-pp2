import pygame
import math
import random
pygame.init()

done = False
clock = pygame.time.Clock()
FPS = 60
W = H = 1000
TILE_SIZE = 40

screen = pygame.display.set_mode((W, H))

# Laser Class
class Laser:
  def __init__(self, x, y):
    self.laser = pygame.image.load("assets\laser\laser.png")
    self.laser = pygame.transform.scale(self.laser, (self.laser.get_width() * 10, self.laser.get_height() * 4))

    self.splash = pygame.image.load("assets\laser\splash.png")
    self.splash = pygame.transform.scale(self.splash, (self.splash.get_width() * 4, self.splash.get_height() * 4))

    self.ray_length = 500
    self.scaled_laser = pygame.transform.scale(self.laser, (self.ray_length, self.laser.get_height()))

    self.rotated_laser = pygame.transform.rotate(self.scaled_laser, 0)
    self.rotated_laser_rect = self.rotated_laser.get_rect()
    self.rotated_laser_rect.center = (250, 250)

    self.rotated_splash = pygame.transform.rotate(self.splash, 0)
    self.rotated_splash_rect = self.rotated_splash.get_rect()

    self.ray_x = x
    self.ray_y = y

    # Laser Ray need a polygon to detect collision
    # Here is the points of that polygon
    self.ray_point_1 = (0, 0)
    self.ray_point_2 = (0, 0)
    self.ray_point_3 = (0, 0)

    self.angle = 0
    self.collision_pos = None

    self.is_visible = True
    self.visibility_delay = 250
    self.last_update = pygame.time.get_ticks()
  
  def move(self, player_pos_x, player_pos_y):
    self.ray_x = player_pos_x
    self.ray_y = player_pos_y
  
    # Finding angle between mouse and initial laser position
    self.angle = get_mouse_angle()

    # Some mathematics to calculate the points of ray according to the angle
    self.ray_point_1 = (self.ray_x + 4.5 * math.cos(math.radians(90 - self.angle)), self.ray_y + 4.5 * 4 * math.sin(math.radians(90 - self.angle)))
    self.ray_point_2 = (self.ray_x - 4.5 * math.cos(math.radians(90 - self.angle)), self.ray_y - 4.5 * 4 * math.sin(math.radians(90 - self.angle)))
    self.ray_point_3 = (self.ray_x + 500 * math.cos(math.radians(self.angle)), self.ray_y - 500 * math.sin(math.radians(self.angle)))

  def make_visible(self):
    current_time = pygame.time.get_ticks()
    if current_time - self.last_update >= self.visibility_delay:
      self.is_visible = True
      self.last_update = current_time

  def render(self):
    # Scaling the laser by length (in order to make it shorter when it collides with object)
    self.scaled_laser = pygame.transform.scale(self.laser, (self.ray_length, self.laser.get_height()))

    # Rotation the laser
    self.rotated_laser = pygame.transform.rotate(self.scaled_laser, self.angle)
    self.rotated_splash = pygame.transform.rotate(self.splash, self.angle)

    self.rotated_laser_rect = self.rotated_laser.get_rect()
    self.rotated_laser_rect.center = (self.ray_x, self.ray_y)

    if self.is_visible:
      screen.blit(self.rotated_laser, self.rotated_laser_rect)
  
  # Collision detection
  def detect_collision(self, rect):
    self.collision_pos = collide_rect_polygon(rect, [self.ray_point_1, self.ray_point_2, self.ray_point_3])

    if self.collision_pos:
      # Some mathematics to calculate the length of the laser according to the point of collision
      self.ray_length = math.sqrt(math.pow(self.collision_pos[1] - self.ray_y, 2) + math.pow(self.collision_pos[0] - self.ray_x, 2)) * 2
    else:
      self.ray_length = 2000

  # Adding laser splash
  def add_splash(self):
    if self.collision_pos:
      self.rotated_splash_rect = self.rotated_splash.get_rect()
      self.rotated_splash_rect.center = self.collision_pos

      if self.is_visible:
        screen.blit(self.rotated_splash, self.rotated_splash_rect)

# Player Class
class Player:
  def __init__(self, x, y):
    self.player = pygame.image.load("assets\player\player_right_1.png")
    self.player = pygame.transform.scale(self.player, (self.player.get_width() * 4, self.player.get_height() * 4))
    self.player_pos_x = x
    self.player_pos_y = y
    self.player_width = 50
    self.player_rect = self.player.get_rect()
    self.player_rect.center = (self.player_pos_x, self.player_pos_y)
    self.player_speed = 5

    # Player movement animation
    self.direction = "right"
    self.is_moving = False
    self.animation_cooldown = 250
    self.frame = 1
    self.last_update = pygame.time.get_ticks()

    self.footstep_audio_1 = pygame.mixer.Sound("assets\\audio\\footstep_1.mp3")
    self.footstep_audio_2 = pygame.mixer.Sound("assets\\audio\\footstep_2.mp3")
    self.footstep_audio_3 = pygame.mixer.Sound("assets\\audio\\footstep_3.mp3")
    self.footstep_audio_1.set_volume(0.5)
    self.footstep_audio_2.set_volume(0.5)
    self.footstep_audio_3.set_volume(0.5)

  def move(self):
    pressed_keys = pygame.key.get_pressed()

    # Detecting collision direction (so player will not move in that direction)
    colliding_obstacle = None
    collision_type = {
      "top": 0,
      "bottom": 0,
      "right": 0,
      "left": 0
    }
    for (obstacle, obstacle_rect) in gameMap.obstacles:
      if pygame.Rect.colliderect(self.player_rect, obstacle_rect):
        colliding_obstacle = obstacle_rect
        if abs(self.player_rect.top - obstacle_rect.bottom) < 5:
          collision_type["top"] = 1
        if abs(self.player_rect.bottom - obstacle_rect.top) < 5:
          collision_type["bottom"] = 1
        if abs(self.player_rect.right - obstacle_rect.left) < 5:
          collision_type["right"] = 1
        if abs(self.player_rect.left - obstacle_rect.right) < 5:
          collision_type["left"] = 1

    if pressed_keys[pygame.K_w]:
      if collision_type["top"]:
        if self.player_pos_y > colliding_obstacle.bottom:
          self.is_moving = False
      else:
        self.is_moving = True
        self.player_pos_y -= self.player_speed
    if pressed_keys[pygame.K_s]:
      if collision_type["bottom"]:
        if self.player_pos_y < colliding_obstacle.top:
          self.is_moving = False
      else:
        self.is_moving = True
        self.player_pos_y += self.player_speed
    if pressed_keys[pygame.K_d]:
      if collision_type["right"]:
        if self.player_pos_y > colliding_obstacle.bottom:
          self.is_moving = False
      else:
        self.is_moving = True
        self.player_pos_x += self.player_speed
    if pressed_keys[pygame.K_a]:
      if collision_type["left"]:
        if self.player_pos_y > colliding_obstacle.bottom:
          self.is_moving = False
      else:
        self.is_moving = True
        self.player_pos_x -= self.player_speed
    if not pressed_keys[pygame.K_w] and not pressed_keys[pygame.K_s] and not pressed_keys[pygame.K_d] and not pressed_keys[pygame.K_a]:
      self.is_moving = False

    # Rotation player accourding to the angle
    angle = get_mouse_angle()
    if 315 <= angle and angle < 360 or 0 <= angle and angle < 45:
      self.direction = "right"
    elif 45 <= angle and angle < 135:
      self.direction = "up"
    elif 145 <= angle and angle < 225:
      self.direction = "left"
    elif 225 <= angle and angle < 315:
      self.direction = "down"

    self.rotate()

  def render(self):
    self.player_rect.center = (self.player_pos_x, self.player_pos_y)
    screen.blit(self.player, self.player_rect)
  
  # Adding shadow
  def add_shadow(self):
    pygame.draw.ellipse(screen, (150, 150, 150), (self.player_rect.centerx - 35, self.player_rect.bottom - 15, 70, 30))
  
  def rotate(self):
    if not self.is_moving:
      self.player = pygame.image.load(f"assets\player\player_{self.direction}.png")
    else:
      # Changing the frame after the cooldown
      current_time = pygame.time.get_ticks()
      if current_time - self.last_update >= self.animation_cooldown:
        self.frame += 1

        rand = random.randint(1, 3)
        
        if rand == 1:
          self.footstep_audio_1.play()
        if rand == 2:
          self.footstep_audio_2.play()
        if rand == 3:
          self.footstep_audio_3.play()

        if self.frame > 2:
          self.frame = 1
        self.last_update = current_time
  
      self.player = pygame.image.load(f"assets\player\player_{self.direction}_{self.frame}.png")
    
    self.player = pygame.transform.scale(self.player, (self.player.get_width() * 4, self.player.get_height() * 4))

# GameMap Class
class GameMap:
  def __init__(self, link):
    self.game_map = pygame.image.load(link)
    self.game_map = pygame.transform.scale(self.game_map, (self.game_map.get_width() * 4, self.game_map.get_height() * 4))
    self.game_map_rect = self.game_map.get_rect()
    self.obstacles = []
    self.students = []
    self.portals = []
  
  def update(self):
    screen.blit(self.game_map, self.game_map_rect)
  
  # Rendering the collision images
  def render_collision(self):
    for (image, rect) in self.obstacles:
      screen.blit(image, rect)
    for (image, rect) in self.students:
      screen.blit(image, rect)

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

# Level1 Class
class Level1(GameMap):
  def __init__(self):
    super().__init__("assets\map\level_1\ground.png")

  def add_collisions(self):
    self.add_collision("assets\map\level_1\walls\wall_1.png", 0, 0, "wall")
    self.add_collision("assets\map\level_1\walls\wall_2.png", 3 * TILE_SIZE, 9 * TILE_SIZE, "wall")
    self.add_collision("assets\map\level_1\walls\wall_3.png", 0, 21 * TILE_SIZE, "wall")
    self.add_collision("assets\map\level_1\walls\wall_4.png", 23 * TILE_SIZE, 13 * TILE_SIZE, "wall")
    self.add_collision("assets\map\level_1\walls\wall_5.png", 23 * TILE_SIZE, 0, "wall")
    self.add_collision("assets\map\level_1\walls\wall_6.png", 3 * TILE_SIZE, 0, "wall")
    self.add_collision("assets\map\level_1\walls\wall_7.png", 0, 9 * TILE_SIZE, "wall")

    self.add_collision("assets\students\student_1.png", 21 * TILE_SIZE, 4 * TILE_SIZE, "student")

    self.add_collision("assets\map\level_1\decoration\\book_shelf.png", 4 * TILE_SIZE, 1 * TILE_SIZE, "wall")
  
  def add_portal(self):
    portal = pygame.Rect(24 * 40, 4 * 40, 40, 5 * 40)
    # pygame.draw.rect(screen, (255, 0, 0), portal, 5)
    self.portals.append((2, portal, (100, 4.5 * 40)))

# Level2 Class
class Level2(GameMap):
  def __init__(self):
    super().__init__("assets\map\level_2\\floor.png")

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

# Level3 Class
class Level3(GameMap):
  def __init__(self):
    super().__init__("assets\map\level_3\\floor.png")

  def add_collisions(self):
    self.add_collision("assets\map\level_3\walls\wall_1.png", 0, 0, "wall")
    self.add_collision("assets\map\level_3\walls\wall_2.png", 0, 5 * TILE_SIZE, "wall")
    self.add_collision("assets\map\level_3\walls\wall_3.png", 17 * TILE_SIZE, 0, "wall")
    self.add_collision("assets\map\level_3\walls\wall_4.png", 21 * TILE_SIZE, 5 * TILE_SIZE, "wall")
    self.add_collision("assets\map\level_3\decoration\chairs.png", 8 * TILE_SIZE, 20 * TILE_SIZE, "wall")
    self.add_collision("assets\map\level_3\decoration\chairs.png", 15 * TILE_SIZE, 20 * TILE_SIZE, "wall")
    self.add_collision("assets\map\level_3\walls\wall_5.png", 0, 21 * TILE_SIZE, "wall")
    self.add_collision("assets\map\level_3\decoration\panini_center.png", 4 * TILE_SIZE, 9 * TILE_SIZE, "wall")
    self.add_collision("assets\students\student_1.png", 5 * TILE_SIZE, 14 * TILE_SIZE, "student")
    self.add_collision("assets\students\student_2.png", 19 * TILE_SIZE, 10 * TILE_SIZE, "student")
    self.add_collision("assets\students\student_3.png", 18 * TILE_SIZE, 12 * TILE_SIZE, "student")
    self.add_collision("assets\students\student_1.png", 19.5 * TILE_SIZE, 13 * TILE_SIZE, "student")
    self.add_collision("assets\students\student_2.png", 19.5 * TILE_SIZE, 19 * TILE_SIZE, "student")
    self.add_collision("assets\students\student_3.png", 6.5 * TILE_SIZE, 19 * TILE_SIZE, "student")
  
  def add_portal(self):
    portal = pygame.Rect(8 * TILE_SIZE, 0, 9 * TILE_SIZE, 40)
    self.portals.append((2, portal, (W // 2, H // 2)))

    portal = pygame.Rect(24 * TILE_SIZE, 15 * TILE_SIZE, TILE_SIZE, 6 * TILE_SIZE)
    self.portals.append((4, portal, (2 * TILE_SIZE, 18 * TILE_SIZE)))

# Level4 Class
class Level4(GameMap):
  def __init__(self):
    super().__init__("assets\map\level_4\\floor.png")

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

class Level5(GameMap):
  def __init__(self):
    super().__init__("assets\map\level_5\\floor.png")
  
  def add_collisions(self):
    self.add_collision("assets\map\level_5\walls\wall_1.png", 0, 0, "wall")
    self.add_collision("assets\map\level_5\walls\wall_2.png", 16 * TILE_SIZE, 0, "wall")
    self.add_collision("assets\map\level_5\decoration\chair_1.png", 9 * TILE_SIZE, 2 * TILE_SIZE, "wall")
    self.add_collision("assets\map\level_5\decoration\chair_2.png", 9 * TILE_SIZE, 9 * TILE_SIZE, "wall")
    self.add_collision("assets\map\level_5\decoration\chair_3.png", 9 * TILE_SIZE, 16 * TILE_SIZE, "wall")
    self.add_collision("assets\students\student_1.png", 9.75 * TILE_SIZE, 6 * TILE_SIZE, "student")
    self.add_collision("assets\students\student_2.png", 9.5 * TILE_SIZE, 8 * TILE_SIZE, "student")
    self.add_collision("assets\students\student_3.png", 14.5 * TILE_SIZE, 2 * TILE_SIZE, "student")
    self.add_collision("assets\students\student_1.png", 14 * TILE_SIZE, 21 * TILE_SIZE, "student")

  def add_portal(self):
    portal = pygame.Rect(9 * TILE_SIZE, 0, 7 * TILE_SIZE, TILE_SIZE)
    self.portals.append((6, portal, (12 * TILE_SIZE, 22 * TILE_SIZE)))

    portal = pygame.Rect(9 * TILE_SIZE, 24 * TILE_SIZE, 7 * TILE_SIZE, TILE_SIZE)
    self.portals.append((4, portal, (20 * TILE_SIZE, 2 * TILE_SIZE)))

class Level6(GameMap):
  def __init__(self):
    super().__init__("assets\map\level_6\\floor.png")
  
  def add_collisions(self):
    self.add_collision("assets\map\level_6\walls\wall_1.png", 4 * TILE_SIZE, 0, "wall")
    self.add_collision("assets\map\level_6\walls\wall_2.png", 0, 15 * TILE_SIZE, "wall")
    self.add_collision("assets\map\level_6\walls\wall_3.png", 16 * TILE_SIZE, 0, "wall")
    self.add_collision("assets\map\level_6\decoration\chair.png", 9 * TILE_SIZE, 20 * TILE_SIZE, "wall")
    self.add_collision("assets\map\level_6\decoration\chair.png", 9 * TILE_SIZE, 3 * TILE_SIZE, "wall")

  def add_portal(self):
    portal = pygame.Rect(0, 8 * TILE_SIZE, 4 * TILE_SIZE, TILE_SIZE)
    self.portals.append((7, portal, (21 * TILE_SIZE, 14 * TILE_SIZE)))

    portal = pygame.Rect(9 * TILE_SIZE, 24 * TILE_SIZE, 7 * TILE_SIZE, TILE_SIZE)
    self.portals.append((5, portal, (12 * TILE_SIZE, 2 * TILE_SIZE)))

class Level7(GameMap):
  def __init__(self):
    super().__init__("assets\map\level_7\\floor.png")
  
  def add_collisions(self):
    self.add_collision("assets\map\level_7\walls\wall_1.png", 0, 0, "wall")
    self.add_collision("assets\map\level_7\walls\wall_2.png", 0, 7 * TILE_SIZE, "wall")
    self.add_collision("assets\map\level_7\walls\wall_3.png", 0, 14 *  TILE_SIZE, "wall")
    self.add_collision("assets\map\level_7\walls\wall_4.png", 0, 16 *  TILE_SIZE, "wall")
    self.add_collision("assets\map\level_7\walls\wall_5.png", 0, 23 *  TILE_SIZE, "wall")
    self.add_collision("assets\map\level_7\walls\wall_6.png", 4 * TILE_SIZE, 0, "wall")
    self.add_collision("assets\map\level_7\walls\wall_7.png", 12 * TILE_SIZE, 0, "wall")
    self.add_collision("assets\map\level_7\walls\wall_8.png", 17 * TILE_SIZE, 0, "wall")
    self.add_collision("assets\map\level_7\walls\wall_9.png", 12 * TILE_SIZE, 13 * TILE_SIZE, "wall")
    self.add_collision("assets\students\student_1.png", 10.5 * TILE_SIZE, 5.5 * TILE_SIZE, "student")
    self.add_collision("assets\students\student_2.png", 4.5 * TILE_SIZE, 14.25 * TILE_SIZE, "student")
    self.add_collision("assets\students\student_3.png", 5.25 * TILE_SIZE, 17 * TILE_SIZE, "student")

  def add_portal(self):
    portal = pygame.Rect(17 * TILE_SIZE, 16 * TILE_SIZE, 8 * TILE_SIZE, TILE_SIZE)
    self.portals.append((6, portal, (2 * TILE_SIZE, 10 * TILE_SIZE)))

    portal = pygame.Rect(4 * TILE_SIZE, 24 * TILE_SIZE, 8 * TILE_SIZE, TILE_SIZE)
    self.portals.append((8, portal, (8 * TILE_SIZE, 2 * TILE_SIZE)))

class Level8(GameMap):
  def __init__(self):
    super().__init__("assets\map\level_8\\floor.png")
  
  def add_collisions(self):
    self.add_collision("assets\map\level_8\walls\wall_1.png", 0, 0, "wall")
    self.add_collision("assets\map\level_8\walls\wall_2.png", 0, 18 * TILE_SIZE, "wall")
    self.add_collision("assets\map\level_8\walls\wall_3.png", 12 * TILE_SIZE, 0, "wall")
    self.add_collision("assets\map\level_8\walls\wall_4.png", 18 * TILE_SIZE, 18 * TILE_SIZE, "wall")
    self.add_collision("assets\students\student_1.png", 12.5 * TILE_SIZE, 10.25 * TILE_SIZE, "student")
    self.add_collision("assets\students\student_2.png", 19.25 * TILE_SIZE, 15.75 * TILE_SIZE, "student")
    self.add_collision("assets\students\student_3.png", 11.25 * TILE_SIZE, 21 * TILE_SIZE, "student")

  def add_portal(self):
    portal = pygame.Rect(7 * TILE_SIZE, 0, 7 * TILE_SIZE, TILE_SIZE)
    self.portals.append((7, portal, (8 * TILE_SIZE, 23 * TILE_SIZE)))

    portal = pygame.Rect(11 * TILE_SIZE, 24 * TILE_SIZE, 7 * TILE_SIZE, TILE_SIZE)
    self.portals.append((9, portal, (12 * TILE_SIZE, 2 * TILE_SIZE)))

class Level9(GameMap):
  def __init__(self):
    super().__init__("assets\map\level_9\\floor.png")
  
  def add_collisions(self):
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
    self.add_collision("assets\students\student_1.png", 15 * TILE_SIZE, 2 * TILE_SIZE, "student")
    self.add_collision("assets\students\student_1.png", 14.75 * TILE_SIZE, 7.5 * TILE_SIZE, "student")
    self.add_collision("assets\students\student_1.png", 15 * TILE_SIZE, 11.5 * TILE_SIZE, "student")
    self.add_collision("assets\students\student_1.png", 14.65 * TILE_SIZE, 16 * TILE_SIZE, "student")
    self.add_collision("assets\students\student_1.png", 6.25 * TILE_SIZE, 13.25 * TILE_SIZE, "student")
    self.add_collision("assets\students\student_1.png", 7  * TILE_SIZE, 22 * TILE_SIZE, "student")
    self.add_collision("assets\students\student_1.png", 14  * TILE_SIZE, 22.25 * TILE_SIZE, "student")

  def add_portal(self):
    portal = pygame.Rect(6 * TILE_SIZE, 0, 12 * TILE_SIZE, TILE_SIZE)
    self.portals.append((8, portal, (14 * TILE_SIZE, 23 * TILE_SIZE)))

    portal = pygame.Rect(0, 21 * TILE_SIZE, TILE_SIZE, 3 * TILE_SIZE)
    self.portals.append((10, portal, (23 * TILE_SIZE, 7 * TILE_SIZE)))

class Level10(GameMap):
  def __init__(self):
    super().__init__("assets\map\level_10\\floor.png")
  
  def add_collisions(self):
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

  def add_portal(self):
    portal = pygame.Rect(24 * TILE_SIZE, 5 * TILE_SIZE, TILE_SIZE, 3 * TILE_SIZE)
    self.portals.append((9, portal, (3 * TILE_SIZE, 23 * TILE_SIZE)))

def get_mouse_angle():
  mousePos = pygame.mouse.get_pos()

  base_vector_len = math.sqrt(math.pow(250, 2))
  mouse_vector_len = math.sqrt(math.pow(mousePos[0] - laser.ray_x, 2) + math.pow(laser.ray_y -mousePos[1], 2))
  dot_product = 250 * (mousePos[0] - laser.ray_x)
  angle = math.degrees(math.acos(dot_product / (base_vector_len * mouse_vector_len)))

  if mousePos[1] >= laser.ray_y:
    angle = 360 - angle
  
  return angle

# Checking collision between two lines
def collideLineLine(P0, P1, Q0, Q1):
  d = (P1[0] - P0[0]) * (Q1[1] - Q0[1]) + (P1[1] - P0[1]) * (Q0[0] - Q1[0]) 
  if d == 0:
    return None
  t = ((Q0[0] - P0[0]) * (Q1[1] - Q0[1]) + (Q0[1] - P0[1]) * (Q0[0] - Q1[0])) / d
  u = ((Q0[0] - P0[0]) * (P1[1] - P0[1]) + (Q0[1] - P0[1]) * (P0[0] - P1[0])) / d

  if 0 <= t <= 2 and 0 <= u <= 1:
    return P1[0] * t + P0[0] * (1 - t), P1[1] * t + P0[1] * (1 - t)

# Checking collision between line and rect
def colide_rect_line(rect, p1, p2):
  angle = get_mouse_angle()

  collision_pos = None
  if 0 <= angle and angle < 180:
    collision_pos = collideLineLine(p1, p2, rect.bottomleft, rect.bottomright)
    if collision_pos:
      return collision_pos
  if 90 <= angle and angle < 270:
    collision_pos = collideLineLine(p1, p2, rect.bottomright, rect.topright)
    if collision_pos:
      return collision_pos
  if 180 <= angle and angle < 360:
    collision_pos = collideLineLine(p1, p2, rect.topright, rect.topleft)
    if collision_pos:
      return collision_pos
  if (270 <= angle and angle < 360) or (0 <= angle and angle < 90):
    collision_pos = collideLineLine(p1, p2, rect.topleft, rect.bottomleft)
    if collision_pos:
      return collision_pos

  return collision_pos

# Checking collision between polygon (laser) and rect (Wall, Student, etc)
def collide_rect_polygon(rect, polygon):
    for i in range(len(polygon)-1):
        collision_pos = colide_rect_line(rect, polygon[i], polygon[i+1])
        if collision_pos:
            return collision_pos
    return None

class Cake:
  def __init__(self, x, y):
    self.cake = pygame.image.load("assets\cake\cake.png")
    self.cake = pygame.transform.scale(self.cake, (self.cake.get_width() * 4, self.cake.get_height() * 4))
    self.cake_rect = self.cake.get_rect()
    self.cake_rect.center = (x, y)

    self.radius = 50
    self.angle = 0

    self.cake_x = x
    self.cake_y = y
  
  def move(self, player_pos_x, player_pos_y):
    self.angle = get_mouse_angle()
    self.cake_x = self.radius * math.cos(math.radians(-self.angle)) + player_pos_x
    self.cake_y = self.radius * math.sin(math.radians(-self.angle)) + player_pos_y

  def render(self):
    self.cake_rect.center = (self.cake_x, self.cake_y)
    screen.blit(self.cake, self.cake_rect)

class GameOverScreen:
  def __init__(self):
    # self.background = pygame.image.load("assets\\UI\lose_screen\lose_screen.png")
    # self.background_rect = self.background.get_rect()
    self.font = pygame.font.Font("assets\\fonts\pixel.ttf", 75)
    self.text = self.font.render("YOU LOSE!!! ;(", True, (255, 255, 255))
  
  def update(self):
    # screen.blit(self.background, self.background_rect)
    screen.blit(self.text, (W / 2 - self.text.get_width() / 2, H / 2 - self.text.get_height() / 2))

# Initializing
current_level = 2

initial_pos_x = W // 2
initial_pos_y = H // 2

player = Player(initial_pos_x, initial_pos_y)
laser = Laser(player.player_pos_x, player.player_pos_y)
cake = Cake(player.player_pos_x, player.player_pos_y)
gameMap = Level2()

game_over_screen = GameOverScreen()

background_music = pygame.mixer.Sound("assets\\audio\\background_music.mp3")
background_music.play(-1)

transition_audio = pygame.mixer.Sound("assets\\audio\\transition.mp3")
transition_audio.set_volume(0.5)
is_transition_audio_playing = False

game_over_audio = pygame.mixer.Sound("assets\\audio\\game_over.mp3")
game_over_audio.set_volume(0.5)
is_game_over_audio_playing = False

# Importing transition
transition = pygame.image.load("assets\\UI\\transition\\transition.png")
transition = pygame.transform.scale(transition, (transition.get_width() * 4, transition.get_height() * 4))
transition_rect = transition.get_rect()
transition_rect.topleft = (W, 0)
transition_x = W
is_transition = False

fl_game_over = False
fl_game_restart = False

# Adding collision detectors to collision objects (Walls, Students, etc)
gameMap.add_collisions()

# Rendering portals to travel between levels
gameMap.add_portal()

def restart():
  global fl_game_over, fl_game_restart, is_game_over_audio_playing, current_level, initial_pos_x, initial_pos_y, player, laser, cake, gameMap

  # Initializing
  current_level = 2

  initial_pos_x = W // 2
  initial_pos_y = H // 2

  player = Player(initial_pos_x, initial_pos_y)
  laser = Laser(player.player_pos_x, player.player_pos_y)
  cake = Cake(player.player_pos_x, player.player_pos_y)
  gameMap = Level2()

  # Adding collision detectors to collision objects (Walls, Students, etc)
  gameMap.add_collisions()

  # Rendering portals to travel between levels
  gameMap.add_portal()

  fl_game_over = False
  fl_game_restart = False

  is_game_over_audio_playing = False

while not done:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      done = True
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_r and fl_game_over:
        is_transition = True
        fl_game_restart = True

  # Drawing map (without collisions)
  gameMap.update()
  
  player.add_shadow()

  # Rendering collision objects (Walls, Students, etc)
  gameMap.render_collision()

  # Priority of layer of laser and player
  if player.direction == "down":
    if not fl_game_over and not is_transition:
      player.move()
      laser.move(player.player_pos_x, player.player_pos_y)
      cake.move(player.player_pos_x, player.player_pos_y)

    player.render()
    laser.render()
    cake.render()
  else:
    if not fl_game_over and not is_transition:
      laser.move(player.player_pos_x, player.player_pos_y)
      cake.move(player.player_pos_x, player.player_pos_y)
      player.move()
  
    laser.render()
    cake.render()
    player.render()
  
  laser.make_visible()
  
  fl_collision = False

  # Search for closest collision of the laser
  closest_collision_distance = 10000
  closest_collision = None
  closest_collision_type = None

  for (obstacle, obstacle_rect) in gameMap.obstacles:
    laser.detect_collision(obstacle_rect)
    ray_length = laser.ray_length
    if ray_length < closest_collision_distance:
      closest_collision_distance = ray_length
      closest_collision = obstacle_rect
      closest_collision_type = "wall"
  for (student, student_rect) in gameMap.students:
    laser.detect_collision(student_rect)
    ray_length = laser.ray_length
    if ray_length < closest_collision_distance:
      closest_collision_distance = ray_length
      closest_collision = student_rect
      closest_collision_type = "student"
  
  if closest_collision:
    if closest_collision_type == "student" and laser.is_visible:
      if not is_game_over_audio_playing:
        game_over_audio.play()
        is_game_over_audio_playing = True
      fl_game_over = True

    laser.detect_collision(closest_collision)
    laser.add_splash()
  
  # Collision detection of portals to travel between levels
  for portal in gameMap.portals:
    if pygame.Rect.colliderect(player.player_rect, portal[1]):
      current_level = portal[0]
      initial_pos_x, initial_pos_y = portal[2]
      is_transition = True
  
  # Transition between levels
  if is_transition:
    if not is_transition_audio_playing:
      transition_audio.play()
      is_transition_audio_playing = True

    transition_x -= 35
    transition_rect.topleft = (transition_x, 0)
    screen.blit(transition, transition_rect)
    spike_width = 140
    if transition_x <= -spike_width:
      player = Player(initial_pos_x, initial_pos_y)
      laser = Laser(initial_pos_x, initial_pos_y)
      cake = Cake(initial_pos_x, initial_pos_y)
      laser.is_visible = False

      if fl_game_over and fl_game_restart:
        restart()

      if current_level == 1:
        gameMap = Level1()
      if current_level == 2:
        gameMap = Level2()
      if current_level == 3:
        gameMap = Level3()
      if current_level == 4:
        gameMap = Level4()
      if current_level == 5:
        gameMap = Level5()
      if current_level == 6:
        gameMap = Level6()
      if current_level == 7:
        gameMap = Level7()
      if current_level == 8:
        gameMap = Level8()
      if current_level == 9:
        gameMap = Level9()
      if current_level == 10:
        gameMap = Level10()

      laser.move(initial_pos_x, initial_pos_y)
      cake.move(initial_pos_y, initial_pos_y)
      gameMap.add_portal()
      gameMap.add_collisions()
    if transition_x <= -(W + 2 * spike_width):
      is_transition_audio_playing = False
      is_transition = False
      transition_x = W

  if fl_game_over:
    game_over_screen.update()

  pygame.display.flip()
  clock.tick(FPS)