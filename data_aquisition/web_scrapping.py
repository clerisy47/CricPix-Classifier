import os
import time
import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver

def image_scrap(search_query, num_of_images):
    driver = webdriver.Chrome()
    driver.get(f"https://www.google.com/search?q={search_query}&tbm=isch&tbs=itp:face")

    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    soup = BeautifulSoup(driver.page_source, "html.parser")
    image_tags = soup.find_all("img")
    image_urls = [tag.get("src") for tag in image_tags]
    if not os.path.exists(f"dataset/{search_query}"):
        os.mkdir(f"dataset/{search_query}")
    for i, url in enumerate(image_urls[:num_of_images]):
        filename = f"dataset/{search_query}/image_{i+1}.jpg"
        urllib.request.urlretrieve(url, filename)

    driver.quit()


players_list = ["rohit_sharma", "ricky_ponting", "kumar_sangakkara", "virat_kohli", "ms_dhoni", "sachin_tendulkar"]

for player in players_list:
    image_scrap(player, 100)
