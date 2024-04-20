import pygame

W = H = 1000

class GameOverScreen:
  def __init__(self, screen):
    self.screen = screen

    self.background = pygame.image.load("assets\\UI\game_over\game_over.png")
    self.background_rect = self.background.get_rect()

    self.button_1 = pygame.image.load("assets\\UI\game_over\\restart_1.png")
    self.button_1_rect = self.button_1.get_rect()
    self.button_1_rect.topleft = (304, 598)

    self.button_2 = pygame.image.load("assets\\UI\game_over\\restart_2.png")
    self.button_2_rect = self.button_2.get_rect()
    self.button_2_rect.topleft = (314, 608)

    self.audio = pygame.mixer.Sound("assets\\audio\\game_over.mp3")
    self.audio.set_volume(0.5)
    
    self.current_button = 1

    self.is_audio_playing = False
    self.is_game_over = False
  
  def click_button(self):
    self.current_button = 2

  def render(self):
    self.screen.blit(self.background, self.background_rect)
    
    if self.current_button == 1:
      self.screen.blit(self.button_1, self.button_1_rect)
    if self.current_button == 2:
      self.screen.blit(self.button_2, self.button_2_rect)

  def play_audio(self):
    if not self.is_audio_playing:
      self.audio.play()
      self.is_audio_playing = True