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
