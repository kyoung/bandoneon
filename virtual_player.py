'''
The virtual player can be run to "play" the `.bellows` and `.buttons` files
by populating them with keyed notes and pressure values.

Use alongside the main bandoneon program in virtual mode.
'''
import mido

from bandoneon import button, bellows

BELLOWS_FILE = bellows._VIRTUAL_BELLOWS_FILE
BUTTON_FILE = button._VIRTUAL_BUTTONS_FILE


CUMPARSITA = 'cumps.mid'


def main():
    with mido.MidiFile(CUMPARSITA) as midi:
        for message in midi.play():
            # print out to the files
            import pdb; pdb.set_trace()
            pass


if __name__ == '__main__':
    main()
