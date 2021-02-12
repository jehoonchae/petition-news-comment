from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from tqdm import tqdm
import time

import re
import os
import csv


from utils import cleaner

# Make folder to save data
current_path = os.getcwd()
petition_data_path = current_path + "/data/petition"
os.makedirs(petition_data_path, exist_ok=True)

# Generate the urls of blut-house petition web page
base_url = "https://www1.president.go.kr/petitions/?c=0&only=2&page={}&order=1"
page_list = [base_url.format(str(i + 1)) for i in range(64356)]

# My chrome driver path
chrome_path = current_path + "/chromedriver"

# Use headless mode
options = webdriver.ChromeOptions()
options.add_argument("headless")
options.add_argument("window-size=1920x1080")
options.add_argument("disable-gpu")
# options.add_argument("--disable-gpu")

# Install and open driver with proper version
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
# driver = webdriver.Chrome(executable_path=chrome_path, options=options)

with open("data/petition/petition_url_list.csv", "w", encoding="utf8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["url", "category", "title", "expired_date", "count"])

    for page in tqdm(page_list):
        driver.get(page)
        driver.implicitly_wait(3)
        time.sleep(1.5)
        html = driver.page_source
        soup = BeautifulSoup(html, "lxml")
        try:
            for i in range(
                len(
                    soup.find("ul", class_="petition_list").find_all(
                        "div", class_="bl_subject"
                    )
                )
            ):
                url = (
                    soup.find("ul", class_="petition_list")
                    .find_all("div", class_="bl_subject")[i]
                    .a.get("href")
                )
                url = cleaner(url, mode="url")
                category = (
                    soup.find("ul", class_="petition_list")
                    .find_all("div", class_="bl_category ccategory cs wv_category")[i]
                    .text
                )
                category = cleaner(category, mode="category")
                title = (
                    soup.find("ul", class_="petition_list")
                    .find_all("div", class_="bl_subject")[i]
                    .text
                )
                title = cleaner(title, mode="title")
                expired_date = (
                    soup.find("ul", class_="petition_list")
                    .find_all("div", class_="bl_date light")[i]
                    .text
                )
                expired_date = cleaner(expired_date, mode="expired_date")
                count = (
                    soup.find("ul", class_="petition_list")
                    .find_all("div", class_="bl_agree cs")[i]
                    .text
                )
                count = cleaner(count, mode="count")
                writer.writerow([url, category, title, expired_date, count])
        except AttributeError:
            print(page, i)

driver.close()
