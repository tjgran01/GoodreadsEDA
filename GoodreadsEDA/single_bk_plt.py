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
    """Sanitizes user input to ensure they answer a yes or no question properly.

    Args:
        prompt(str): Prompt displayed to the user.

    Returns:
        Bool: True if user responds yes, False if user responds no."""
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
    """Sanitizes user input to make sure that book titles are only letters and
    spaces.

    Args:
        prompt(str): Prompt displayed to the user.

    Returns:
        ans(str): Valid answer provided by the user."""

    while True:
        print(prompt)
        ans = input(">")
        if not re.match("^[A-Za-z ]*$", ans):
            print("Sorry, response can only contain letters and spaces.")
        else:
            return ans


def input_book_information():
    """Takes user input to determine information about the book to be plotted.

    Args:
        None

    Returns:
        title(str): The title of the book.
        author(str): The author of the book.
        is_movie(Bool): True if there is a movie, False if there is not.
    """
    title = check_if_valid_string("Please provide a book title you would like to graph: ")
    author = check_if_valid_string("Please provide the author's name: ")
    is_movie = get_yes_or_no("Is there a movie adaptation of this book?: ")

    return (title, author, is_movie)


def navigate_to_book_page(book_title, driver):
    """Navigates to the goodreads.com page for the book the user inputted.

    Args:
        book_title(str): The title of the book.
        driver: Selenium WebDriver object.

    Returns:
        driver.current_utl(str): The url address of the book page.
    """

    driver.get("https://www.goodreads.com/")
    s_field = driver.find_element_by_css_selector("input[placeholder='Title / Author / ISBN']")
    s_field.send_keys(f"{book_title}")
    s_field.send_keys(Keys.RETURN)
    first_book = driver.find_element_by_class_name("bookTitle")
    driver.execute_script("arguments[0].click()", first_book)
    return driver.current_url


def drop_old_table(c):
    """Drops the last review database to aviod clutter.

    Args:
        c: Cursor object for SQLite3 database.

    Returns:
        None"""
    c.execute("""DROP TABLE IF EXISTS Reviews""")


def create_review_table(c):
    """Creates a table called "Reviews" in the reviews.db database if it doesn't
    already exist. If "Reviews" does exists, it informs the user that it will
    append the current database.

    Args:
        c: Cursor object for SGLite3 database

    Returns:
        None"""

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
    # [:-17] removes search from url.
    book_url = navigate_to_book_page(title, driver)[:-17]
    book_info = [[author, title, book_url]]

    with sqlite3.connect(f"{os.getcwd()}/review_dbs/single_review.db") as conn:
        c = conn.cursor()
        drop_old_table(c)
        create_review_table(c)
        scp_bks.scrape_book_info(book_info, driver, c)
        if is_movie:
            create_release_table(c)
            imdb_release.main(c=c, driver=driver, single_title=title)
        bk_plt.main([title], 20, conn=conn)

if __name__ == "__main__":
    main()
