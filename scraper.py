from bs4 import BeautifulSoup
from flask import jsonify
import requests
from enum import Enum 

AppFeature = Enum("AppFeature", 
    "App-Name Version Number-of-Downloads Release-Date Description")

def checkProtocol(url):
    # Validate argument starts with http or https
    return url.startswith('http://') or url.startswith('https://')

def add_description_key_value_info(soup, app_info):
    description_tag_with_breaks = soup.find(class_="view-app__description").\
        find("p", itemprop="description")
    app_info[AppFeature.Description] = description_tag_with_breaks.text
    
def add_available_key_value_info(soup, app_info):
    """ as long as the detailed information exists we can scrape
        the website for everything except the description
        
        the two lines below get the necessary information
        #description is not there, but the method gracefully moves past it
    """
    
    
    """
    TODO: this can be optimized: 
        think next sibling from beautiful-soup
        also should be able to get rid of the explicit for on app-info_row
    """
    for tr_app_info_row in soup.find_all("tr", class_="app-info__row"):
        td_list = tr_app_info_row.find_all("td")
        if td_list: 
            for feature in AppFeature:
                if feature.name.lower().replace("-"," ") \
                        == td_list[0].text.lower().strip().replace(":", ""):
                    app_info[feature] = td_list[1].text
                    
def extract_info(url):


    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        app_info = {}

        add_available_key_value_info(soup, app_info)
        add_description_key_value_info(soup, app_info)
                
        json_data = []
        for feature in app_info:
            json_data.append\
                ({'feature': feature.name, 'value': app_info[feature]})
        return json_data
    except requests.ConnectionError:
        return jsonify({'error': 'unable to connect'})
    except requests.exceptions.MissingSchema:
        return jsonify({'error': 'missing http://'})
    except(Exception) as e:
        raise e
        return jsonify({'error': 'unknown'})