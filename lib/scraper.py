from bs4 import BeautifulSoup
from flask import jsonify
import requests
from enum import Enum 

AppFeature = Enum("
name.name, AppFeature.downloads.name, AppFeature.version.name, AppFeature.release_date:

def add_key_value_info(soup, name, app_info):
    for tr_app_info_row in soup.find_all("tr", class_="app-info__row"):
        td_list = tr_app_info_row.find_all("td")
        if td_list and name.lower() in td_list[0].text.lower():
            app_info[name] = td_list[1].text



"""
>>> for br in k.find_all("br"):
...   br.replace_with("\n")
...
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
>>> k
<p itemprop="description">Looking for the most talked about TV programmes and films from the around the world? They’re all on Netflix.

We’ve got award-winning series, films, documentaries and stand-up specials. And with the mobile app, you get Netflix while you travel, commute, or just take a break.

What you’ll love about Netflix:

• We add TV programmes and films all the time. Browse new titles or search for your favourites, and stream videos straight to your device.
• The more you watch, the better Netflix gets at recommending TV programmes and films you’ll love.
• Create up to five profiles for an account. Profiles give different members of your household their own personalised Netflix.
• Enjoy a safe watching experience just for children with family-friendly entertainment.
• Preview quick videos of our series and films and get notifications for new episodes and releases.
• Save your data. Download titles to your mobile device and watch offline, wherever you are.

For complete terms and conditions, please visit http://www.netflix.com/termsofuse
For privacy statement, please visit http://www.netflix.com/privacy
</p>
"""
def extract_info(url):


    try:
        response = requests.get(url)
        content = clear_br_
        soup = BeautifulSoup(response.content, 'html.parser')
        
        app_info = {}

        app_info[AppFeature.description.name] = 
                soup.find(class_="view-app__description")\
                .find("p", itemprop="description").text

        #the two lines below get the necessary information
        for name in AppFeature:
            if name != AppFeature.description:
                add_key_value_info(soup, name, app_info)
                
                
        json_data = []
        for feature in app_info:
            json_data.append({'feature': feature, 'value': app_info[feature]})
        return json_data
    except requests.ConnectionError:
        return jsonify({'error': 'unable to connect'})
    except requests.exceptions.MissingSchema:
        return jsonify({'error': 'missing http://'})
    except(Exception) as e:
        return jsonify({'error': 'unknown'})