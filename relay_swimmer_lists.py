import requests
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
params = {'param1': 'value1'}  # Replace with the parameters you found

# If the request requires headers like authentication tokens or cookies, add them here
headers = {
    'header1': 'value1',
    # ...
}

# response = requests.get(url, params=params, headers=headers)
response = requests.get(url)

# The response text will be a string, so if the API returns JSON, you can convert it to a Python dictionary
data = response.json()

# Now you can process the data however you need to
print(data)
