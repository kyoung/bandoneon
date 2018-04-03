'''
Button related implementations.
'''
import os
import random
import re


_RE_HELMHOLTZ = re.compile('^([a-gA-G]#?)(`*)$')
_note_map = {
    'C': 0, 'C#': 1,
    'D': 2, 'D#': 3,
    'E': 4,
    'F': 5, 'F#': 6,
    'G': 7, 'G#': 8,
    'A': 9, 'A#': 10,
    'B': 11
}

_VIRTUAL = 'virtual'
_IC2 = 'ic2'
_KEY_MODE = os.getenv('BANDONEON_BUTTONS', _VIRTUAL)

_VIRTUAL_BUTTONS_FILE = '.buttons'

_SOUND_DIR = os.getenv('SOUND_DIRECTORY', 'sounds/transposed')

_buttons = {}


# Prescan the sound dir to make a map of ISO note values to sound files
_file_list = os.listdir(_SOUND_DIR)
_file_map = {
    note: [f for f in _file_list if note in f]
    for note in [f'{n}{o}' for n in _note_map.keys() for o in range(7)]
}


class InvalidNoteError(Exception):
    pass


class Note():
    '''
    A Note is a representation of a frequency, initiated with a
    helmholtz_value (eg. c#` indicates the MIDI note 61, or C3# or C4#
    '''

    def __init__(self, helmholtz_value):
        self.helmholtz_value = helmholtz_value

        m = _RE_HELMHOLTZ.search(helmholtz_value)
        if not m:
            raise InvalidNoteError(f'{helmholtz_value} failed to parse')
        note = m.group(1)
        octave_shift = m.group(2)
        if note[0].isupper():
            octave = 2
        else:
            octave = 3 + len(octave_shift)

        self.octave_value_yamaha = f'{note.upper()}{octave - 1}'
        self.octave_value = f'{note.upper()}{octave}'
        self.midi = 24 + _note_map[note.upper()] + 12 * octave

    def fname(self):
        file_ = random.choice(_file_map[self.octave_value])
        return os.path.join(_SOUND_DIR, file_)

    def __repr__(self):
        return f'[{self.midi}] {self.octave_value}'

    def __str__(self):
        return self.__repr__()


class Button():
    '''
    A button is one of the 72 keys on the bandoneon. Each button may have
    a different tone depending on whether the bandoneon is being opened or
    closed.

    note values are represented in Helmholtz Pitch notation:
    http://www.theoreticallycorrect.com/Helmholtz-Pitch-Numbering/

    We parse and store them out to Octave Numbering and MIDI notes.
    '''

    def __init__(self, key_number, draw_value, push_value):
        self.key_number = key_number
        self.draw_note = Note(draw_value)
        self.push_note = Note(push_value)

    def get_file(self, bellows_value):
        if bellows_value >= 0:
            return self.push_note.fname()
        return self.draw_note.fname()

    def __repr__(self):
        return (
            f'[{self.key_number}] {self.draw_note.octave_value}'
            f'/{self.push_note.octave_value}')

    def __str__(self):
        return self.__repr__()


def get_current_buttons_pushed():
    '''
    Measures "depressed buttons" and returns the set of selected Buttons.

    In `_VIRTUAL` mode, we get these values by reading in from a loacal file:
    `.buttons`, where we expect to find a comma delimited list a pressed keys
    with values from 0 - 70.
    '''
    try:
        with open(_VIRTUAL_BUTTONS_FILE, 'r') as f:
            raw_value = f.read()
    except FileNotFoundError as e:
        raw_value = ''
    raw_value = raw_value.replace('\x00', '')
    button_keys = raw_value.strip().split(',')
    try:
        button_keys = [int(k.strip()) for k in button_keys if k != '']
    except ValueError as e:
        import pdb; pdb.set_trace()
    pushed_buttons = [_buttons[k] for k in button_keys if k in _buttons.keys()]
    return set(pushed_buttons)


