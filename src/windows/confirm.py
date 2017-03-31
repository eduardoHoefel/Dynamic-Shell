
def update(window, action):
    from src.windows import windows_utils
    from src import os_utils

    cursor_pos = window['cursor_pos']
    if action in ['ENTER', 'ESC']:
        windows_utils.remove_popup(window)
        if cursor_pos == 1:
            os_utils.execute(window['command'])
    elif action in ['LEFT_ARROW', 'UP_ARROW']:
        cursor_pos = 0
        window['updated'] = True
    elif action in ['DOWN_ARROW', 'RIGHT_ARROW']:
        cursor_pos = 1
        window['updated'] = True
    elif action == 'TAB':
        if cursor_pos == 0:
            cursor_pos = 1
        else:
            cursor_pos = 0

        window['updated'] = True

    window['cursor_pos'] = cursor_pos
