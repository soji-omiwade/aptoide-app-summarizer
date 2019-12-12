from bs4 import BeautifulSoup
from flask import jsonify
import requests


def add_key_value_info(soup, name, app_info):
    for tr_app_info_row in soup.find_all("tr", class_="app-info__row"):
        td_list = tr_app_info_row.find_all("td")
        if td_list and name.lower() in td_list[0].text.lower():
            app_info[name] = td_list[1].text


def extract_info(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        app_info = {}

        #the two lines below get the necessary information
        for name in ("Name", "Downloads", "Version", "Release date"):
            add_key_value_info(soup, name, app_info)            
        app_info["Description"] = soup.find(class_="view-app__description")\
        .find("p", itemprop="description").text
                
       
        jsonData = []
        for feature in app_info:
            jsonData.append({'feature': feature, 'value': app_info[feature]})
        return jsonData
    except requests.ConnectionError:
        return jsonify({'error': 'unable to connect'})
    except requests.exceptions.MissingSchema:
        return jsonify({'error': 'missing http://'})
    except(Exception) as e:
        return jsonify({'error': 'unknown'})