'''
Button related implementations.
'''


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


def button_deltas(active_buttons, pressed_buttons):
    '''
    Calculate the buttons to kill and the buttons to activate given active
    buttons and pressed buttons.
    '''
    kill = active_buttons.difference(pressed_buttons)
    start = pressed_buttons.difference(active_buttons)
    return start, kill
