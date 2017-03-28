
def update(window, action):
    from src.windows import windows_utils
    if action in ['ENTER', 'ESC']:
        windows_utils.remove_popup(window)
