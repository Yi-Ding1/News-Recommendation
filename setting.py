'''
News Recommendation Structure
Coder: David Ding
Date: 21/07/2023
Version: 1.3
This is the setting page for the news recommendation software.
'''

import webbrowser
from csv import reader
from os import path
from ast import literal_eval
import PySimpleGUI as sg
import textwrap
import init_preference
import content
sg.theme('LightBlue')
sg.SetOptions(font=('Calibri',12,'bold'))

#a procedure that opens the setting page
def open_setting():

    #declare variables
    table_toprow = ['Date','Article']
    record_rows = []
    favourite_rows = []
    file_dir_record = path.dirname(__file__)+"\\assets\\reading_record.csv"
    file_dir_fav = path.dirname(__file__)+"\\assets\\favourite_articles.csv"
    file_dir_rt = path.dirname(__file__)+"\\assets\\reading_time.txt"
    article_links = []
    
    #get the reading time from the .txt file and convert the time into day, hr and min
    with open(file_dir_rt,'r') as open_file:
        total_reading_time = int(open_file.readline())
        trt_day = total_reading_time // 86400
        trt_hour = (total_reading_time % 86400) // 3600
        trt_min = (total_reading_time % 3600) // 60

    #get the reading record and sort them into a list for display and another list for article links
    with open(file_dir_record,'r',encoding='utf-8') as csvfile:
        readin = reader(csvfile)
        for line in readin:
            record_rows.append([line[0],textwrap.fill(line[1],70)])
            article_links.append(line[2])

    #get the list of favourite articles
    with open(file_dir_fav,'r',encoding='utf-8') as csvfile:
        readin = reader(csvfile)
        for line in readin:
            favourite_rows.append(line)

    #define the layout for the reading record table
    record_table = sg.Table(values=record_rows, headings=table_toprow,
    auto_size_columns=False,
    size=[1,5],
    col_widths=[5,60],
    row_height=45,
    display_row_numbers=False,
    justification='center', key='rec_table',
    selected_row_colors='black on light gray',
    enable_events=True,
    expand_x=True,
    expand_y=False,
    enable_click_events=True)

    #define the layout for the favourite articles table
    favourite_table = sg.Table(values=favourite_rows, headings=table_toprow,
    auto_size_columns=False,
    size=[1,5],
    col_widths=[5,60],
    row_height=45,
    display_row_numbers=False,
    justification='center', key='fav_table',
    selected_row_colors='black on light gray',
    enable_events=True,
    expand_x=True,
    expand_y=True,
    enable_click_events=True)

    #define the layout for the setting window
    layout_setting = [
        [sg.Text('Setting',size=(100,1),justification='center',font=('Calibri',20,'bold'))],
        [sg.Text('Total reading time'),sg.Text(f'{trt_day} days {trt_hour} hours {trt_min} minutes',size=(22,1),background_color='white')],
        [sg.Text('Reading record')],
        [record_table],
        [sg.Text('Favourite articles')],
        [favourite_table],
        [sg.Text('Initialize preference'),sg.Button('Confirm')]
    ]

    #create the setting window
    setting_window = sg.Window('Monday News',layout_setting,size=(1000,700),finalize=True)

    #keep the setting window open
    while True:

        #check user interaction with the setting window
        event, values = setting_window.read()
        print("event:", event, "values:", values)

        #user closes the window
        if event == sg.WIN_CLOSED:
            break

        #if user clicks the record table, they get directed to the relevant article in their browser
        elif ('+CLICKED+' in event) &  ('rec_table' in event):
            try:
                webbrowser.open(article_links[int(event[2][0])])
            except:
                pass

        #if user clicks the favourite article table, they get directed to the content page
        elif ('+CLICKED+' in event) &  ('fav_table' in event):
            try:
                fav_article = favourite_rows[int(event[2][0])]
                article_title = fav_article[1]
                publication_date = fav_article[2]
                section_name = fav_article[3]
                url = fav_article[4]
                article_content = literal_eval(fav_article[5])
                setting_window.hide()
                content.article_display(publication_date,section_name,article_title,url,True,article_content)
                setting_window.un_hide()
            except:
                pass

        #if user chooses to initialize their preference
        elif event in (None,'Confirm'):
            setting_window.hide()
            init_preference.open_pref_window()
            setting_window.un_hide()

    setting_window.close()
