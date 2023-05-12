import requests
from bs4 import BeautifulSoup

relay_model = {
    'school': None,
    'year': None,
    'swimmers': []
}


swimmer_model = {
    'name': None,
    'relay_split': None
}


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
            print(f'Split - {float(val)}')
            print('----------')
        else:
            new_swimmer_obj = swimmer_model.copy()
            new_swimmer_obj['name'] = val
            print(new_swimmer_obj)
            new_team_model['swimmers'].append(new_swimmer_obj)
            print(new_team_model)

print(new_team_model)

# To get the text of the response object:
# response_text = response_object.get_text()

# Now you can process the data however you need to
# print(response_text)
