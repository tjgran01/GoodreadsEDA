import pandas as pd
import os
import re
import sqlite3

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from imdb import IMDb
ia = IMDb()


def replace_double_quotes(string):
    """When entering information into the SQL db, there is a chance to get
    double quote characters within the text. This turns them into single
    quotes, so they do not escape the insert statement."""

    string = string.replace('"', "'")
    return(string)


conn = sqlite3.connect(f"{os.getcwd()}/review_dbs/reviews.db")
c = conn.cursor()

try:
    c.execute(f"""CREATE TABLE Release_Dates (
                  book_title TEXT(100) NOT NULL,
                  movie_title TEXT(100) NOT NULL,
                  release_date TEXT(100) NOT NULL
                  );""")
except sqlite3.OperationalError as e:
    c.execute(f"""DROP TABLE Release_Dates;""")
    print("table being overwritten")
    c.execute(f"""CREATE TABLE Release_Dates (
                  book_title TEXT(100) NOT NULL,
                  movie_title TEXT(100) NOT NULL,
                  release_date TEXT(100) NOT NULL
                  );""")

# Options for the Chrome driver, so Chrome operates without calling a window.
options = webdriver.ChromeOptions()
options.add_argument('headless')

movie_titl = ["Big Little Lies", "Me Before You", "The Circle",
              "Call Me By Your Name", "Everything, Everything",
              "Brooklyn", "A Man Called Ove",
              "Miss Peregrine’s Home for Peculiar Children",
              "The Girl on the Train", "The Light Between Oceans",
              "The 5th Wave", "Still Alice", "The DUFF",
              "Beasts of No Nation", "The Family Fang",
              "This Is Where I Leave You", "Me and Earl and the Dying Girl",
              "The Handmaid's Tale", "The Dinner",
              "Billy Lynn’s Long Halftime Walk", "Ender’s Game", "If I Stay"]

for title in movie_titl:
    print(title)
    s_result = ia.search_movie(title)
    print(s_result[0]['long imdb canonical title'], s_result[0].movieID)
    mov_title = s_result[0]['long imdb canonical title']
    mov_ID = s_result[0].movieID

    mov_url = f"http://www.imdb.com/title/tt{mov_ID}/"
    driver = webdriver.Chrome(chrome_options=options)
    driver.get(mov_url)
    mov_info = driver.find_element_by_id("titleDetails")
    r_date_elm = mov_info.find_element_by_xpath("//*[contains(text(), 'Release Date:')]/parent::*").text
    r_date = re.findall(r'\d\d\s(?:January|February|March|April|May|June|July|August|September|October|November|December)\s\d{4}', r_date_elm)
    if not r_date:
        r_date = re.findall(r'\d\s(?:January|February|March|April|May|June|July|August|September|October|November|December)\s\d{4}', r_date_elm)

    try:
        c.execute(f"""INSERT INTO Release_Dates (
                      book_title, movie_title,
                      release_date)
                      VALUES ("{title}", "{mov_title}",
                      "{r_date[0]}"
                      )""")
    except sqlite3.OperationalError as e:
        print(f"ERROR: {e}")
        mov_title = replace_double_quotes(mov_title)
        c.execute(f"""INSERT INTO Release_Dates (
                      book_title, movie_title,
                      release_date)
                      VALUES ("{title}", "{mov_title}",
                      "{r_date[0]}"
                      )""")
        print("ERROR resolved.")

    conn.commit()
    driver.close()

conn.close()
