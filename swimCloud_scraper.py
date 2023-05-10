import requests
from bs4 import BeautifulSoup

# The swimmer's URL on swimcloud.com
url = 'https://www.swimcloud.com/swimmer/670258/'

# Send a GET request to the URL
response = requests.get(url)

# Parse the HTML content of the response using Beautiful Soup
soup = BeautifulSoup(response.content, 'html.parser')

# Find the table containing the swimmer's fastest times
table = soup.find_all(
    'table', {'class': 'c-table-clean c-table-clean--middle table table-hover'})[1]


# Find the rows in the table
rows = table.find_all('tr')

# print(rows)

# # Loop through the rows and extract the swimmer's fastest times
fastest_times = []
for row in rows:
    cells = row.find_all('td')
    if len(cells) == 6:
        time = cells[1].text.strip()
        event = cells[0].text.strip()
        date = cells[4].text.strip()
        # location = cells[3].text.strip()
        meet = cells[3].text.strip()
        fastest_times.append(
            {'time': time, 'event': event, 'date': date, 'meet': meet})

# Print the swimmer's fastest times
print(fastest_times)
