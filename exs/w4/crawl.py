import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
import json

# top 250 url
url = 'https://www.imdb.com/chart/top/?ref_=nv_mv_250'

# without this header you get 403 forbidden, and sometimes it sends german output
header = {'User-Agent': 'Mozilla/5.0', 'accept-language': 'en-US,en;q=0.9,en-GB;q=0.8'}
page = requests.get(url, headers=header)
soup = BeautifulSoup(page.content, 'html.parser')

# go through the page and get 250 links
links = []
list_items = soup.find_all('td', class_='titleColumn')

for item in list_items:
    # save the links in this format /title/tt19824/ for easier crawling
    link_parts = item.find('a')['href'].split('/')
    links.append('/'.join(link_parts[:3]))

# convert the time from the website to minutes
def convert_time(time):
    # 1h 11m format
    if len(time.split('h ')) == 2:
        hours, minutes = time.split("h ")
        minutes = int(minutes[:-1])
        return int(hours) * 60 + minutes
    # 1h format
    else:
        if time[-1] == 'h':
            hours = time.replace('h', '')
            return int(hours) * 60
        else:
            minutes = time.replace('m', '')
            return int(minutes)

# load selenium web driver to scrape story
options = Options()
options.add_argument("--headless=new")
driver = webdriver.Chrome(options=options)

# open the json  file
with open('data.json', "r") as file:
    json_data = json.load(file)

# go through each link and extract the data
for link in links:
    movie = {}
    link_url = 'https://www.imdb.com/'

    page = requests.get(link_url + link, headers=header)
    soup = BeautifulSoup(page.content, 'html.parser')

    # selenium
    try:
        driver.get(link_url + link)
    except TimeoutException:
        driver.get(link_url + link)

    movie['id'] = link.replace('/title/tt', '').replace('/', '')
    movie['title'] = soup.find('h1').text

    # the year ,PG ,time is in the same ul
    bar = driver.find_elements(By.XPATH, '//h1[@data-testid="hero__pageTitle"]/following-sibling::ul/li')
    parts = [item.text.strip() for item in bar]
    # might not get PG
    if len(parts) == 3:
        movie['year'], movie['parental_guide'], time = parts[0], parts[1], parts[2]
    else:
        movie['year'], time = parts[0], parts[1]

    movie['runtime'] = convert_time(time)

    # gener is a list
    genre_list = driver.find_elements(By.XPATH, '//div[@data-testid="genres"]/div/a')
    movie['genre'] = [g.text for g in genre_list]

    # find the div -> all elements could be lists
        # get rows one by one
        # i have three rows -> each row one ul -> each ul has name
    meta = soup.find('div', class_="jBXsRT")
    meta_list = meta.find_all('div', class_='ipc-metadata-list-item__content-container')
    lis = []
    for i in meta_list:
        ul = i.find('ul')
        li = ul.find_all('li')
        people = []
        for x in li:
            person_id = x.find('a')['href']
            person_id = person_id[8:15]
            people.append({str(x.text): person_id})
        lis.append(people)
    movie['director'], movie['writers'], movie['stars'] = lis[0], lis[1], lis[2]

    # get the story with selenium because it loads dynamically
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2 - 400);")
    wait = WebDriverWait(driver, 5)

    # inghad internet khoobe ha !!!
    try:
        story_section = wait.until(ec.visibility_of_element_located((By.XPATH, '//section[@data-testid="Storyline"]')))
    except TimeoutException:
        story_section = wait.until(ec.visibility_of_element_located((By.XPATH, '//section[@data-testid="Storyline"]')))

    movie['story'] = story_section.find_element(By.XPATH,
                                       '//section[@data-testid="Storyline"]//div[@class="ipc-html-content-inner-div"]').text

    # gross us canada
    try:
        gross = driver.find_element(By.XPATH,
                                    "//*[contains(text(), 'Gross US & Canada')]/following-sibling::div//ul//li//span").text
        gross = gross.replace('$', '').replace(',', '')
    except:
        gross = None
    movie['gross_us_canada'] = gross

    # add to json file
    json_data.append(movie)

    with open('data.json', 'w') as f:
        json.dump(json_data, f)


# quit the driver
driver.quit()

