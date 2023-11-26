# Install packages when required
"""
!pip install requests
!pip install html5lib
!pip install bs4
"""

import requests
from bs4 import BeautifulSoup
import csv

# make user input prompts for city, state
# city = input('Please Enter City Name')
# for now, using hard-coded input for city and state
city = 'San-Jose'
state = 'CA'
URL = f'https://www.realtor.com/realestateandhomes-search/{city}_{state}'
#print(URL)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Referer': 'https://www.google.com/',
    'DNT': '1',
    'Upgrade-Insecure-Requests': '1',
    'TE': 'Trailers'
}

session = requests.Session()
session.headers.update(headers)
try:
    response = session.get(URL)
    response.raise_for_status()
except requests.exceptions.RequestException as e:
    print(f'Error in getting response from web:\n {e}')

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html5lib')
else:
    exit()

soup.prettify()

# navigate to properties list container
properties_list = soup.find('section', attrs = {'class':'PropertiesList_propertiesContainer__HTNbx PropertiesList_listViewGrid__U_BlK'})
#properties_list.prettify()

"""We have to find

* Property listing title
* Property price
* Property URL
"""

# list to hold all properties
prop_list = []

# Move to each Card/Property result
property_placeholder = properties_list.findAll('div',attrs={'class':'BasePropertyCard_propertyCardWrap__Z5y4p'})
for prop in property_placeholder:
    prop_dict = {}
    # find card contents which contains detail regarding each property
    card_content = prop.find('div',attrs={'data-testid':'card-content'})

    # extract price of each property
    try:
        price = card_content.find('div',attrs={'data-testid':'card-price'})
        print(price.text)
        prop_dict['price'] = price.text
    except Exception as e:
        print(f'Error occur in extracting price:\n {e}')
        prop_dict['price'] = '-'
  # get property link
    try:
        link = card_content.find('a',attrs={'class':'LinkComponent_anchor__0C2xC'})
        link_url = 'https://www.realtor.com/'+link['href'].split('?')[0]
        print(link_url)
        prop_dict['link'] = link_url
    except Exception as e:
        print(f'Error occur in extracting link:\n {e}')
        prop_dict['link'] = '-'
    try:
        title_card = card_content.findAll('div',attrs={'class':'content-col-left'})
        title = [t.text for t in title_card]
        print(', '.join(title))
        prop_dict['title'] = ', '.join(title)
    except Exception as e:
        print(f'Error occur in extracting title:\n {e}')
        prop_dict['title'] = '-'
    prop_list.append(prop_dict)

filename = 'properties_data.csv'
with open(filename, 'w', newline='') as file:
	writer = csv.DictWriter(file,['title','price','link'])
	writer.writeheader()
	for prop in prop_list:
		writer.writerow(prop)

"""## TODOs
Navigate to all pages one by one
"""