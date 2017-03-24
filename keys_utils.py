import curses, os
from log import log

keys = {
        10: 'ENTER',
        27: 'ESC',
        46: 'DOT',
        48: '0',
        49: '1',
        50: '2',
        51: '3',
        52: '4',
        53: '5',
        54: '6',
        55: '7',
        56: '8',
        57: '9',
        258: 'DOWN_ARROW',
        259: 'UP_ARROW',
        260: 'UP_ARROW',
        261: 'DOWN_ARROW',
        263: 'BACKSPACE'
}

def get_input(window):
    x = window['renderer'].getch() # Gets user input
    log(x)
    return keys[x]
