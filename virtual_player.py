'''
The virtual player can be run to "play" the `.bellows` and `.buttons` files
by populating them with keyed notes and pressure values.

Use alongside the main bandoneon program in virtual mode.
'''
from collections import defaultdict
import logging
import time

import mido

from bandoneon import button, bellows


BELLOWS_FILE = bellows._VIRTUAL_BELLOWS_FILE
BUTTON_FILE = button._VIRTUAL_BUTTONS_FILE
CUMPARSITA = 'cumparsita.mid'
BANDONEON_CHANNELS = set([3, 5, 6])  # the only bandoneon channels in the file

# Build up a midi map buttons
MIDI_TO_KEY_DRAW = {
    button.draw_note.midi: button.key_number
    for button in button._buttons.values()
}
MIDI_TO_KEY_PUSH = {
    button.push_note.midi: button.key_number
    for button in button._buttons.values()
}


class DirectionEnum():
    DRAW = 'draw'
    PUSH = 'push'


class InvalidNoteCombination(Exception):
    pass


def infer_direction(notes, last_direction=DirectionEnum.DRAW):
    '''
    notes - set of midi notes

    Given a set of notes, determine if the concertina is being drawn or pushed,
    also alternate if possible.
    '''
    draw_possible = False
    if all([n in MIDI_TO_KEY_DRAW for n in notes]):
        draw_possible = True

    push_possible = False
    if all([n in MIDI_TO_KEY_PUSH for n in notes]):
        push_possible = True

    if draw_possible and push_possible:
        return (DirectionEnum.DRAW
                if last_direction != DirectionEnum.DRAW
                else DirectionEnum.PUSH)

    if draw_possible:
        return DirectionEnum.DRAW
    elif push_possible:
        return DirectionEnum.PUSH

    raise InvalidNoteCombination(', '.join([str(n) for n in notes]))


def write_notes(notes, direction):
    '''
    notes - set of midi notes
    direction - one of the DirectionEnum values

    Given a list of notes, calculate possible keys.
    '''
    map_ = {
        DirectionEnum.DRAW: MIDI_TO_KEY_DRAW,
        DirectionEnum.PUSH: MIDI_TO_KEY_PUSH
    }[direction]

    # sometimes we get impossible notes?
    keys = [map_[n] for n in notes if n in map_]

    # report on bad notes:
    bad_notes = [n for n in notes if n not in map_]
    if bad_notes:
        logging.warning(f'Invalid notes: {bad_notes}')

    if keys:
        key_string = ','.join((str(k) for k in keys))
    else:
        key_string  = ''

    with open(BUTTON_FILE, 'w') as f:
        f.seek(0)
        f.write(key_string)


def write_bellows(velocities, direction=DirectionEnum.DRAW):
    '''
    velocities - list of velocity values
    direction - one of the DirectionEnum values

    The velocity is consistent on a bandoneon, (or any concertina or accordian
    for that matter); we much average it if presented with a list of varying
    velocities.

    Direction will determine the cardinality of the value (pos or neg)
    '''
    try:
        avg_velocity = int(sum(velocities) / len(velocities))
    except ZeroDivisionError:
        avg_velocity = 0
    if direction == DirectionEnum.DRAW:
        avg_velocity *= -1
    with open(BELLOWS_FILE, 'w') as f:
        f.write(str(avg_velocity))


def check_song():

    channel_ranges = defaultdict(lambda: {'max_midi': None, 'min_midi': None})

    for message in mido.MidiFile(CUMPARSITA):
        if message.is_meta:
            if message.type == 'channel_prefix':
                print(f'Channel Prefix: {message.channel}')
            if message.type == 'track_name':
                print(f'\t{message.name}')
        if message.type not in ['note_on', 'note_off']:
            continue
        ch = message.channel
        max_ = channel_ranges[ch]['max_midi']
        if not max_ or message.note > max_:
            channel_ranges[ch]['max_midi'] = message.note
        min_ = channel_ranges[ch]['min_midi']
        if not min_ or message.note < min_:
            channel_ranges[ch]['min_midi'] = message.note

    print('MIDI ranges:')
    for ch, ranges in channel_ranges.items():
        print(f"{ch}: min {ranges['min_midi']}, max {ranges['max_midi']}")


def main():
    '''
    '''
    currently_playing_notes = set()
    current_velocities = [0]
    direction = DirectionEnum.DRAW
    for message in mido.MidiFile(CUMPARSITA):
        # We're not really interested in anything else just yet
        if message.type not in ['note_on', 'note_off']:
            continue

        if message.channel not in BANDONEON_CHANNELS:
            continue

        logging.info((
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
                    logging.info(f'note wasn\'t playing: {message.note}')

        else:
            direction = infer_direction(currently_playing_notes, direction)
            write_notes(currently_playing_notes, direction)
            write_bellows(current_velocities, direction)
            time.sleep(message.time * 10)
            if message.type == 'note_on':
                current_velocities = [message.velocity, ]
                currently_playing_notes.add(message.note)
            if message.type == 'note_off':
                try:
                    currently_playing_notes.remove(message.note)
                except KeyError:
                    logging.info(f'note wasn\'t playing: {message.note}')

    write_notes(currently_playing_notes, direction)
    write_bellows([])


if __name__ == '__main__':
    # check_song()
    main()
