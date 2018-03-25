'''
Sound wraps pygame and a few other conveniences.
'''
import pygame


# to allow for more than just the actual notes being played
pygame.mixer.set_num_channels(16)


class Sound():

    def __init__(self, file_path):
        self.file_path = file_path
        self._sound = pygame.mixer.Sound(file_path)
        self._channel = None

    def play(self, loops=-1):
        self._channel = self._sound.play(loops)
        return self._channel

    def stop(self):
        self._sound.stop()

    def set_volume(self, volume):
        self._sound.set_volume(volume)
