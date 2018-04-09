import logging
import sys

from bandoneon import start_loop


if __name__ == '__main__':
    if 'debug' in sys.argv:
        logging.basicConfig(level=logging.DEBUG)
        
    start_loop()
