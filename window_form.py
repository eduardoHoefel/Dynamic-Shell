import windows_utils
import input_utils
import form_utils
from log import log

RETURN_BUTTON = -2
SUBMIT_BUTTON = -1

def load_form(window, form_name):
    import json
    
    with open('assets/forms.json') as json_data:
        json_object = json.load(json_data)

    form = json_object[form_name]
    form = form_utils.init(form)

    form['name'] = form_name

    window['form'] = form
    window['cursor_pos'] = 0
    window['updated'] = True

def update(window, action):
    form = window['form']
    inputs = form['inputs']
    length = len(inputs)

    cursor_pos = window['cursor_pos']
    current_input = inputs[cursor_pos]

    if action == 'DOWN_ARROW':
        input_utils.append(current_input, 'ENTER')
        cursor_pos += 1
        if cursor_pos == SUBMIT_BUTTON and not form_utils.is_finished(form):
            cursor_pos += 1
        window['updated'] = True
    elif action == 'UP_ARROW':
        input_utils.append(current_input, 'ENTER')
        cursor_pos -= 1
        if cursor_pos == SUBMIT_BUTTON and not form_utils.is_finished(form):
            cursor_pos -= 1
        window['updated'] = True
    elif action == 'ENTER':
        #TODO: go to next, open select, select radio, mark checkbox, return or submit
        if cursor_pos == RETURN_BUTTON:
            windows_utils.return_to_menu()
            window['updated'] = True
        elif cursor_pos == SUBMIT_BUTTON:
            if form_utils.is_finished(form):
                result = form_utils.submit(form)['result']
                message = form['messages'][result]
                windows_utils.add_popup(window, result, message)
            #windows_utils.return_to_menu()
    elif action == 'ESC':
        windows_utils.return_to_menu()
        window['updated'] = True
    else:
        if input_utils.append(current_input, action):
            window['updated'] = True

    if (cursor_pos < RETURN_BUTTON):
        cursor_pos = length - 1
    elif (cursor_pos >= length):
        cursor_pos = RETURN_BUTTON

    window['cursor_pos'] = cursor_pos
