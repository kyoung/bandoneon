'''
Bellow code wraps the sensing and translation of the bellows position.
'''
import os

# Bellows modes are either opening or closing
OPEN = 'open'
CLOSED = 'closed'

_VIRTUAL = 'virtual'
_SLIDER = 'slider'
_BAROMETRIC = 'barometric'
_BELLOW_MODE = os.getenv('BANDONEON_BELLOWS', _VIRTUAL)

_VIRTUAL_BELLOWS_FILE = '.bellows'


def get_current_bellows_value():
    '''
    Returns a reading from the bellows mechanism, ranging from -127 to 127 to
    indicate the pressure and direction of the bandoneon.

    In `_VIRTUAL` mode, we get these values by reading in from a loacal file:
    `.bellows`, where we expect to find a numerica value from -127 to 127
    '''
    try:
        with open(_VIRTUAL_BELLOWS_FILE, 'r') as f:
            bellows_value = int(f.readlines()[0].strip())
    except FileNotFoundError as e:
        bellows_value = 0
    return bellows_value


def pressure_to_volume(bellow_pressure):
    '''
    Translate a -127, 127 range value to a 0.0, 1.0 value.

    nb. MVP assumes a linear relation.
    '''
    return abs(bellow_pressure) / 127


def pressure_to_mode(bellow_pressure):
    '''
    When the pressure reading is positive, there is more pressure inside the
    case than outside, meaning it is being CLOSED.

    Conversely, the opposite is OPEN.
    '''
    return CLOSED if bellow_pressure >= 0 else OPEN
