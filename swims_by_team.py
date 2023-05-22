import re
import json
import requests
from bs4 import BeautifulSoup

# Texas team page
page_url = 'https://www.swimcloud.com/results/194776/team/105/swims/'


def count_string_pattern(url):

    counts = {}

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
            if match in counts:
                counts[match] += 1
            else:
                counts[match] = 1

    # Return the counts as a JSON object
    return json.dumps(counts)


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


print(find_largest_pagination(url=page_url))
print(count_string_pattern(url=page_url))
