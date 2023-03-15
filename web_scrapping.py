import os
import requests
from bs4 import BeautifulSoup
import time

def image_scrap(search_query, num_of_images):
    url = f"https://www.google.com/search?q={search_query}&tbm=isch&tbs=itp:face"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    image_tags = soup.find_all("img")
    if not os.path.exists(f"dataset/{search_query}"):
        os.mkdir(f"dataset/{search_query}")
    for i, image_tag in enumerate(image_tags[1:num_of_images+1]):
        image_url = image_tag.get("src")
        response = requests.get(image_url)
        with open(f"dataset/{search_query}/image_{i+1}.jpg", "wb") as f:
            f.write(response.content)


players_list = ["Sachin Tendulkar", "Virat Kohli", "Rohit Sharma", "Babar Azam", 
                "Kane Williamson", "Steve Smith", "Joe Root", "David Warner", 
                "Shakib Al Hasan", "Ross Taylor", "Jasprit Bumrah", "Jofra Archer", 
                "Mitchell Starc", "Trent Boult", "Pat Cummins", "Mohammad Amir", 
                "Bhuvneshwar Kumar", "Hardik Pandya", "Rashid Khan", "Imran Tahir", 
                "Chris Gayle", "AB de Villiers", "Quinton de Kock", "MS Dhoni", 
                "Rishabh Pant", "Kieron Pollard"]


for player in players_list:
    image_scrap(player, 100)
    time.sleep(10)
    
