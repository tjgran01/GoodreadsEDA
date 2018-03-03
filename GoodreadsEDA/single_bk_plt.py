import sqlite3
import os
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException


import scp_bks
import imdb_release
import bk_plt


def get_yes_or_no(prompt):
    while True:
        print(prompt)
        ans = input(">")
        if ans[0].upper() == "Y":
            return True
        elif ans[0].upper() == "N":
            return False
        else:
            print("Sorry, that is not a valid answer.")


def check_if_valid_string(prompt):
    while True:
        print(prompt)
        ans = input(">")
        if not re.match("^[A-Za-z ]*$", ans):
            print("Sorry, response can only contain letters and spaces.")
        else:
            return ans


def input_book_information():
    """


    """
    title = check_if_valid_string("Please provide a book title you would like to graph: ")
    author = check_if_valid_string("Please provide the author's name: ")
    is_movie = get_yes_or_no("Is there a movie adaptation of this book?: ")

    return (title, author, is_movie)

def navigate_to_book_page(book, driver):
    """


    """

    driver.get("https://www.goodreads.com/")
    s_field = driver.find_element_by_css_selector("input[placeholder='Title / Author / ISBN']")
    s_field.send_keys(f"{book}")
    s_field.send_keys(Keys.RETURN)
    first_book = driver.find_element_by_class_name("bookTitle")
    driver.execute_script("arguments[0].click()", first_book)
    return driver.current_url

def drop_old_table(c):
    c.execute("""DROP TABLE IF EXISTS Reviews""")

def create_review_table(c):
    """Creates a table called "Reviews" in the reviews.db database if it doesn't
    already exist. If "Reviews" does exists, it informs the user that it will
    append the current database."""

    c.execute("""CREATE TABLE IF NOT EXISTS Reviews (
                 book_auth TEXT(100) NOT NULL,
                 book_title TEXT(100) NOT NULL,
                 book_url TEXT(9999) NOT NULL,
                 review_score INT(100),
                 user_name TEXT(100) NOT NULL,
                 review_date TEXT(100) NOT NULL
                 );""")

def main():
    title, author, is_movie = input_book_information()
    # driver options
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(chrome_options=options)
    # scape_book_info requires that the url be in a list.
    book_url = navigate_to_book_page(title, driver)[:-17]
    book_info = [[author, title, book_url]]

    with sqlite3.connect(f"{os.getcwd()}/review_dbs/single_review.db") as conn:
        c = conn.cursor()
        drop_old_table(c)
        create_review_table(c)
        scp_bks.scrape_book_info(book_info, driver, c)
        bk_plt.main([title], 20, conn=conn)

if __name__ == "__main__":
    main()
