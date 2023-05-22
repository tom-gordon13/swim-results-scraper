import requests
from bs4 import BeautifulSoup
from copy import deepcopy

from selenium_packages import *
import re

from data_models import swimmer_model, relay_model
from get_team_name import get_team_name


import re


def extract_integer(url):
    match = re.search('/times/(\d+)/splashsplits/', url)
    if match:
        return match.group(1)
    else:
        return None


url_response_prefix = 'https://www.swimcloud.com/'


def get_data_urls(url):
    # Send a GET request to the URL
    response = requests.get(url)

    # If the GET request is successful, the status code will be 200
    if response.status_code == 200:
        # Get the content of the response
        page_content = response.content

        # Create a BeautifulSoup object and specify the parser
        soup = BeautifulSoup(page_content, 'html.parser')

        # Find all <a> tags with a 'data-url' attribute that starts with '/times/'
        a_tags = soup.find_all('a', attrs={'data-url': True})

        # Filter out those tags whose 'data-url' doesn't start with '/times/'
        times_urls = [tag['data-url']
                      for tag in a_tags if tag['data-url'].startswith('/times/')]

        return times_urls


page_url = 'https://www.swimcloud.com/results/236950/event/21/'
# page_url = 'https://www.swimcloud.com/results/118612/event/21/0/'
html_content = requests.get(page_url)
soup_full_page = BeautifulSoup(html_content.text, 'html.parser')

meet_date = soup_full_page.find("li", {"id": "meet-date"}).text


url_response_list = get_data_urls(page_url)

team_list = []

for url_endpoint in url_response_list:

    response = requests.get(url_response_prefix + url_endpoint)

    # The response will be HTML, so parse it with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Now you can find elements in the HTML using BeautifulSoup's methods
    # For example, to find a div with class 'response-object':
    response_rows = soup.find_all('tr')
    # print(response_rows)

    new_team_model = deepcopy(relay_model)
    response_integer = extract_integer(url_endpoint)
    new_team_model['school'] = get_team_name(soup_full_page, response_integer)
    new_team_model['date'] = meet_date
    new_team_model['year'] = meet_date[-4:]

    for row in response_rows:

        tds = row.find_all('td', class_='u-text-semi')
        if tds:
            val = tds[0].text.strip()
            if val.replace(".", "").isnumeric():
                new_team_model['swimmers'][-1]['relay_split'] = val
            else:
                new_swimmer_obj = swimmer_model.copy()
                new_swimmer_obj['name'] = val
                new_team_model['swimmers'].append(new_swimmer_obj)

    team_list.append(new_team_model)

print(team_list)
