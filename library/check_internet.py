'''
News Recommendation Structure
Coder: David Ding
Date: 14/07/2023
Version: 1.0
This procedure checks whether the user is connected to the Internet
'''

import urllib.request

#check for internet connection through connecting to google.com
def is_connected():
    try:
        urllib.request.urlopen('http://google.com')
        return True
    except:
        return False
