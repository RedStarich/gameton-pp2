import pygame

W = H = 1000

class MainMenu:
  def __init__(self, screen):
    self.screen = screen

    self.is_game_over = False
    self.background = pygame.image.load("assets\\UI\main_menu\main_menu.png")
    self.background_rect = self.background.get_rect()

    self.button_1 = pygame.image.load("assets\\UI\main_menu\play_1.png")
    self.button_1_rect = self.button_1.get_rect()
    self.button_1_rect.topleft = (373, 608)

    self.button_2 = pygame.image.load("assets\\UI\main_menu\play_2.png")
    self.button_2_rect = self.button_2.get_rect()
    self.button_2_rect.topleft = (383, 618)

    self.current_button = 1

    self.is_main_menu = True
  
  def click_button(self):
    self.current_button = 2

  def render(self):
    self.screen.blit(self.background, self.background_rect)
    
    if self.current_button == 1:
      self.screen.blit(self.button_1, self.button_1_rect)
    if self.current_button == 2:
      self.screen.blit(self.button_2, self.button_2_rect)