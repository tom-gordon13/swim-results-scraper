from selenium_packages import *
import re
from time import sleep

# Set up the Selenium web driver
driver = webdriver.Chrome()

# Navigate to the webpage with the button
driver.get('https://www.swimcloud.com/results/187641/event/8/0/#round-FIN')

# Find results table
results_div = driver.find_element(By.CLASS_NAME, 'o-meet-layout')


# Find all swimmer rows
swimmer_rows = results_div.find_elements(By.TAG_NAME, 'tr')

best_split = {
    '1': None,
    '2': None,
    '3': None,
    '4': None
}

for row in swimmer_rows:
    try:
        # Find swimmer name
        swimmer_name = row.find_element(By.CLASS_NAME, 'bold').text

        # Wait for the button to be clickable
        wait = WebDriverWait(driver, 10)
        # button = wait.until(EC.element_to_be_clickable(
        #     (By.CLASS_NAME, 'js-time-popover')))

        button = row.find_element(
            By.CLASS_NAME, 'js-time-popover')

        # Click the button
        button.click()

        sleep(0.5)

        wait.until(EC.visibility_of_element_located(
            (By.CLASS_NAME, "popover")))

        # Extract the revealed information as a string
        # revealed_info = driver.find_element(By.ID, "input[class^='popover']").text
        splits = driver.find_element(By.CLASS_NAME, "popover")
        splits_text = splits.text

        # Print the revealed information
        print(swimmer_name)
        print(splits_text[0])

    except Exception as e:
        print('Error')
        # print(e)
        continue

# Close the web driver
driver.quit()
