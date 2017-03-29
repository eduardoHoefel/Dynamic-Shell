from src.log import log
from src import input_utils, os_utils

def is_finished(form):
    for input in form['inputs']:
        if input['visible'] and not input_utils.is_finished(input):
            return False

    return True

def get_value(input):
    if input['visible'] and input_utils.is_valid(input):
        type = input['type']
        if type == 'ip':
            text = '';
            for value in input['value']:
                text += value['value'] + '.'

            return text[:-1]
        elif type == 'select':
            return str(input['options'][input['value']]['value'])
        elif type == 'string':
            return input['value']
        elif type == 'radio':
            return str(input['value'])

    return ''

def to_args(inputs):
    args = []

    for input in inputs:
        args.append(get_value(input))

    return args

def submit(form, action = ''):
    if action == '':
        action = form['name']

    args = to_args(form['inputs'])

    return os_utils.execute_with_log(action, args)

def init(form):
    inputs = form['inputs']
    for input in inputs:
        input['form'] = form
        input['visible'] = True
        if input['type'] == 'select' and type(input['options']) is str:
            load_options(input)

        input_utils.clear_value(input)

    if 'onload' in form:
        exec_action(form, form['onload'])

    return form

def exec_action(form, action, args=[]):
    type = action['type']
    if type == 'FILL':
        command = action['command']
        inputs = form['inputs']
        values = os_utils.execute(command, args)['return']
        for i in range(len(values)):
            value = values[i].split('=')
            for input in inputs:
                if input['name'] == value[0]:
                    input_utils.set_value(input, value[1])
                    break
    elif type == 'SHOW_FIELDS':
        inputs = form['inputs']
        for input in inputs:
            if input['name'] in action['values']:
                input['visible'] = True
    elif type == 'HIDE_FIELDS':
        inputs = form['inputs']
        for input in inputs:
            if input['name'] in action['values']:
                input['visible'] = False
    elif type == 'COMMAND':
        command = action['command']
        os_utils.execute(command, args)

def load_options(input):
    command = input['options']
    values = os_utils.execute(command)['return']
    options = []
    for i in range(len(values)):
        value = values[i]
        options.append({ "name": value, "value": value })

    input['options'] = options
