import requests
from bs4 import BeautifulSoup

from selenium_packages import *
import re

from data_models import swimmer_model, relay_model

# Set up the Selenium web driver
# driver = webdriver.Chrome()
# dev_tools = driver.execute_cdp_cmd("Network.enable", {})

# Navigate to the webpage with the button
# driver.get('https://www.swimcloud.com/results/236950/event/21/')
# wait = WebDriverWait(driver, 10)
# links = wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, 'div')))

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


url_response_list = get_data_urls(page_url)


for url_endpoint in url_response_list:

    response = requests.get(url_response_prefix + url_endpoint)

    # The response will be HTML, so parse it with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Now you can find elements in the HTML using BeautifulSoup's methods
    # For example, to find a div with class 'response-object':
    response_rows = soup.find_all('tr')
    # print(response_rows)

    new_team_model = relay_model
    new_team_model['school'] = 'Florida'

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

        print(new_team_model)


exit()

# Replace with the API endpoint URL you found
url = 'https://www.swimcloud.com/times/99626707/splashsplits/'


# response = requests.get(url, params=params, headers=headers)
response = requests.get(url)

# The response will be HTML, so parse it with BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Now you can find elements in the HTML using BeautifulSoup's methods
# For example, to find a div with class 'response-object':
response_rows = soup.find_all('tr')
# print(response_rows)

new_team_model = relay_model
new_team_model['school'] = 'Florida'

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

print(new_team_model)

# To get the text of the response object:
# response_text = response_object.get_text()

# Now you can process the data however you need to
# print(response_text)
