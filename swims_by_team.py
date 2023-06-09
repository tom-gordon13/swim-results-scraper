from collections import Counter
import re
import json
import requests
from bs4 import BeautifulSoup

# Texas team page
page_url = 'https://www.swimcloud.com/results/194776/team/105/swims/'


def count_indiv_swims(url):

    count__indiv_swims = {}

    # Use regex to find all instances of 'swimmer/<integer>/'
    pattern = re.compile(r'swimmer/(\d+)/')

    for num in range(1, find_largest_pagination(url=page_url)+1):

        new_url = url + f'?page={num}'
        print(new_url)

        # Get the HTML content of the webpage
        response = requests.get(new_url)
        html_content = response.text

        # Parse the HTML content
        soup = BeautifulSoup(html_content, 'html.parser')
        html_text = str(soup)
        matches = pattern.findall(html_text)

        # Count the occurrences of each integer

        for match in matches:
            if match in count__indiv_swims:
                count__indiv_swims[match] += 1
            else:
                count__indiv_swims[match] = 1

    # Return the count__indiv_swims as a JSON object
    return count__indiv_swims


def find_largest_pagination(url):
    # Get the HTML content of the webpage
    response = requests.get(url)
    html_content = response.text

    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all elements with class name 'c-pagination__action'
    elements = soup.find_all(class_='c-pagination__action')

    if not elements:  # If no elements exist, return 1
        return 1

    max_val = 1
    for element in elements:
        curr_val = element.get_text().strip()
        if not curr_val.isdigit():
            continue

        max_val = max(int(curr_val), max_val)

    return max_val


swim_counts = count_indiv_swims(url=page_url)


def find_relay_links(url):
    # Download the page
    response = requests.get(url)
    response.raise_for_status()  # Raise exception if the request failed

    # Parse the HTML content of the page with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all elements with a class of 'c-nav__item' and an href matching the pattern
    matching_elements = soup.find_all(
        lambda tag: tag.get('class') == ['c-nav__item'] and
        re.match(r'/results/\d+/event/\d+/', tag.get('href', '')) and
        tag.find('div', attrs={'title': re.compile(r'\bRelay\b', re.I)})
    )

    # Get the href attribute of each matching element
    hrefs = [element.get('href') for element in matching_elements]

    return hrefs


meet_dashboard_url = 'https://www.swimcloud.com/results/236950/'
url_prefix = 'https://www.swimcloud.com'

relay_urls = find_relay_links(url=meet_dashboard_url)


# HAVE NOT TESTED YET


def count_swimmer_ids(url):
    # Download the page
    response = requests.get(url)
    response.raise_for_status()  # Raise exception if the request failed

    # Parse the HTML content of the page with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all elements with an href matching the pattern
    matching_elements = soup.find_all(
        href=re.compile(r'/results/\d+/swimmer/\d+/'))

    # Get the href attribute of each matching element
    hrefs = [element.get('href') for element in matching_elements]

    # Extract the swimmer id (integer2) from each href
    swimmer_ids = [re.search(r'/swimmer/(\d+)/', href).group(1)
                   for href in hrefs]

    # Count the occurrences of each swimmer id
    for swimmer_id in swimmer_ids:
        if swimmer_id in swim_counts:
            swim_counts[swimmer_id] += 1

    return swim_counts


def populate_relay_swims(swim_obj):
    for url in relay_urls:
        swim_obj = count_swimmer_ids(url=url_prefix+url)


populate_relay_swims(swim_obj=swim_counts)
print(swim_counts)
