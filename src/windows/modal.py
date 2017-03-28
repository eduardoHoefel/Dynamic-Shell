from src import input_utils

RETURN_BUTTON = -1

def update(window, action):
    from src.windows import windows_utils

    cursor_pos = window['cursor_pos']
    input = window['input']
    length = len(input['options'])

    if action == 'DOWN_ARROW':
        cursor_pos += 1
        window['updated'] = True
    elif action == 'UP_ARROW':
        cursor_pos -= 1
        window['updated'] = True
    elif action == 'ENTER':
        if cursor_pos != RETURN_BUTTON:
            input_utils.set_value(input, cursor_pos)

        windows_utils.remove_popup(window)

    if (cursor_pos < RETURN_BUTTON):
        cursor_pos = length - 1
    elif (cursor_pos >= length):
        cursor_pos = RETURN_BUTTON

    window['cursor_pos'] = cursor_pos
