'''
Sound wraps pygame and a few other conveniences.
'''
from abc import ABC, abstractmethod
import logging

import pygame


pygame.mixer.init()
# to allow for more than just the actual notes being played
pygame.mixer.set_num_channels(16)


class SoundABC(ABC):

    @abstractmethod
    def play(self, loops):
        pass

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def set_volume(self, volume):
        pass


class Sound(SoundABC):

    # Class-level sound cache to keep memory in-check
    # file_path: <Sound> instance
    _cache_ = {}

    def __init__(self, file_path):
        self.file_path = file_path
        self._sound = None
        self._sound = pygame.mixer.Sound(file_path)
        self._channel = None

    def play(self, loops=-1):
        logging.debug(f'Playing {self.file_path}')
        self._channel = self._sound.play(loops)
        return self._channel

    def stop(self):
        self._sound.stop()

    def set_volume(self, volume):
        self._sound.set_volume(volume)


class SoundStub(SoundABC):

    def __init__(self, file_path):
        self.file_path = file_path

    def play(self, loops=-1):
        return None

    def stop(self):
        return

    def set_volume(self, volume):
        return


_cached_sounds = {}


def get_sound(file_path, sound_class):
    if file_path in _cached_sounds:
        return _cached_sounds[file_path]
    s = sound_class(file_path)
    _cached_sounds[file_path] = s
    return s
