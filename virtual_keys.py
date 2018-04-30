'''
Built off of: https://stackoverflow.com/questions/24072790/detect-key-press-in-python#32386410
'''
import curses
import os

from posix_ipc import MessageQueue, O_CREAT

from bandoneon import button, MESSAGE_Q_PATH
from bandoneon.message import ButtonMessage, BellowsMessage


# Keyboard to midi note map
KEYBOARD_MAP = {
    'a': 60,
    'w': 61,
    's': 62,
    'e': 63,
    'd': 64,
    'f': 65,
    't': 66,
    'g': 67,
    'y': 68,
    'h': 69,
    'u': 70,
    'j': 71,
    'k': 72
}

# Build up a midi map buttons
MIDI_TO_KEY_DRAW = {
    button.draw_note.midi: button.key_number
    for button in button._buttons.values()
}
MIDI_TO_KEY_PUSH = {
    button.push_note.midi: button.key_number
    for button in button._buttons.values()
}

messageQueue = MessageQueue(MESSAGE_Q_PATH, flags=O_CREAT, max_messages=1,
                            read=False, write=True)


def play_key(keyboard_key):
    if keyboard_key not in KEYBOARD_MAP:
        return
    midi_note = KEYBOARD_MAP[keyboard_key]
    bandoneon_key = MIDI_TO_KEY_PUSH[midi_note]
    msg = ButtonMessage(active_buttons=[bandoneon_key])
    messageQueue.send(msg.str())


def main(win):
    win.nodelay(True)
    key=""
    win.clear()
    win.addstr("Detected key:")
    while 1:
        try:
           key = win.getkey()
           win.clear()
           win.addstr("Detected key:")
           win.addstr(str(key))
           play_key(str(key))
           noise = BellowsMessage(pressure=100)
           messageQueue.send(noise.str())
           if key == os.linesep:
              break
        except Exception as e:
           # No input
           pass
    noise = BellowsMessage(pressure=0)
    messageQueue.send(noise.str())

curses.wrapper(main)
