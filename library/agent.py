'''
News Recommendation Structure
Coder: David Ding
Date: 18/07/2023
Version: 1.2
This is the module that acts as a bridge between the user interface and all the relevant modules
'''

from library import learning_model as lm
from library import download_content as dc
from csv import reader
from os import path
from math import sqrt

#a procedure that reads the tags preference csv file
def get_tag_preference_table():
    file_dir = path.dirname(__file__)+"\\tags_preference.csv"
    tags_preference_table = []

    with open(file_dir,'r') as csvfile:
        readin = reader(csvfile)
        for line in readin:
            tags_preference_table.append(line)
    
    return(tags_preference_table)

#a procedure that download the news info, get the tag preference table
#and asks the learning model to evaluate which articles are more suitable
def get_news():

    daily_news = dc.download_content_procedure()
    tags_preference_table = get_tag_preference_table()
    news_selected = lm.news_selection(tags_preference_table,daily_news)
    print(f"number of news found: {len(daily_news)}")

    return(news_selected)

#a function that updates the user preference table
def update_preference(tags,action):
    
    #get existing tag preference table
    tags_preference_table = get_tag_preference_table()

    for tag in tags:
        for i in range(len(tags_preference_table)):
            if tags_preference_table[i][0] == tag:

                #increase the value for desired tags
                if action == "reward":
                    tags_preference_table[i][1] = sqrt(float(tags_preference_table[i][1])) + 1.1
                    break

                #decrease the value for undesired tags
                elif action == "punish":
                    tags_preference_table[i][1] = float(tags_preference_table[i][1]) * (6/11) + 0.2
                    break

                #initialize user preference
                elif action == "set_score":
                    tags_preference_table[i][1] = 2.5
                    break
    
    #update the tag preference table
    lm.tag_preference_update(tags_preference_table)

    return()
