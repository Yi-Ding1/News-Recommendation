'''
News Recommendation Structure
Coder: David Ding
Date: 05/07/2023
Version: 1.1
This is the module that learns from the tag preference table 
and select the appriopriate news articles.
'''

from random import random
from csv import writer
from os import path

#this function updates the tags preference csv file based on given tag preference table
def tag_preference_update(tag_preference_table):
    file_dir = path.dirname(__file__)+'\\tags_preference.csv'

    with open(file_dir, 'w', newline='') as file:
        write = writer(file)
        write.writerows(tag_preference_table)

    return()

#this function decides which news articles will be chosen.
#tag preference is a 2-dim list and daily_news is a record of all the news articles
def news_selection(tag_preference_table,daily_news):

    #declare variables
    probability_array = []
    news_selected_index = []
    probability_distribute_array = []
    news_selected = []

    #extract all the news articles tags from daily news
    for item in daily_news:
        item_tag = item['sectionName']
        tag_found = False

        #check if the tag of the article is already in the tag preference table (existence check)
        #if yes, then get the value of the tag
        for tag in tag_preference_table:
            if tag[0] == item_tag:
                probability_array.append(float(tag[1]))
                tag_found = True
                break
        
        #if tag not found, then add the tag to the preference table and initialize its value to 1.0
        if not tag_found:
            tag_preference_table.append([item_tag,1])
            tag_preference_update(tag_preference_table)
            probability_array.append(1)
    
    #get the total value of all the tags
    total_score = sum(probability_array)
    probability_distribute_array.append(probability_array[0]/total_score)

    #get the probability each article will be selected through learning their values
    for i in range(1,len(probability_array)):
        percentage = probability_distribute_array[-1]+probability_array[i]/total_score
        probability_distribute_array.append(percentage)

    #randomly select an article based on the given probability, 4 articles will be chosen
    while (len(news_selected_index)) < 4:
        selected_new = random()
        for i in range(len(probability_distribute_array)):

            #existence check of whether the article is already selected
            if (probability_distribute_array[i] >= selected_new) & (i not in news_selected_index):
                news_selected_index.append(i)
                break
    
    #get the details of the selected news article
    for index in news_selected_index:
        news_selected.append(daily_news[index])
    
    return news_selected
