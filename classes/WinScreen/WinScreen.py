import pygame

W = H = 1000

class WinScreen:
  def __init__(self, screen):
    self.screen = screen

    self.background = pygame.image.load("assets\\UI\win_screen\win_screen.png")
    self.background_rect = self.background.get_rect()
    self.background_rect.top = H

    self.audio = pygame.mixer.Sound("assets\\audio\win.mp3")
    self.audio.set_volume(0.5)

    self.is_audio_playing = False
    self.win_y = H
    self.is_win = False

  # Rendering and moving WinScreen
  def render(self):
    self.play_audio()

    self.background_rect.top = self.win_y
    self.screen.blit(self.background, self.background_rect)

    if self.win_y > 0:
      self.win_y -= 35

  def play_audio(self):
    if not self.is_audio_playing:
      self.audio.play()
      self.is_audio_playing = True