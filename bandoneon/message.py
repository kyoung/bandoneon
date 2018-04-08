'''
Message classes to be passed over the POSIX socket.

Messages indicate either a change in bellow pressure or a change in active
buttons. All messages must be serialized down to strings.
'''
import re


class InvalidMessage(Exception):
    pass


class BellowsMessage():

    _RE = re.compile('blw:([\d]*)')

    def __init__(self, pressure=0):
        self.pressure = pressure

    def str(self):
        return f'blw:{self.pressure}'

    def parse(self, raw):
        m = self._RE.search(raw)
        if not m:
            raise InvalidMessage(f'{raw} failed to match BellowMessage format')
        if not m.group(1):
            return None
        self.pressure = int(m.group(1))
        return self

    def __eq__(self, other):
        return self.pressure == other.pressure


class ButtonMessage():

    _RE = re.compile('btn:([\d,]*)')

    def __init__(self, active_buttons=None):
        self.active_buttons = active_buttons
        if not active_buttons:
            self.active_buttons = []

    def str(self):
        button_list = ','.join([f'{i}' for i in self.active_buttons])
        return f'btn:{button_list}'

    def parse(self, raw):
        m = self._RE.search(raw)
        if not m:
            raise InvalidMessage(f'{raw} failed to match ButtonMessage format')
        if not m.group(1):
            return None
        self.active_buttons = [int(i) for i in m.group(1).split(',')]
        return self

    def __eq__(self, other):
        return self.active_buttons == other.active_buttons


def parse_message(raw_msg):
    '''
    Given a string either of <ButtonMessage> or <BellowsMessage> format, return
    a tuple (<ButtonMessage>|None, <BellowsMessage>|None)
    '''
    str_msg = raw_msg.decode('utf-8')

    if str_msg.startswith('blw'):
        return (None, BellowsMessage().parse(str_msg))

    if str_msg.startswith('btn'):
        return (ButtonMessage().parse(str_msg), None)

    return (None, None)
