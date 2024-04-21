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

    self.click_sound = pygame.mixer.Sound("assets\\audio\click.mp3")
    
    self.current_button = 1

    self.is_audio_playing = False
    self.game_over_y = H
    self.is_game_over = False
  
  # Change button state if it was clicked
  def click_button(self):
    self.current_button = 2
    self.click_sound.play()

  # Rendering and moving GameOverScreen
  def render(self):
    self.play_audio()

    self.background_rect.top = self.game_over_y
    self.screen.blit(self.background, self.background_rect)

    if self.game_over_y > 35:
      self.game_over_y -= 35
    elif self.game_over_y > 0:
      self.game_over_y = 0

    
    if self.current_button == 1:
      self.screen.blit(self.button_1, self.button_1_rect)
    if self.current_button == 2:
      self.screen.blit(self.button_2, self.button_2_rect)

  def play_audio(self):
    if not self.is_audio_playing:
      self.audio.play()
      self.is_audio_playing = True