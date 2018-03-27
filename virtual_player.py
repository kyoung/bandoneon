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
            if message.type in ['control_change', 'program_change']:
                continue
            # print out to the files
            if message.type in ['note_on', 'note_off']:
                note = message.note
                velocity = message.velocity
                time = message.time  # The time attribute of each message is the number of seconds since the last message or the start of the file.

            import pdb; pdb.set_trace()


if __name__ == '__main__':
    main()
