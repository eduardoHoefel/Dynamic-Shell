#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Topmenu and the submenus are based of the example found at this location http://blog.skeltonnetworks.com/2010/03/python-curses-custom-menu/
# The rest of the work was done by Matthew Bennett and he requests you keep these two mentions when you reuse the code :-)
# Basic code refactoring by Andrew Scheller

from time import sleep
import curses, os #curses is the interface for capturing key presses on the menu, os launches the files
import windows_utils
import keys_utils
import os_utils
from log import log

action = 0
open = True

def init():
    windows_utils.init()

# Main program
def main():
    init()
    global open
    while True:
        update()
        render()

        if not open:
            break

        get_input()

    curses.endwin()
    curses.curs_set(1)
    curses.reset_shell_mode()
    curses.echo()
    os.system('clear')
    exit()

def get_input():
    global action
    active_window = windows_utils.active_window
    action = keys_utils.get_input(active_window)

def update():
    global action
    if action == 'NONE':
        return

    windows_utils.update(action)

    action = 'NONE'

def render():
    windows_utils.render()

def close():
    global open
    open = False
    exit()
