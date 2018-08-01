import curses, os, curses.textpad
from math import ceil, trunc
from src import colors, input_utils, form_utils
from src.log import log
from src.windows import window_menu, window_form, popup, modal, stream, confirm

windows = 0
active_window = 0

WINDOW_HEADER = 0
WINDOW_MENU = 1
WINDOW_FORM = 2
POPUP = 3
MODAL = 4
STREAM = 5
CONFIRM = 6

def print_window(window):
    if not window['updated']:
        return

    window['updated'] = False
    curses.curs_set(0)

    type = window['config']['type']
    renderer = window['renderer']

    renderer.clear()

    height = window['config']['height'] - 3
    width = window['config']['width'] - 5

    if type == WINDOW_HEADER:
        i = 2
        with open('title.txt') as f:
            for line in f:
                renderer.addstr(i, 2, line, colors.get['RCX_TITLE']) # Title for this menu
                i += 1

        with open('version.txt') as f:
            subtitle = 'version: ' + f.readline()
            renderer.addstr(height, 2, subtitle, colors.get['RCX_TITLE']) # Title for this menu

    elif type == WINDOW_MENU:

        textstyle = colors.get['MENU_TITLE']
        title = window['menu']['title'] + ':'
        renderer.addstr(2, 4, title, textstyle)

        cursor_pos = window['cursor_pos']
        options = window['menu']['options']
        for index in range(len(options)):
            title = options[index]['title']
            hotkey = options[index]['hotkey']

            textstyle = colors.get['NORMAL']
            if cursor_pos == index:
                textstyle = colors.get['HIGHLIGHTED']

            renderer.addstr(4+index, 4, "[%d] - %s" % (hotkey, title), textstyle)
    elif type == WINDOW_FORM:

        if window['active']:
            cursor_pos = window['cursor_pos']

            textstyle = colors.get['FORM_TITLE']
            form = window['form']
            title = form['title'] + ':'
            renderer.addstr(2, 4, title, textstyle)

            textstyle = colors.get['NORMAL']
            if cursor_pos == window_form.RETURN_BUTTON:
                textstyle = colors.get['HIGHLIGHTED']

            curses.textpad.rectangle(renderer, height - 2, 4, height, 19)
            renderer.addstr(height - 1, 6, '[ESC] Return', textstyle)

            textstyle = colors.get['NORMAL']
            if not form_utils.is_finished(form):
                textstyle = colors.get['ALERT']
            elif cursor_pos == window_form.SUBMIT_BUTTON:
                textstyle = colors.get['HIGHLIGHTED']

            curses.textpad.rectangle(renderer, height - 2, width - 13, height, width)
            renderer.addstr(height - 1, width - 9, 'Submit', textstyle)

            inputs = form['inputs']
            for index in range(len(inputs)):
                input = inputs[index]

                if not input['visible']:
                    continue

                name = input['name'] + ':'

                textstyle = colors.get['NORMAL']
                if not input_utils.is_finished(input):
                    textstyle = colors.get['ALERT']

                if input['required']:
                    symbol = '*'
                else:
                    symbol = ' '

                text_required = symbol

                renderer.addstr(4+index*2, 4, text_required, textstyle)
                renderer.addstr(4+index*2, 6, name, textstyle)

                textstyle = colors.get['NORMAL']
                value = input_utils.to_text(input)
                if input['type'] == 'select':
                    value = value.ljust(12) + '[>]'

                renderer.addstr(4+index*2, width - len(value), value, textstyle)
            
            if cursor_pos >= 0:
                curses.curs_set(2)
                input = inputs[cursor_pos]
                value = input_utils.to_text(input)

                cursor_x = width

                if input['type'] == 'select':
                    cursor_x -= 2
                else:
                    cursor_x += - len(value) + input_utils.get_cursor_pos(input)

                renderer.move(4+cursor_pos*2, cursor_x)
    elif type == POPUP:
        renderer.addstr(2, 2, window['title'], colors.get['RCX_TITLE'])

        textstyle = colors.get['HIGHLIGHTED']

        curses.textpad.rectangle(renderer, height - 2, 4, height, 19)
        renderer.addstr(height - 1, 6, 'Return', textstyle)
    elif type == MODAL:
        renderer.addstr(2, 2, window['title'], colors.get['RCX_TITLE'])

        for index in range(len(window['input']['options'])):
            option = window['input']['options'][index]
            cursor_pos = window['cursor_pos']
            if index == cursor_pos:
                textstyle = colors.get['HIGHLIGHTED']
            else:
                textstyle = colors.get['NORMAL']

            text = option['name']

            if index == window['input']['value']:
                text = '* ' + text
            else:
                text = '  ' + text

            renderer.addstr(4 + index * 2, 6, text, textstyle)

        textstyle = colors.get['NORMAL']
        if cursor_pos == modal.RETURN_BUTTON:
            textstyle = colors.get['HIGHLIGHTED']

        curses.textpad.rectangle(renderer, height - 2, 4, height, 19)
        renderer.addstr(height - 1, 6, 'Return', textstyle)
    elif type == STREAM:
        renderer.addstr(2, 2, window['title'], colors.get['RCX_TITLE'])

        textstyle = colors.get['NORMAL']

        start_pos = 4
        end_pos = height - 3
        size = end_pos - start_pos

        if len(window['result']) == 0:
            renderer.addstr(start_pos + trunc(size / 2), trunc(width / 2) - 4, 'Loading', textstyle)
        else:
            index = window['cursor_pos'] - size + 1
            pos = 0
            bar = get_bar(size, len(window['result']), index)

            while pos < size:
                textstyle = colors.get['NORMAL']
                if index >= 0:
                    line = window['result'][index]
                    renderer.addstr(start_pos + pos, 6, line, textstyle)

                if bar[pos]:
                    textstyle = colors.get['HIGHLIGHTED']

                renderer.addstr(start_pos + pos, width, ' ', textstyle)

                index += 1
                pos += 1

        textstyle = colors.get['HIGHLIGHTED']

        curses.textpad.rectangle(renderer, height - 2, 4, height, 19)
        renderer.addstr(height - 1, 6, 'Return', textstyle)
    elif type == CONFIRM:
        cursor_pos = window['cursor_pos']

        renderer.addstr(2, 2, window['title'], colors.get['RCX_TITLE'])

        textstyle = colors.get['NORMAL']

        if cursor_pos == 0:
            textstyle = colors.get['HIGHLIGHTED']

        curses.textpad.rectangle(renderer, height - 2, 4, height, 10)
        renderer.addstr(height - 1, 6, 'No', textstyle)

        textstyle = colors.get['NORMAL']

        if cursor_pos == 1:
            textstyle = colors.get['HIGHLIGHTED']

        curses.textpad.rectangle(renderer, height - 2, width - 8, height, width)
        renderer.addstr(height - 1, width - 6, 'Yes', textstyle)

    
    if type == POPUP:
        if window['submit']['result'] == '0':
            renderer.attrset(colors.get['POPUP_BORDER_SUCCESS'])
        else:
            renderer.attrset(colors.get['POPUP_BORDER_ERROR'])

    elif window['active']:
        renderer.attrset(colors.get['WINDOW_BORDER_ACTIVE'])
    else:
        renderer.attrset(colors.get['WINDOW_BORDER'])

    renderer.border(0)

    renderer.attrset(0)

    renderer.refresh()

