'''
Bandoneon main application.
'''
from bandoneon import bellows, button
from bandoneon.sound import Sound  # Stub as Sound


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

    while True:
        current_bttns = button.get_current_buttons_pushed()
        current_bellows_value = bellows.get_current_bellows_value()
        current_bellows_mode = bellows.pressure_to_mode(current_bellows_value)
        current_volume = bellows.pressure_to_volume(current_bellows_value)
        buttons_to_start, buttons_to_kill = button.button_deltas(
            set(active_buttons.keys()),
            current_bttns)
        for bttn in buttons_to_kill:
            active_buttons[bttn].stop()
            del active_buttons[bttn]
        for bttn in buttons_to_start:
            try:
                sound = Sound(bttn.get_file(current_bellows_value))
            except IndexError:
                continue
            active_buttons[bttn] = sound
            sound.set_volume(current_volume)
            sound.play(loops=-1)  # ignore the returned channel
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


if __name__ == '__main__':
    start_loop()
