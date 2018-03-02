import pandas as pd
import os
import re
import sqlite3

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from imdb import IMDb
# my imports
from lists import movie_titl


def create_release_table(c):
    """Creates a table called "Release_Dates" in the reviews.db databse if it doesn't
    already exist. If "Release_Dates" does exists, it informs the user that it will
    overwrite the current database."""

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


def insert_into_release(c, title, mov_title, r_date):
    """Inserts the release date information pulled from imdb to the
    "Release_Dates" table"""

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


def get_movie_id(title):
    """IMDb uses movie IDs in the urls. This function searched for the movie
    using the title of the movie as a string, and returns the first result's
    corresponding movie ID as well as the movie title as IMDb stores it."""

    ia = IMDb()
    s_result = ia.search_movie(title)
    mov_title = s_result[0]['long imdb canonical title']
    mov_ID = s_result[0].movieID
    return mov_title, mov_ID


def get_movie_release(mov_ID, options):
    """Scrapes the page of the movie ID given, finds the release date element
    and returns it."""

    mov_url = f"http://www.imdb.com/title/tt{mov_ID}/"
    driver = webdriver.Chrome(chrome_options=options)
    driver.get(mov_url)
    mov_info = driver.find_element_by_id("titleDetails")
    r_date_elm = mov_info.find_element_by_xpath("//*[contains(text(), 'Release Date:')]/parent::*").text
    r_date = re.findall(r'\d\d\s(?:January|February|March|April|May|June|July|August|September|October|November|December)\s\d{4}', r_date_elm)
    if not r_date:
        r_date = re.findall(r'\d\s(?:January|February|March|April|May|June|July|August|September|October|November|December)\s\d{4}', r_date_elm)
    driver.close()
    return r_date


def replace_double_quotes(string):
    """When entering information into the SQL db, there is a chance to get
    double quote characters within the text. This turns them into single
    quotes, so they do not escape the insert statement."""

    string = string.replace('"', "'")
    return(string)


def main():

    conn = sqlite3.connect(f"{os.getcwd()}/review_dbs/reviews.db")
    c = conn.cursor()
    create_release_table(c)

    # Options for the Chrome driver, so Chrome operates without calling a window.
    options = webdriver.ChromeOptions()
    options.add_argument('headless')

    for title in movie_titl:
        mov_title, mov_ID = get_movie_id(title)
        r_date = get_movie_release(mov_ID, options)
        insert_into_release(c, title, mov_title, r_date)
        conn.commit()
    conn.close()


if __name__ == "__main__":
    main()