def get_bar(show_size, total_size, pos):
    bar_cons_size = total_size / show_size
    pos2 = pos + show_size
    bar = []
    for i in range(show_size):
        i2 = i * bar_cons_size
        bar.append(i2 > pos and i2 <= pos2)

    return bar

def update(action):
    window = active_window
    type = window['config']['type']
    if type == WINDOW_MENU:
        window_menu.update(window, action)
    elif type == WINDOW_FORM:
        window_form.update(window, action)
    elif type == POPUP:
        popup.update(window, action)
    elif type == MODAL:
        modal.update(window, action)
    elif type == STREAM:
        stream.update(window, action)
    elif type == CONFIRM:
        confirm.update(window, action)

def render():
    for window in windows:
        print_window(window)

def set_active(window):
    global active_window
    active_window['active'] = False
    active_window = window
    active_window['active'] = True
    active_window['updated'] = True
    type = active_window['config']['type']

def return_to_menu():
    set_active(windows[WINDOW_MENU])

def set_form(form):
    global active_window
    set_active(windows[WINDOW_FORM])
    window_form.load_form(active_window, form)

def add_modal(parent_window, input):
    parent_width = parent_window['config']['width']
    parent_height = parent_window['config']['height']

    width = trunc(parent_width / 2)
    height = 10 + 2 * len(input['options'])

    pos_y = trunc((parent_height - height) / 2)
    pos_x = trunc((parent_width - width) / 2)

    renderer = parent_window['renderer'].derwin(height, width, pos_y, pos_x)
    renderer.keypad(1) # Capture input from keypad

    #parent_window['active'] = False

    modal = {}
    modal['input'] = input

    if input['value'] < 0:
        modal['cursor_pos'] = 0
    else:
        modal['cursor_pos'] = input['value']

    modal['parent'] = parent_window
    modal['title'] = input['name']
    modal['renderer'] = renderer
    modal['config'] = { 'type': MODAL, 'height': height, 'width': width, 'pos_y': pos_y, 'pos_y': pos_x }

    modal['updated'] = True

    windows.append(modal)
    set_active(modal)

