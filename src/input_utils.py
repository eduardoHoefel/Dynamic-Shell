from src.log import log

def to_text(input):
    type = input['type']
    if type == 'ip':
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
    elif type == 'string':
        return (input['value'] + '_______________')[:15]
    elif type == 'radio':
        if input['value'] == 0:
            return '[ ]'

        return '[*]'
    elif type == 'checkbox':
        return '[ ]'
    elif type == 'select':
        if input['value'] == -1:
            return 'Select:'

        return input['options'][input['value']]['name']

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
    elif input['type'] == 'string':
        return len(input['value'])
    elif input['type'] == 'radio':
        return 1
    elif input['type'] == 'checkbox':
        return 1
    elif input['type'] == 'select':
        return 0


    return 0

def clear_value(input):
    type = input['type']
    value = ''

    if type == 'ip':
        value = [ 
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
    elif type == 'string':
        value = ''
    elif type == 'checkbox':
        value = 0
    elif type == 'radio':
        value = 0
    elif type == 'select':
        value = -1

    input['value'] = value

def set_value(input, value):
    clear_value(input)
    if type(value) == int:
        append(input, value)
    else:
        for char in value:
            append(input, char)

    append(input, 'FINISH')

def append(input, action):
    if action == '':
        return False

    input_type = input['type']
    if input_type == 'ip':
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
                        onchange(input)
                    return True
            last = input['value'][-1]
            if len(last) < 3:
                last['done'] = False
                last['value'] += action
                if len(value['value']) == 3 and int(value['value']) > 0:
                    value['done'] = True
                    int_value = int(value['value'])
                    if int_value > 255:
                        int_value = 255

                    value['value'] = str(int_value)
                    onchange(input)
                return True

        elif action == 'BACKSPACE':
            for value in input['value'][::-1]:
                if value['done'] or len(value['value']) > 0:
                    value['value'] = value['value'][:-1]
                    value['done'] = False
                    onchange(input)
                    return True

        elif action in ['.', ' ', 'ENTER', 'FINISH', 'RIGHT_ARROW']:
            for value in input['value']:
                if not value['done']:
                    if len(value['value']) == 0:
                        return True

                    value['done'] = True
                    int_value = int(value['value'])
                    if int_value > 255:
                        int_value = 255

                    value['value'] = str(int_value)
                    onchange(input)
                    return True
    elif input_type == 'select':
        if type(action) == int or action.isdigit():
            input['value'] = int(action)
            onchange(input)
            return True
    elif input_type == 'string':
        if action == 'BACKSPACE':
            input['value'] = input['value'][:-1]
            onchange(input)
            return True
        elif len(action) == 1:
            input['value'] += action
            onchange(input)
            return True
    elif input_type == 'radio':
        if action == 0:
            input['value'] = 0
            onchange(input)
            return True
        elif action == 1:
            input['value'] = 1
            onchange(input)
            return True
        elif action != 'FINISH':
            if input['value'] == 0:
                input['value'] = 1
            else:
                input['value'] = 0

            onchange(input)
            return True

    return False

def is_finished(input):
    if input['required']:
        return is_valid(input)

    return True


def is_valid(input):
    type = input['type']
    if type == 'ip':
        for value in input['value']:
            if not value['done']:
                    return False
    elif type == 'string':
        return len(input['value']) > 0
    elif type == 'select':
        return input['value'] >= 0

    return True

def onchange(input):
    from src import form_utils
    if 'onchange' in input:
        form_utils.exec_action(input['form'], input['onchange'], [input['options'][input['value']]['name']])
    if input['type'] == 'select' and 'onset' in input['options'][input['value']]:
        form_utils.exec_action(input['form'], input['options'][input['value']]['onset'])
