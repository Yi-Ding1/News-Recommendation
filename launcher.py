'''
News Recommendation Structure
Coder: David Ding
Date: 21/07/2023
Version: 1.4
This is the home page for the news recommendation software.
'''

import PySimpleGUI as sg
import textwrap
from datetime import date
from library import agent
from library.check_internet import is_connected
from error_message import error_popup
import content
import setting

sg.theme('LightBlue')
sg.SetOptions(font=('Calibri',12,'bold'))

#declare variables
current_date = date.today()
article_toprow = ['Title','Section']
article_rows = []

#get daily news if user connected to internet
if is_connected():
   news_selected = agent.get_news()
else:
   error_popup('No Internet Connection')
   news_selected = []

#modify the selected articles into rows that can be displayed in PSG table
for i in range(len(news_selected)):
    article_row = [textwrap.fill(news_selected[i]['webTitle'],105),news_selected[i]['sectionName']]
    article_rows.append(article_row)

#define the layout of the PSG table
article_table = sg.Table(values=article_rows, headings=article_toprow,
   auto_size_columns=False,
   col_widths=[60,5],
   display_row_numbers=False,
   row_height=50,
   num_rows=4,
   justification='center', key='article_table',
   selected_row_colors='black on light gray',
   enable_events=True,
   expand_x=True,
   expand_y=False,
   enable_click_events=True)

#define the layout of the home page
layout_home = [
    [sg.Text('Home',size=(100,1),justification='center',font=('Calibri',20,'bold'))],
    [article_table],
    [sg.Text(f'Date: {current_date}'),sg.Button('Refresh',size=(8,1)),sg.Button('Setting',size=(8,1))]
]

#create home window
home_window = sg.Window('Monday News',layout_home,size=(1000,700),finalize=True)

#a procedure that opens the home window
def open_home_window():

   #ensure the selected news can be read within the procedure
   global news_selected
   global article_rows

   #a record of which article the user clicked
   clicked_article_tag = []

   #keep the home window open
   while True:

      #check user interaction with the home window
      event, values = home_window.read()
      print("event:", event, "values:", values)

      #user closes the application
      if event == sg.WIN_CLOSED:
         break

      #user refreshes the home page
      elif (event in (None,'Refresh')) & (is_connected()):

         #adjust the decision making on user preference
         undesired_tags = []
         for item in article_rows:
            if (item[1] not in undesired_tags) & (item[1] not in clicked_article_tag):
               undesired_tags.append(item[1])
         agent.update_preference(undesired_tags,"punish")
         clicked_article_tag = []

         #get another set of news
         news_selected = agent.get_news()
         article_rows = []
         for i in range(len(news_selected)):
            article_row = [news_selected[i]['webTitle'],news_selected[i]['sectionName']]
            article_rows.append(article_row)
         home_window.find_element('article_table').update(article_rows)      
      
      #user chooses to open up setting page
      elif event in (None,'Setting'):
         home_window.hide()
         setting.open_setting()
         home_window.un_hide()

      #check which article did the user select and direct the user to the content page
      elif ('+CLICKED+' in event):
         try:
            user_selection = int(event[2][0])
            user_news = news_selected[user_selection]

            #adjust the decision making on user preference
            desired_tags = [user_news['sectionName']]
            clicked_article_tag.append(user_news['sectionName'])
            agent.update_preference(desired_tags,"reward")

            #open up the content window to display article
            home_window.hide()
            content.article_display(user_news['webPublicationDate'],user_news['sectionName'],user_news['webTitle'],user_news['webUrl'],False,article_content='')
            home_window.un_hide()
         except:
            continue

   home_window.close()

   return ()

#launch the program. An error message will be displayed if anything goes wrong
try:
   open_home_window()
except Exception as error:
   error_popup(error)