def add_confirm(parent_window, message, command):
    parent_width = parent_window['config']['width']
    parent_height = parent_window['config']['height']

    width = trunc(parent_width / 2)
    height = 10

    pos_y = trunc((parent_height - height) / 2)
    pos_x = trunc((parent_width - width) / 2)

    renderer = parent_window['renderer'].derwin(height, width, pos_y, pos_x)
    renderer.keypad(1) # Capture input from keypad

    #parent_window['active'] = False

    popup = {}
    popup['parent'] = parent_window
    popup['title'] = message
    popup['cursor_pos'] = 0
    popup['renderer'] = renderer
    popup['config'] = { 'type': CONFIRM, 'height': height, 'width': width, 'pos_y': pos_y, 'pos_y': pos_x }
    popup['command'] = command

    popup['updated'] = True

    windows.append(popup)
    set_active(popup)

def add_stream(parent_window):
    parent_width = parent_window['config']['width']
    parent_height = parent_window['config']['height']

    width = trunc(parent_width / 1.2)
    height = trunc(parent_height / 1.2)

    pos_y = trunc((parent_height - height) / 2)
    pos_x = trunc((parent_width - width) / 2)

    renderer = parent_window['renderer'].derwin(height, width, pos_y, pos_x)
    renderer.keypad(1) # Capture input from keypad

    #parent_window['active'] = False

    form = parent_window['form']

    popup = {}
    popup['parent'] = parent_window
    popup['title'] = form['title']
    popup['renderer'] = renderer
    popup['form'] = form
    popup['result'] = []
    popup['cursor_pos'] = 0
    popup['config'] = { 'type': STREAM, 'height': height, 'width': width, 'pos_y': pos_y, 'pos_y': pos_x }

    popup['updated'] = True

    windows.append(popup)
    set_active(popup)

def add_popup(parent_window, type, message):
    parent_width = parent_window['config']['width']
    parent_height = parent_window['config']['height']

    width = trunc(parent_width / 2)
    height = 10

    pos_y = trunc((parent_height - height) / 2)
    pos_x = trunc((parent_width - width) / 2)

    renderer = parent_window['renderer'].derwin(height, width, pos_y, pos_x)
    renderer.keypad(1) # Capture input from keypad

    #parent_window['active'] = False

    popup = {}
    popup['parent'] = parent_window
    popup['title'] = message
    popup['renderer'] = renderer
    popup['config'] = { 'type': POPUP, 'height': height, 'width': width, 'pos_y': pos_y, 'pos_y': pos_x }
    popup['submit'] = { 'result': type }

    popup['updated'] = True

    windows.append(popup)
    set_active(popup)

def remove_popup(popup):
    set_active(popup['parent'])
    del popup['renderer']
    del popup

def init():

    min_width = 75
    min_height = 35

    global windows, active_window
    screen = curses.initscr() #initializes a new window for capturing key presses
    height, width = screen.getmaxyx()

    if height < min_height or width < min_width:
        raise Exception({'height': height, 'width': width, 'min_height': min_height, 'min_width': min_width})
        
    windows_configs = [
            { 'type': WINDOW_HEADER, 'height': trunc(height/3), 'width': width, 'pos_y': 0, 'pos_x': 0 },
            { 'type': WINDOW_MENU, 'height': ceil(height*2/3), 'width': trunc(width/2), 'pos_y': ceil(height/3)-1, 'pos_x': 0 },
            { 'type': WINDOW_FORM, 'height': ceil(height*2/3), 'width': trunc(width/2), 'pos_y': ceil(height/3)-1, 'pos_x': ceil(width/2) }
    ]
    
    windows = []
    for window_config in windows_configs:
        window = {}
        renderer = curses.newwin(window_config['height'], window_config['width'], window_config['pos_y'], window_config['pos_x']);
        window['config'] = window_config
        window['renderer'] = renderer
        renderer.keypad(1) # Capture input from keypad
        if window['config']['type'] == WINDOW_MENU:
            window_menu.load_menu(window)

        window['updated'] = True
        window['active'] = False

        windows.append(window);

    curses.noecho() # Disables automatic echoing of key presses (prevents program from input each key twice)
    curses.cbreak() # Disables line buffering (runs each key as it is pressed rather than waiting for the return key to pressed)
    colors.init()
    
    # Change this to use different colors when highlighting
    curses.init_pair(1,curses.COLOR_BLACK, curses.COLOR_WHITE) # Sets up color pair #1, it does black text with white background

    active_window = windows[WINDOW_MENU]
    
    set_active(active_window)
