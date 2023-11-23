'''
News Recommendation Structure
Coder: David Ding
Date: 20/06/2023
Version: 1.0
This is the module that interacts with the guardian api and download news info
'''

from library.theguardian import theguardian_content

def download_content_procedure():
    #Global News; Cartoons; Opinion piece; letters (which are what the client required)
    base_url_global = "https://content.guardianapis.com/world"
    base_url_opinion = "https://content.guardianapis.com/commentisfree"
    base_url_letter = "https://content.guardianapis.com/tone/letters"

    #declare variables
    base_urls = [base_url_global,base_url_opinion,base_url_letter]
    all_results = []

    #extract content from the guardian api using my api key
    for base_url in base_urls:
        content = theguardian_content.Content(api='ebae4e36-c37e-4fd8-a487-ff0d3833a5ff',url=base_url)
        
        #get all results of a page
        json_content = content.get_content_response()
        all_results.extend(content.get_results(json_content))
    
    return(all_results)
