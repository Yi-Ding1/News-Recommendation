'''
News Recommendation Structure
Coder: David Ding
Date: 21/07/2023
Version: 1.5
This is the content page for the news recommendation software.
'''

import PySimpleGUI as sg
import textwrap
from library import web_scrape
from library import agent
from datetime import date
from time import time
from csv import writer
from csv import reader
from os import path
sg.theme('LightBlue')
sg.SetOptions(font=('Calibri',12,'bold'))

#get current date for reading record
current_date = date.today()

#a function that adds the article to the reading record
def add_reading_record(article_title,url):
    file_dir = path.dirname(__file__)+'\\assets\\reading_record.csv'
    new_record = [[current_date,article_title,url]]

    #get content of existing csv reading record file and check if the article is already read
    with open(file_dir,'r',encoding='utf-8') as csvfile:
        readin = reader(csvfile)
        for line in readin:

            #existence check. Prevent repeating rows being recorded.
            if line[1] == article_title:
                continue
            else:
                new_record.append(line)

    #rewrite the reading record csv file with the new record
    with open(file_dir, 'w', newline='',encoding='utf-8') as csvfile:
        write = writer(csvfile)
        write.writerows(new_record)

    return()

#a function that will save an article to the favourite category
def add_fav_article(publication_date,section_name,article_title,url,article_content):

    #record the favourite article in csv file
    file_dir_csv = path.dirname(__file__)+'\\assets\\favourite_articles.csv'
    new_record = [[current_date,article_title,publication_date,section_name,url,repr(article_content)]]

    #get content of existing csv favourite article record file
    with open(file_dir_csv,'r',encoding='utf-8') as csvfile:
        readin = reader(csvfile)
        for line in readin:

            #check if the article is already saved to the favourite category
            if line[1] == article_title:
                return()
            else:
                new_record.append(line)

    #rewrite the favourite articles file with the new record
    with open(file_dir_csv, 'w', newline='',encoding='utf-8') as csvfile:
        write = writer(csvfile)
        write.writerows(new_record)

    return()

#update the total reading time
def update_reading_time(start_time):

    #get the current time, subtract it with the initial time to get how long the user has been doing reading
    end_time = time()
    time_elapsed = int(end_time - start_time)
    file_dir_rt = path.dirname(__file__)+"\\assets\\reading_time.txt"

    with open(file_dir_rt,'r') as open_file:
        total_reading_time = int(open_file.readline()) + time_elapsed
    with open(file_dir_rt,'w') as open_file:
        open_file.write(str(total_reading_time))

    return()

#a function that calls the content window to display the article
def article_display(publication_date,section_name,article_title,url,is_fav_article,article_content):

    #declare variables
    add_reading_record(article_title,url)
    start_time = time()

    #record the state of all the buttons
    like_btn_state = False
    dislike_btn_state = False

    #check whether user already saved this article to favourite
    if not is_fav_article:
        article_text = web_scrape.scrape_news(url)
        column_text = [[sg.Text(f'{article_text}',font=('Helvetica',11))]]
        fav_btn_state = False
    else:
        article_text = article_content
        column_text = [[sg.Text(f'{article_text}')]]
        fav_btn_state = True

    #define the layout of the content page
    layout_content = [
        [sg.Text(f'{article_title}',font=('Calibri',14,'bold'))],
        [sg.Text(f'• Section: {section_name}')],
        [sg.Text(f'• Publication: {publication_date}')],
        [sg.Text(f'• Source: {textwrap.fill(url,130)}')],
        [sg.Column(column_text,size=(950,500),scrollable=True,vertical_scroll_only=True)],
        [sg.Button('Like',size=(8,1)),sg.Button('Dislike',size=(8,1)),sg.Button('Favourite',size=(8,1)),sg.Button('Back',size=(8,1))]
    ]

    #create the content page
    content_window = sg.Window('Monday News',layout_content,size=(1000,700),finalize=True)

    #keep the content page open
    while True:
        event, values = content_window.read()
        print("event:", event, "values:", values)

        #user chooses to close the window
        if (event == sg.WIN_CLOSED) | (event in (None,'Back')):
            update_reading_time(start_time)
            break

        #if user likes the article. Update user's tag preference
        elif (event in (None,'Like')) & (like_btn_state == False) & (dislike_btn_state == False):
            tag = [section_name]
            agent.update_preference(tag,"reward")
            like_btn_state = True
            content_window.find_element('Like').update(button_color='grey')

        #if user dislikes the article. Update user's tag preference
        elif (event in (None,'Dislike')) & (dislike_btn_state == False) & (like_btn_state == False):
            tag = [section_name]
            agent.update_preference(tag,"punish")
            dislike_btn_state = True
            content_window.find_element('Dislike').update(button_color='grey')

        #if user saves the article to the favourite category
        elif (event in (None,'Favourite')) & (fav_btn_state == False):
            sg.Popup('Article Saved to Favourite!')
            add_fav_article(publication_date,section_name,article_title,url,article_text)
            fav_btn_state = True
            content_window.find_element('Favourite').update(button_color='grey')

    content_window.close()

    return()
