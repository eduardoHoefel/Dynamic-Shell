import windows_utils

def update(window, action):
    if action in ['ENTER', 'ESC']:
        windows_utils.remove_popup(window)
