from log import log
import curses, os

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

def get_form_input_text(input):
    if input['type'] == 'ip':
        text = '';
        for value in input['value']:
            if value['done']:
                text_aux = '___' + value['value']
                text_aux = text_aux[-3:]
            else:
                text_aux = value['value'] + '___' 
                text_aux = text_aux[:3]

            text += text_aux + '.'

        return text[:-1]

    return ''

def get_cursor_pos(input):
    if input['type'] == 'ip':
        pos = 0
        for value in input['value']:
            if value['done']:
                pos += 4
            else:
                pos += len(value['value'])
                return pos

        if pos > 0:
            pos -= 1

        return pos

    return 0

def clear_value(input):
    if input['type'] == 'ip':
        input['value'] = [ 
            {
                "done": False,
                "value": ''
            }, {
                "done": False,
                "value": ''
            }, {
                "done": False,
                "value": ''
            }, {
                "done": False,
                "value": ''
            }
        ]
    elif input['type'] == 'select':
        input['value'] = ' -- Selecione -- '
    else:
        input['value'] = ''

def set_value(input, value):
    clear_value(input)
    for char in value:
        append(input, char)

    append(input, 'ENTER')

def append(input, action):
    if input['type'] == 'ip':
        if action.isdigit():
            for value in input['value']:
                if not value['done']:
                    if len(value['value']) == 3:
                        return False

                    value['value'] += action
                    if len(value['value']) == 3 and int(value['value']) > 0:
                        value['done'] = True
                        int_value = int(value['value'])
                        if int_value > 255:
                            int_value = 255
                        value['value'] = str(int_value)
                    return True
        elif action == 'BACKSPACE':
            for value in input['value'][::-1]:
                if value['done'] or len(value['value']) > 0:
                    value['value'] = value['value'][:-1]
                    value['done'] = False
                    return True
        elif action in ['.', 'DOT', 'ENTER']:
            for value in input['value']:
                if not value['done']:
                    if int('0' + value['value']) == 0:
                        return False

                    value['done'] = True
                    int_value = int(value['value'])
                    if int_value > 255:
                        int_value = 255
                    value['value'] = str(int_value)
                    return True

    return False

def is_finished(input):
    if input['required']:
        return is_valid(input)

    return True


def is_valid(input):
    if input['type'] == 'ip':
        for value in input['value']:
            if not value['done']:
                    return False

    return True
