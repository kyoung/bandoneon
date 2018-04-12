'''
Bandoneon main application.
'''
import logging
from posix_ipc import MessageQueue, O_CREAT

from . import bellows, button
from .message import parse_message
from .sound import Sound


MESSAGE_Q_PATH = '/bandoneon'


_message_queue = MessageQueue(MESSAGE_Q_PATH, flags=O_CREAT, max_messages=1,
                              read=True, write=False)


def start_loop():
    '''
    Main program loop. Read from input buttons and bellows value, evaluate
    current volume and adjust accordingly.
    '''
    # <Button> to <Sound> mapping
    active_buttons = {}

    # - to + number indicating whether the bellows is opening or closing,
    # and at what pressure
    bellows_value = 0
    bellows_mode = bellows.OPEN
    volume = 0

    while True:
        msg, _ = _message_queue.receive()
        bttn_msg, bellow_msg = parse_message(msg)

        if bttn_msg:
            logging.debug(f'Button Msg: {bttn_msg.str()}')
            current_bttns = button.get_current_buttons_pushed(bttn_msg)
            buttons_to_start, buttons_to_kill = button.button_deltas(
                set(active_buttons.keys()),
                current_bttns)
            for bttn in buttons_to_kill:
                active_buttons[bttn].stop()
                del active_buttons[bttn]
            for bttn in buttons_to_start:
                try:
                    sound = Sound(bttn.get_file(bellows_value))
                except IndexError:
                    continue
                active_buttons[bttn] = sound
                sound.set_volume(volume)
                sound.play(loops=-1)  # ignore the returned channel

        if bellow_msg:
            logging.debug(f'Bellow Msg: {bellow_msg.str()}')
            current_bellows_value = bellow_msg.pressure
            current_bellows_mode = bellows.pressure_to_mode(current_bellows_value)
            current_volume = bellows.pressure_to_volume(current_bellows_value)
            if current_bellows_mode != bellows_mode:
                new_active_buttons = {}
                for bttn, sound in active_buttons.items():
                    sound.stop()
                    try:
                        new_sound = Sound(bttn.get_file(current_bellows_value))
                    except IndexError:
                        continue
                    new_sound.set_volume(current_volume)
                    new_sound.play(loops=-1)  # ignore the returned channel
                    new_active_buttons[bttn] = new_sound
                active_buttons = new_active_buttons
            elif current_bellows_value != bellows_value:
                for sound in active_buttons.values():
                    sound.set_volume(current_volume)
            bellows_value = current_bellows_value
            bellows_mode = current_bellows_mode
            volume = current_volume
