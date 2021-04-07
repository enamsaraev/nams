import pygame

WIDTH = 800
HEIGHT = 640

class Camera:
    def __init__(self, camera, w, h):
      self.camera = camera
      self.state = pygame.Rect(0, 0, w, h)

    def show(self, player):
      return player.rect.move(self.state.topleft)

    def update(self, player):
      self.state = self.camera(self.state, player.rect)

def start_camera(cam, player_rect):
    l, t, _, _ = player_rect
    _, _, w, h = cam
    l = -l + WIDTH/6
    t = -t + HEIGHT/6

    l = min(0, l)
    l = max(-(cam.width - WIDTH), l)
    t = max(-(cam.height - HEIGHT), t)
    t = min(0, t)
    
    return pygame.Rect(l, t, w, h)