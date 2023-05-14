import requests
from bs4 import BeautifulSoup


page_url = 'https://www.swimcloud.com/results/236950/event/21/'

html_content = requests.get(page_url)

# Create a BeautifulSoup object and specify the parser
soup = BeautifulSoup(html_content.text, 'html.parser')


def get_team_name(page_html, tag_num):

    # Find the <tr> element containing an <a> with a 'data-url' attribute containing '99626707'
    tr_element = soup.find(lambda tag: tag.name == 'tr' and tag.find(
        'a', attrs={'data-url': lambda x: x and tag_num in x}))

    team_name = tr_element.find('span').text

    return team_name
