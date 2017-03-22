from log import log
import input_utils
import os_utils

def is_finished(form):
    for input in form['inputs']:
        if not input_utils.is_finished(input):
            return False

    return True

def get_value(input):
    if input_utils.is_valid(input):
        if input['type'] == 'ip':
            text = '';
            for value in input['value']:
                text += value['value'] + '.'

            return text[:-1]

    return ''

def submit(form):
    action = form['name']
    args = []

    for input in form['inputs']:
        args.append(get_value(input))

    return os_utils.execute(action, args)

def init(form):
    inputs = form['inputs']
    for input in inputs:
        input_utils.clear_value(input)

    values = os_utils.execute(form['fill_command'])['return']

    for i in range(len(values)):
        input_utils.set_value(inputs[i], values[i])

    return form
