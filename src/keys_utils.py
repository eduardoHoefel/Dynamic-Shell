import curses, os
from src.log import log

keys = {
        -1: '', #CTRL C
        3: '', #CTRL C
        4: '', #CTRL D
        8: 'BACKSPACE',
        9: 'TAB',
        10: 'ENTER',
        26: '', #CTRL Z
        27: 'ESC',
        32: ' ',
        46: '.',
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
        65: 'A',
        66: 'B',
        67: 'C',
        68: 'D',
        69: 'E',
        70: 'F',
        71: 'G',
        72: 'H',
        73: 'I',
        74: 'J',
        75: 'K',
        76: 'L',
        77: 'M',
        78: 'N',
        79: 'O',
        80: 'P',
        81: 'Q',
        82: 'R',
        83: 'S',
        84: 'T',
        85: 'U',
        86: 'V',
        87: 'W',
        88: 'X',
        89: 'Y',
        90: 'Z',
        97: 'a',
        98: 'b',
        99: 'c',
        100: 'd',
        101: 'e',
        102: 'f',
        103: 'g',
        104: 'h',
        105: 'i',
        106: 'j',
        107: 'k',
        108: 'l',
        109: 'm',
        110: 'n',
        111: 'o',
        111: 'p',
        112: 'q',
        113: 'r',
        114: 's',
        115: 't',
        116: 'u',
        117: 'v',
        118: 'w',
        119: 'x',
        120: 'y',
        121: 'z',
        258: 'DOWN_ARROW',
        259: 'UP_ARROW',
        260: 'LEFT_ARROW',
        261: 'RIGHT_ARROW',
        263: 'BACKSPACE'
}

def get_input(window):
    renderer = window['renderer']
    renderer.nodelay(1)
    x = renderer.getch() # Gets user input
    if x in keys:
        return keys[x]

    return ''
