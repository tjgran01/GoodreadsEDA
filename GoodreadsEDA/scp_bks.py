import csv
import os
import re
import sqlite3
import time
import traceback
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


def get_book_urls():
    """Loads the export file from 'mk_bklst.py', and gets the urls of all
    of the books to pull reviews for. Returns the non-header rows

    Args:
        None

    Returns:
        book_urls[:1]
    """

    with open(f"{os.getcwd()}/csv_files/booksnlinks.csv", "r") as in_file:
        book_urls = list(csv.reader(in_file, delimiter=","))

    return book_urls[1:]


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


def click_next_review_page(driver):
    """Finds a link on the page that loads the next set of thirty reviews. If
    it is unable to find the link it tells the user no link was found and allows
    the program to move on to the next book in the list."""

    # print("clicking link!")
    try:
        next_link = driver.find_element_by_class_name("next_page")
        driver.execute_script("arguments[0].click()", next_link)
        # print("Waiting to load page.. ..")
        time.sleep(3.5)
        return True
    except:
        # print("Could Not Find a link!")
        return False


def print_bk_info(author, title, url):
    """Prints the information to the console about the book the scrapper is
    currently gathering data for."""

    print(author, title)
    print("-" * 50)
    print(url)
    print("-" * 50)


def print_pg_number(page_count):
    """Prints information to the console about how many pages into the scraping
    the scraper currently is."""

    print("-" * 50)
    print(f"Page: {page_count}")
    print("-" * 50)


def get_individual_review(review):
    """Grabs the user, date, and score information from an individual review"""

    user = review.find_element_by_class_name("user").text
    date = review.find_element_by_class_name("reviewDate").text
    try:
        score = review.find_element_by_class_name(" staticStars").text
        score = scores_to_numbers_dict[score]
    except NoSuchElementException:
        # print("No Score Given")
        score = None
    # Convert Score to Number Value
    # print(f"| {user} | {date} | {score}")
    return user, date, score


def insert_into_review_table(c, author, title, url, score, user, date):
    """Inserts all of the available data pulled from the review in to the "Reviews"
    table in the database."""

    # escapes all non-alphanumeric characters for consistent insertion
    user = re.escape(user)
    try:
        c.execute("""INSERT INTO Reviews (book_auth, book_title, book_url, review_score, user_name, review_date)
                     VALUES (?, ?, ?, ?, ?, ?)""", (author, title, url, score, user, date))
    except sqlite3.OperationalError:
        # this should actually never happen now, but I'm leaving it here for good measure
        traceback.print_exc()
        c.execute("""INSERT INTO Reviews (book_auth, book_title, book_url, review_score, user_name, review_date)
                     VALUES (?, ?, ?, ?, 'invalid username', ?)""", (author, title, url, score, date))


def print_scraping_status(current_book, total_books, start_timer):
    """Prints the status of the scraping if the process has progressed an arbitrary amount of books (currently 5)"""

    if current_book % 5 == 0 or current_book == 1:
        percent_completed = round(current_book / len(total_books) * 100, 2)
        minutes_elapsed = round((time.perf_counter() - start_timer) / 60, 2)
        print("-" * 75)
        print("{}% Complete".format(percent_completed))
        print("{} minutes elapsed, {} minutes of scraping remaining".format(
            minutes_elapsed, round(minutes_elapsed * (100.0 - percent_completed), 2)
        ))
        print("-" * 75)


def scrape_book_info(book_urls, driver, cursor):
    """Navigates the webdriver to the urls provided and scrapes up to 300 rating results from 10 pages of rating results

    Args:
        book_urls ([[str, str, str]]): A list of list of strings consisting of book author, book title, and book url
          to visit to serve as the base scraping url.
        driver (webdriver): The selenium chromedriver object to visit the urls with.
        cursor (sqlite3.cursor): A sqlite cursor to pass to methods writing to the DB.
    """

    scraping_start_timer = time.perf_counter()

    for book_number, entry in enumerate(book_urls):
        author = entry[0]
        title = entry[1]
        url = entry[2]
        print(author, title, url)
        time.sleep(5)
        driver.get(url)

        # Goodreads keeps a collection of 10 pages of 30 reviews available on the
        # book's page at a time.
        print("Scraping 10 pages of reviews for \"{}\". Scraping page ".format(title), end="", flush=True)
        for page_count in range(1, 11):
            # print_pg_number(page_count)
            # each set of 10 pages is printed on the same line to save space & cut down on noise
            if page_count != 10:
                print(f"{page_count}..", end="", flush=True)
            else:
                print(f"{page_count}")
            # grab every review on the current page and put it into "Reviews"
            reviews = driver.find_elements_by_class_name("reviewHeader")
            for review in reviews:
                user, date, score = get_individual_review(review)
                insert_into_review_table(cursor, author, title, url, score, user, date)

            link_found = click_next_review_page(driver)

            if not link_found or len(reviews) < 30:
                break

        print_scraping_status(book_number, book_urls, scraping_start_timer)


def main():
    # Get a list of all the urls for the books by the authors supplied from
    # mk_bklst.py, and remove the header row.
    book_urls = get_book_urls()

    # Options for the Chrome driver, so Chrome operates without calling a window.
    options = webdriver.ChromeOptions()
    options.add_argument('headless')

    # Connect to db, and create new table "Reviews"
    with sqlite3.connect(f"{os.getcwd()}/review_dbs/reviews.db") as conn:
        c = conn.cursor()
        create_review_table(c)
        driver = webdriver.Chrome(chrome_options=options)

        # Making sure the DB and driver connections are closed if there are any errors
        try:
            scrape_book_info(book_urls, driver, c)
        finally:
            driver.close()
            conn.commit()


scores_to_numbers_dict = {
    "it was amazing" : 5,
    "really liked it": 4,
    "liked it"       : 3,
    "it was ok"      : 2,
    "did not like it": 1
}

if __name__ == "__main__":
    main()
