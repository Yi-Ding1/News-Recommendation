'''
News Recommendation Structure
Coder: David Ding
Date: 14/07/2023
Version: 1.0
This displays an error message if something wrong occurs in any of the modules
'''

import PySimpleGUI as sg

def error_popup(reason):
    sg.Popup(f'Something went wrong...\nReason: {reason}')
    return()
    