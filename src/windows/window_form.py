from src import input_utils, form_utils
from src.log import log

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
    from src.windows import windows_utils
    form = window['form']
    inputs = form['inputs']
    length = len(inputs)

    cursor_pos = window['cursor_pos']
    if cursor_over_input(cursor_pos, inputs):
        current_input = inputs[cursor_pos]
        if input_utils.append(current_input, action):
            window['updated'] = True
            return

    if action in ['DOWN_ARROW', 'RIGHT_ARROW', 'TAB']:
        if cursor_over_input(cursor_pos, inputs):
            input_utils.append(current_input, 'FINISH')

        cursor_pos += 1
        while cursor_pos >= 0 and cursor_pos < length and not inputs[cursor_pos]['visible']:
            cursor_pos += 1

        if cursor_pos == SUBMIT_BUTTON and not form_utils.is_finished(form):
            cursor_pos += 1
        window['updated'] = True
    elif action in ['LEFT_ARROW', 'UP_ARROW']:
        if cursor_over_input(cursor_pos, inputs):
            input_utils.append(current_input, 'FINISH')

        cursor_pos -= 1
        while cursor_over_input(cursor_pos, inputs) and not inputs[cursor_pos]['visible']:
            cursor_pos -= 1

        if cursor_pos == SUBMIT_BUTTON and not form_utils.is_finished(form):
            cursor_pos -= 1
        window['updated'] = True

    elif action == 'ENTER':
        if cursor_over_input(cursor_pos, inputs):
            if current_input['type'] == 'select':
                windows_utils.add_modal(window, current_input)
            else:
                cursor_pos += 1
                while cursor_pos >= 0 and cursor_pos < length and not inputs[cursor_pos]['visible']:
                    cursor_pos += 1

                if cursor_pos == SUBMIT_BUTTON and not form_utils.is_finished(form):
                    cursor_pos += 1
                window['updated'] = True
        elif cursor_pos == RETURN_BUTTON:
            windows_utils.return_to_menu()
            window['updated'] = True
        elif cursor_pos == SUBMIT_BUTTON:
            if form_utils.is_finished(form):
                if form['type'] == 'save_config':
                    result = form_utils.submit(form)['result']
                    result = str(result)
                    if result in form['messages']:
                        message = form['messages'][result]
                    else:
                        message = 'Message not found: ' + result

                    windows_utils.add_popup(window, result, message)
                elif form['type'] == 'stream':
                    windows_utils.add_stream(window)

                if 'onsubmit' in form:
                    args = form_utils.to_args(form['inputs'])
                    form_utils.exec_action(form, form['onsubmit'], args)

    elif action == 'ESC':
        windows_utils.return_to_menu()
        window['updated'] = True

    if (cursor_pos < RETURN_BUTTON):
        cursor_pos = length - 1
    elif (cursor_pos >= length):
        cursor_pos = RETURN_BUTTON

    window['cursor_pos'] = cursor_pos

def cursor_over_input(cursor_pos, inputs):
    return cursor_pos >= 0 and cursor_pos < len(inputs)
