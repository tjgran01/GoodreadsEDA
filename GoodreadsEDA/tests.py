import csv
import os
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup

url = "https://www.goodreads.com/book/show/19486412-big-little-lies"

# Options for the Chrome driver. Chome operates without calling a window.
options = webdriver.ChromeOptions()
options.add_argument("headless")

driver = webdriver.Chrome(chrome_options=options)
driver.get(url)

html = urlopen(url)
bsObj = BeautifulSoup(html, "html.parser")

for x in range(0, 10):

    reviews = driver.find_elements_by_class_name("reviewHeader")

    for i, review in enumerate(reviews):
        user = review.find_element_by_class_name("user").text
        date = review.find_element_by_class_name("reviewDate").text
        try:
            score = review.find_element_by_class_name(" staticStars").text
        except NoSuchElementException as e:
            print("No Score Given")
            score = "No Score Given"
        print(f"{i + 1} | {user} | {date} | {score}")



    print("clicking link!")
    try:
        next_link = driver.find_element_by_class_name("next_page")
        driver.execute_script("arguments[0].click()", next_link)
        print(driver.find_element_by_class_name("next_page").text)
        print("sleeping... ...")
        # after experimenting with a few different sleep times, this
        # time (3.5) seems to have allowed the page the proper amount of
        # time to load.
        time.sleep(3.5)
    except:
        print("Could Not Find a link")
        print("reloading page...")
        # keep an eye on this. might just need to adjust sleep time.

    driver.close
