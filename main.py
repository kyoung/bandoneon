'''
Bandoneon main application.
'''
import pygame


class Button():
    '''
    A button is one of the 72 keys on the bandoneon. Each button may have
    a different tone depending on whether the bandoneon is being opened or
    closed.
    '''

    def __init__(self, key_number, open_value, closed_value):
        self.key_number = key_number
        self.open_value = open_value
        self.closed_value = closed_value

    def get_file(self, bellows_value):
        if bellows_value >= 0:
            return f'/path/to/sound/file/{self.closed_value}'
        return f'/path/to/sound/file/{self.open_value}'


def get_current_buttons_pushed():
    '''
    Measures "depressed buttons" and returns the set of selected Buttons.
    '''
    return set()


def get_current_bellows_value():
    '''
    Returns a reading from the bellows mechanism, ranging from -127 to 127 to
    indicate the pressure and direction of the bandoneon.
    '''
    return 0


def button_deltas(active_buttons, pressed_buttons):
    '''
    Calculate the buttons to kill and the buttons to activate given active
    buttons and pressed buttons.
    '''
    kill = active_buttons.difference(pressed_buttons)
    start = pressed_buttons.difference(active_buttons)
    return start, kill


def start_loop():
    '''
    Main program loop. Read from input buttons and bellows value, evaluate
    current volume and adjust accordingly.
    '''
    # <Button> to <pygame.mixer.Sound> mapping
    active_buttons = {}

    # - to + number indicating whether the bellows is opening or closing,
    # and at what pressure
    bellows_value = 0

    # to allow for more than just the actual notes being played
    pygame.mixer.set_num_channels(16)

    while True:
        current_bttns = get_current_buttons_pushed()
        current_bellows_value = get_current_bellows_value()
        buttons_to_start, buttons_to_kill = button_deltas(
            set(active_buttons.keys()),
            current_bttns)
        for bttn in buttons_to_kill:
            active_buttons[bttn].stop()
            del active_buttons[bttn]
        for bttn in buttons_to_start:
            sound = pygame.mixer.Sound(bttn.get_file(bellows_value))
            active_buttons[bttn] = sound
            _ = sound.play(loops=-1)


if __name__ == '__main__':
    start_loop()
