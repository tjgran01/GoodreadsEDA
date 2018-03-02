import os
import re
import sqlite3
import traceback
from imdb import IMDb
from selenium import webdriver
# my imports
from lists import movie_titles


def create_release_table(c):
    """Creates a table called "Release_Dates" in the reviews.db database if it doesn't
    already exist. If "Release_Dates" does exists, it informs the user that it will
    overwrite the current database."""

    try:
        c.execute("""CREATE TABLE Release_Dates (
                     book_title TEXT(100) NOT NULL,
                     movie_title TEXT(100) NOT NULL,
                     release_date TEXT(100) NOT NULL
                     );""")
    except sqlite3.OperationalError:
        traceback.print_exc()
        c.execute("""DROP TABLE Release_Dates;""")
        print("Table being overwritten")
        c.execute("""CREATE TABLE Release_Dates (
                     book_title TEXT(100) NOT NULL,
                     movie_title TEXT(100) NOT NULL,
                     release_date TEXT(100) NOT NULL
                     );""")


def insert_into_release(c, title, mov_title, r_date):
    """Inserts the release date information pulled from imdb to the
    "Release_Dates" table"""
    # title, mov_title, r_date = [remove_quotes(x) for x in [title, mov_title, r_date[0]]]
    # title, mov_title, r_date = [re.escape(x) for x in [title, mov_title, r_date[0]]]
    c.execute("INSERT INTO Release_Dates (book_title, movie_title, release_date) VALUES (?, ?, ?)",
              (title, mov_title, r_date[0]))


def get_movie_id(title):
    """IMDb uses movie IDs in the urls. This function searched for the movie
    using the title of the movie as a string, and returns the first result's
    corresponding movie ID as well as the movie title as IMDb stores it."""

    movie_db = IMDb()
    s_result = movie_db.search_movie(title)
    # print(s_result[0]['long imdb canonical title'], s_result[0].movieID)
    mov_title = s_result[0]['long imdb canonical title']
    mov_id = s_result[0].movieID
    return mov_title, mov_id


def get_movie_release(mov_id, driver):
    """Scrapes the page of the movie ID given, finds the release date element
    and returns it."""

    driver.get(f"http://www.imdb.com/title/tt{mov_id}/")
    mov_info = driver.find_element_by_id("titleDetails")
    r_date_elm = mov_info.find_element_by_xpath("//*[contains(text(), 'Release Date:')]/parent::*").text
    r_date = re.findall(r'\d\d\s(?:January|February|March|April|May|June|July|August|September|October|November|December)\s\d{4}', r_date_elm)
    if not r_date:
        r_date = re.findall(r'\d\s(?:January|February|March|April|May|June|July|August|September|October|November|December)\s\d{4}', r_date_elm)

    return r_date


def replace_double_quotes(string):
    """When entering information into the SQL db, there is a chance to get
    double quote characters within the text. This turns them into single
    quotes, so they do not escape the insert statement."""

    string = string.replace('"', "'")
    return string


def main():

    conn = sqlite3.connect(f"{os.getcwd()}/review_dbs/reviews.db")
    c = conn.cursor()
    create_release_table(c)

    # Options for the Chrome driver, so Chrome operates without calling a window.
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(chrome_options=options)

    for title in movie_titles:
        print(title)
        mov_title, mov_id = get_movie_id(title)
        r_date = get_movie_release(mov_id, driver)
        print(f"Released: {r_date[0]}\n")
        insert_into_release(c, title, mov_title, r_date)
    driver.close()
    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()
