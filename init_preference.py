'''
News Recommendation Structure
Coder: David Ding
Date: 12/07/2023
Version: 1.0
This is the initialize preference page for the news recommendation software.
'''

import PySimpleGUI as sg
from library import agent
sg.theme('LightBlue')
sg.SetOptions(font=('Calibri',12,'bold'))

def open_pref_window():

    #list the relevant topics that user can choose
    topics = [
    ['Environment','Education','Society'],
    ['Media','Life and style','World news'],
    ['Politics','Culture','Music'],
    ['Opinion','Money','Global']
    ]
    checkbox = []
    preferred_tags = []

    #create the checkboxes based on the topics
    for row in topics:
        cb_row = []
        for item in row:
            cb_row.append(sg.Checkbox(item))
        checkbox.append(cb_row)

    #define the layout of the initialize preference window
    layout_init = [
        [sg.Text('Choose your preferred topics:')],
        [checkbox],
        [sg.Button('Confirm'),sg.Button('Cancel')]
    ]

    #create the window
    init_window = sg.Window('Monday News',layout_init,size=(400,300),finalize=True)
    
    #keep the window open
    while True:

        #check for user interaction with the application
        event, values = init_window.read()
        print("event:", event, "values:", values)

        #close the initialize preference window
        if (event == sg.WIN_CLOSED) | (event in (None,'Cancel')):
            break

        #initialize user preference
        elif event in (None,'Confirm'):

            #check which checkboxes are ticked and record the preferred tags
            for row in checkbox:
                for item in row:
                    if item.get() == True:
                        preferred_tags.append(item.Text)
            agent.update_preference(preferred_tags,"set_score")
            sg.Popup('Preference Initialized.')
    init_window.close()

    return()
