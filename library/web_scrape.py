'''
News Recommendation Structure
Coder: David Ding
Date: 16/07/2023
Version: 1.0
This is the function that downloads paragraphs based on url.
'''

from urllib.request import urlopen
from bs4 import BeautifulSoup
import textwrap

#takes the input of a url link and return a string
def scrape_news(url):
    
    #open the url and extract the html content
    html = urlopen(url)
    soup = BeautifulSoup(html,'html.parser')
    paragraph = ''

    #find all the sections with <p> which are the paragraphs
    for new_para in soup.find_all("p"):
        paragraph_formatted = textwrap.fill(new_para.get_text(),width=125)
        if paragraph != '':
            paragraph = f'{paragraph}\n\n{paragraph_formatted}'
        else:
            paragraph = paragraph_formatted
    
    return(paragraph)