def button_deltas(active_buttons, pressed_buttons):
    '''
    Calculate the buttons to kill and the buttons to activate given active
    buttons and pressed buttons.
    '''
    kill = active_buttons.difference(pressed_buttons)
    start = pressed_buttons.difference(active_buttons)
    return start, kill


def _init_buttons():
    '''
    In the event that this program is being run in local dev mode, there is no
    button matrix to read from, and we will instead init the buttons based on
    an internal "virtual bandoneon" keyboard.
    '''
    if _KEY_MODE == _VIRTUAL:
        _init_virtual_buttons()
    elif _KEY_MODE == _IC2:
        raise NotImplementedError('IC2 handling is not yet implemented')
    else:
        raise NotImplementedError(f'{_KEY_MODE} is unrecognized')


def _init_virtual_buttons():
    '''
    Create a module-level button context.
    '''
    button_maps = [
        # left hand
        # col 1
        (0, 'D', 'E'),
        # col 2
        (1, 'B', 'e'),
        (2, 'e', 'A'),
        # col 3
        (3, 'g`', 'f#`'),
        (4, 'g#', 'e'),
        (5, 'd', 'G'),
        (6, 'E', 'D'),
        # col 4
        (7, 'a`', 'g#`'),
        (8, 'b', 'a'),
        (9, 'a', 'g'),
        (10, 'A', 'd'),
        # col 5
        (11, 'd#`', 'b`'),
        (12, 'd`', 'c#`'),
        (13, 'c`', 'b'),
        (14, 'g', 'a#'),
        (15, 'G#', 'G#'),
        # col 6
        (16, 'f#', 'f'),
        (17, 'f#`', 'e`'),
        (18, 'e`', 'd`'),
        (19, 'd#', 'c`'),
        (20, 'A#', 'A#'),
        # col 7
        (21, 'D#', 'C#'),
        (22, 'c#`', 'g#'),
        (23, 'c', 'f`'),
        (24, 'f`', 'c#'),
        (25, 'c#', 'd#'),
        # col 8
        (26, 'C', 'F'),
        (27, 'F#', 'B'),
        (28, 'G', 'f#'),
        (29, 'a#', 'c'),
        (30, 'f', 'd#`'),
        # col 9
        (31, 'F', 'F#'),
        (32, 'g#`', 'g`'),
        # right hand
        # col 1
        (33, 'a#', 'a#'),
        (34, 'a', 'a'),
        # col 2
        (35, 'd#`', 'd#`'),
        (36, 'f`', 'f`'),
        (37, 'b', 'b'),
        # col 3
        (38, 'f``', 'f``'),
        (39, 'a#`', 'e`'),
        (40, 'e`', 'f#`'),
        (41, 'c`', 'd`'),
        # col 4
        (42, 'd#``', 'e``'),
        (43, 'g#`', 'a`'),
        (44, 'c#``', 'f#``'),
        (45, 'd`', 'c#'),
        (46, 'c#`', 'c`'),
        # col 5
        (47, 'f#``', 'g#``'),
        (48, 'b`', 'c#``'),
        (49, 'f#`', 'g`'),
        (50, 'g`', 'g#`'),
        (51, 'a```', 'g```'),
        (52, 'b```', 'a```'),
        # col 6
        (53, 'a``', 'b``'),
        (54, 'd``', 'b`'),
        (55, 'a`', 'b`'),
        (56, 'a#``', 'a#`'),
        (57, 'f#```', 'a#``'),
        (58, 'g#```', 'g#```'),
        # col 7
        (59, 'c#```', 'e```'),
        (60, 'g#``', 'a``'),
        (61, 'c``', 'd``'),
        (62, 'c```', 'c``'),
        (63, 'e```', 'c```'),
        (64, 'g```', 'f#```'),
        # col 8
        (65, 'g``', 'd#``'),
        (66, 'b``', 'c#```'),
        (67, 'e``', 'g``'),
        (68, 'd```', 'd```'),
        (69, 'd#```', 'd#```'),
        (70, 'f```', 'f```'),
    ]
    global _buttons
    for bttn_key, draw, push in button_maps:
        _buttons[bttn_key] = Button(bttn_key, draw, push)


_init_buttons()
