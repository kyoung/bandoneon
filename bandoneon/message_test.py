import unittest

from . import message


class TestBellowsMessage(unittest.TestCase):

    def test_string_formating(self):
        m = message.BellowsMessage(pressure=100)
        s = m.str()
        self.assertEqual(s, 'blw:100')

    def test_parse_raw(self):
        r = 'blw:101'
        m = message.BellowsMessage().parse(r)
        self.assertEqual(m.pressure, 101)

    def test_negative_bellows_values(self):
        r = 'blw:-100'
        m = message.BellowsMessage().parse(r)
        self.assertEqual(m.pressure, -100)
        s = m.str()
        self.assertEqual(s, r)


class TestButtonMessage(unittest.TestCase):

    def test_string_formating(self):
        m = message.ButtonMessage(active_buttons=[1, 2, 3])
        s = m.str()
        self.assertEqual(s, 'btn:1,2,3')

    def test_parse_raw(self):
        r = 'btn:6,5,4'
        m = message.ButtonMessage().parse(r)
        self.assertEqual(m.active_buttons, [6, 5, 4])


class TestParseMessage(unittest.TestCase):

    def test_parse_message(self):
        expected = {
            b'btn:12,34,45': (message.ButtonMessage([12, 34, 45]), None),
            b'blw:123': (None, message.BellowsMessage(123)),
            b'not_valid': (None, None),
            b'blw:': (None, None)
        }
        for m, ex in expected.items():
            got = message.parse_message(m)
            self.assertEqual(ex, got)
