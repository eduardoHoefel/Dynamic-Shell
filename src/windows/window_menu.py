from src.log import log

def load_menu(window):
    import json
    
    with open('assets/menu.json') as json_data:
        json_object = json.load(json_data)

    options = json_object['options']
    title = json_object['title']

    menu = {}
    menu['options'] = options
    menu['title'] = title
    window['menu'] = menu
    window['cursor_pos'] = 0
    window['updated'] = True
    enter_menu(window, json_object)

def enter_menu(window, menu):
    new_menu = {}
    new_menu['options'] = menu['options']
    new_menu['title'] = menu['title']
    new_menu['parent'] = window['menu']
    window['menu']['cursor_pos'] = window['cursor_pos']
    window['menu'] = new_menu

def return_menu(window):
    if 'parent' in window['menu']:
        window['menu'] = window['menu']['parent']
        return window['menu']['cursor_pos']

    from src import main
    main.close()
    return 0

def update(window, action):
    menu = window['menu']
    options = menu['options']
    length = len(options)

    cursor_pos = window['cursor_pos']

    if action == 'DOWN_ARROW':
        cursor_pos += 1;
        window['updated'] = True
    elif action == 'UP_ARROW':
        cursor_pos -= 1;
        window['updated'] = True
    elif action == 'ENTER':
        cursor_pos = enter(window)
        window['updated'] = True
    elif action in ['ESC', 'BACKSPACE']:
        cursor_pos = return_menu(window)
        window['updated'] = True
    else:
        for index in range(len(options)):
            if str(options[index]['hotkey']) == str(action):
                window['cursor_pos'] = index
                cursor_pos = enter(window)
                window['updated'] = True
                break

    if (cursor_pos < 0):
        cursor_pos = length - 1
    elif (cursor_pos >= length):
        cursor_pos = 0

    window['cursor_pos'] = cursor_pos

def enter(window):
    menu = window['menu']
    options = menu['options']
    cursor_pos = window['cursor_pos']
    selected_option = options[cursor_pos]
    type = selected_option['type']
    
    if type == 'MENU':
        enter_menu(window, selected_option['menu'])
        cursor_pos = 0
    elif type == 'FORM':
        from src.windows import windows_utils
        windows_utils.set_form(selected_option['form'])
    elif type == 'COMMAND':
        if 'confirm' in selected_option:
            from src.windows import windows_utils
            windows_utils.add_confirm(window, selected_option['confirm'], selected_option['command'])
        else:
            from src import os_utils
            os_utils.execute(selected_option['command'])
    elif type == 'RETURN':
        cursor_pos = return_menu(window)

    return cursor_pos
