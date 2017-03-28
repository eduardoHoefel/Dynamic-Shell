import time
from src import form_utils
from src.windows import popup

def update(window, action):
    popup.update(window, action)

    cursor_pos = window['cursor_pos']

    if 'time' not in window:
        window['time'] = time.time()
        stream(window)
        window['updated'] = True
        window['updates'] = 1
    else:
        if 'limit' not in window['form'] or window['updates'] < window['form']['limit']:
            new_time = time.time()
            if new_time - window['time'] > 1:
                window['time'] = new_time
                update_cursor = cursor_pos >= len(window['result']) - 1

                length = stream(window)
                if update_cursor:
                    cursor_pos += length

                window['updated'] = True
                window['updates'] += 1

    if action == 'DOWN_ARROW':
        cursor_pos += 1
        window['updated'] = True

    if action == 'UP_ARROW':
        cursor_pos -= 1
        window['updated'] = True

    if cursor_pos >= len(window['result']):
        cursor_pos = len(window['result']) - 1

    window['cursor_pos'] = cursor_pos

def stream(window):
    result = form_utils.submit(window['form'])
    if window['form']['behavior'] == 'substitute':
        window['result'] = []

    for line in result['return']:
        window['result'].append(line)

    return len(result['return'])
