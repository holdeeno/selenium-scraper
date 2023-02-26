import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from parsel import Selector

# https://www.google.com/maps/search/{keyword PLI}/@{LAT},{LONG},15z
GOOGLE_MAPS_URL = 'https://www.google.com/maps/search/gyms/@30.2357602,-97.8386944,15z'

# start a selenium web driver and specify browsing options
def get_driver():
  chrome_options = Options()
  chrome_options.add_argument('--no-sandbox')
  chrome_options.add_argument('--headless')
  chrome_options.add_argument('--disable-dev-shm-usage')
  driver = webdriver.Chrome(options=chrome_options)
  return driver

# download google maps page
def get_page_content(driver):
  driver.get(GOOGLE_MAPS_URL)

  # scroll down until all results are returned
  # locate the google maps feed using xpath 
  feed_element = driver.find_element(By.XPATH, '//div[contains(@aria-label, "Results for")]')

  # get the scroll height of the feed using javascript
  last_height = driver.execute_script("return arguments[0].scrollHeight;", feed_element)

  while True:
    # scroll to the bottom
    driver.execute_script("arguments[0].scrollTo(0, arguments[1]);", feed_element, last_height)

    # wait to load the page
    time.sleep(5)

    # calculate new scroll height and compare with the last scroll height
    new_height = driver.execute_script("return arguments[0].scrollHeight;", feed_element)

    # if the new scroll height is the same as the old, then no new elements were loaded
    if new_height == last_height:
      break
    last_height = new_height

  # download page content
  page_content = driver.page_source
  
  # return page_content
  return page_content

# parse maps search content
def parse_places(page_content):
  response = Selector(page_content)
  results = []

  for element in response.xpath('//div[contains(@aria-label, "Results for")]/div/div[./a]'):
    results.append({
        'title': element.xpath('./a/@aria-label').extract_first(''),
        'link': element.xpath('./a/@href').extract_first('')
    })

  return results

if __name__ == "__main__":
  print ('Creating driver')
  driver = get_driver()

  print('Fetching page content')
  page_content = get_page_content(driver)

  print('Parsing page results')
  places_data = parse_places(page_content)

  print('Saving the data to a CSV')
  places_df = pd.DataFrame(places_data)
  print(places_df)
  places_df.to_csv('places.csv', index=None)