from curses import *

get = {
        'RCX_TITLE': 0,
        'MENU_TITLE': 1,
        'FORM_TITLE': 2,
        'NORMAL': 3,
        'HIGHLIGHTED': 4,
        'ALERT': 5,
        'WINDOW_BORDER': 6,
        'WINDOW_BORDER_ACTIVE': 7,
        'POPUP_BORDER_SUCCESS': 8,
        'POPUP_BORDER_ERROR': 9
}

def init():
    noecho()
    raw()
    
    start_color()
    use_default_colors()

    get['NORMAL'] = A_NORMAL
    get['MENU_TITLE'] = A_BOLD
    get['HIGHLIGHTED'] = color_pair(1)
    set_color('ALERT', COLOR_WHITE, COLOR_RED)
    set_color('WINDOW_BORDER', COLOR_BLUE, COLOR_BLACK)
    get['WINDOW_BORDER_ACTIVE'] = get['WINDOW_BORDER'] | A_BOLD
    set_color('RCX_TITLE', COLOR_BLUE, COLOR_BLACK)
    set_color('POPUP_BORDER_SUCCESS', COLOR_GREEN, COLOR_BLACK)
    set_color('POPUP_BORDER_ERROR', COLOR_RED, COLOR_BLACK)

def set_color(key, fg, bg):
    init_pair(get[key], fg, bg)
    get[key] = color_pair(get[key])
