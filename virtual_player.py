'''
The virtual player can be run to "play" the `.bellows` and `.buttons` files
by populating them with keyed notes and pressure values.

Use alongside the main bandoneon program in virtual mode.
'''
import time

import mido

from bandoneon import button, bellows


BELLOWS_FILE = bellows._VIRTUAL_BELLOWS_FILE
BUTTON_FILE = button._VIRTUAL_BUTTONS_FILE
CUMPARSITA = 'cumparsita.mid'

# Build up a midi map buttons
MIDI_TO_KEY_DRAW = {
    button.draw_note.midi: button.key_number
    for button in button._buttons.values()
}
MIDI_TO_KEY_PUSH = {
    button.push_note.midi: button.key_number
    for button in button._buttons.values()
}


def write_notes(notes, direction):
    '''
    notes - set of midi notes
    direction - 'draw' or 'push'

    Given a list of notes, calculate possible keys.
    '''
    map_ = {
        'draw': MIDI_TO_KEY_DRAW,
        'push': MIDI_TO_KEY_PUSH
    }[direction]
    keys = [map_[n] for n in notes]
    key_string = ','.join((str(k) for k in keys))
    with open(BUTTON_FILE, 'w') as f:
        f.write(key_string)


def write_bellows(velocities, direction):
    '''
    velocities - list of velocity values
    direction - 'draw' or 'push'

    The velocity is consistent on a bandoneon, (or any concertina or accordian
    for that matter); we much average it if presented with a list of varying
    velocities.

    Direction will determine the cardinality of the value (pos or neg)
    '''
    try:
        avg_velocity = int(sum(velocities) / len(velocities))
    except ZeroDivisionError:
        avg_velocity = 0
    with open(BELLOWS_FILE, 'w') as f:
        f.write(str(avg_velocity))


def check_song():
    max_midi = None
    min_midi = None
    for message in mido.MidiFile(CUMPARSITA):
        if message.type not in ['note_on', 'note_off']:
            continue
        if not max_midi or message.note > max_midi:
            max_midi = message.note
        if not min_midi or message.note < min_midi:
            min_midi = message.note
    print(f'MIDI range: {min_midi} - {max_midi}')


def main():
    '''
    '''
    currently_playing_notes = set()
    current_velocities = [0]
    for message in mido.MidiFile(CUMPARSITA):
        # We're not really interested in anything else just yet
        if message.type not in ['note_on', 'note_off']:
            continue

        print((
            f'{message.type}: {message.note} ({message.velocity}) '
            f'-- {message.time}'
        ))

        # NB. The time attribute of each message is the number of seconds since
        # the last message or the start of the file.

        if message.time == 0:
            if message.type == 'note_on':
                currently_playing_notes.add(message.note)
                current_velocities.append(message.velocity)
            if message.type == 'note_off':
                try:
                    currently_playing_notes.remove(message.note)
                except KeyError:
                    print(f'note wasn\'t playing: {message.note}')

        else:
            write_notes(currently_playing_notes, 'draw')
            write_bellows(current_velocities, 'draw')
            time.sleep(message.time)
            if message.type == 'note_on':
                current_velocities = [message.velocity,]
                currently_playing_notes.add(message.note)
            if message.type == 'note_off':
                try:
                    currently_playing_notes.remove(message.note)
                except KeyError:
                    print(f'note wasn\'t playing: {message.note}')


if __name__ == '__main__':
    # check_song()
    main()
