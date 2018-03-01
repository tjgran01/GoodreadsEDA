import time
import csv
import os
import sqlite3
import sys

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


def get_book_urls():
    """Loads the export file from 'mk_bklst.py', and gets the urls of all
    of the books to pull reviews for."""

    with open(f"{os.getcwd()}/csv_files/booksnlinks.csv", "r") as in_file:
        books = csv.reader(in_file, delimiter=",")

        book_urls = [b for b in books]
        return book_urls


def scores_to_numbers(review_text):
    """Goodreads ratings are stored as text, this function converts them to
    their numerical values. If there is no score given, this function returns
    None"""

    if review_text == "it was amazing":
        review_score = 5
    elif review_text == "really liked it":
        review_score = 4
    elif review_text == "liked it":
        review_score = 3
    elif review_text == "it was ok":
        review_score = 2
    elif review_text == "did not like it":
        review_score = 1
    else:
        return None

    return review_score


def replace_double_quotes(string):
    """When entering information into the SQL db, there is a chance to get
    double quote characters within the text. This turns them into single
    quotes, so they do not escape the insert statement."""

    string = string.replace('"', "'")
    return(string)


def create_review_table(c):
    """Creates a table called "Reviews" in the reviews.db databse if it doesn't
    already exist. If "Reviews" does exists, it informs the user that it will
    append the current database."""

    try:
        c.execute(f"""CREATE TABLE Reviews (
                      book_auth TEXT(100) NOT NULL,
                      book_title TEXT(100) NOT NULL,
                      book_url TEXT(9999) NOT NULL,
                      review_score INT(100),
                      user_name TEXT(100) NOT NULL,
                      review_date TEXT(100) NOT NULL
                      );""")
    except sqlite3.OperationalError as e:
        print("Table already exists. The program will append the current table.")


def click_next_review_page(driver):
    """Finds a link on the page that loads the next set of thirty reviews. If
    it is unable to find the link it tells the user no link was found and allows
    the program to move on to the next book in the list."""

    print("clicking link!")
    try:
        next_link = driver.find_element_by_class_name("next_page")
        driver.execute_script("arguments[0].click()", next_link)
        print("Waiting to load page.. ..")
        time.sleep(3.5)
        return True
    except:
        print("Could Not Find a link!")
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
    """Grabs the user, date, and score information from an indivdual review"""

    user = review.find_element_by_class_name("user").text
    date = review.find_element_by_class_name("reviewDate").text
    try:
        score = review.find_element_by_class_name(" staticStars").text
    except NoSuchElementException as e:
        print("No Score Given")
        score = "None"
    # Convert Score to Number Value
    score = scores_to_numbers(score)
    print(f"| {user} | {date} | {score}")
    return (user, date, score)

def insert_into_review_table(c, author, title, url,
                             score, user, date):
    """Inserts all of the avilable data pulled from the review in to the "Review"
    table in the databse."""

    try:
        c.execute(f"""INSERT INTO Reviews (
                     book_auth, book_title,
                     book_url, review_score,
                     user_name, review_date)
                     VALUES ("{author}", "{title}",
                     "{url}", "{score}",
                     "{user}", "{date}"
                     )""")
    except sqlite3.OperationalError as e:
        print(e)
        c.execute(f"""INSERT INTO Reviews (
                 book_auth, book_title,
                 book_url, review_score,
                 user_name, review_date)
                 VALUES ("{author}", "{title}",
                 "{url}", "{score}",
                 "invalid_username", "{date}"
                 )""")


def main():
    # Get a list of all the urls for the books by the authors supplied from
    # mk_bklst.py, and remove the header row.
    book_urls = get_book_urls()
    book_urls.pop(0)

    # Options for the Chrome driver, so Chrome operates without calling a window.
    options = webdriver.ChromeOptions()
    options.add_argument('headless')

    # Connect to db, and create new table "Reviews"
    conn = sqlite3.connect(f"{os.getcwd()}/review_dbs/reviews.db")
    c = conn.cursor()
    create_review_table(c)

    for entry in book_urls:
        author = entry[0]
        title = entry[1]
        if '"' in title:
            title = replace_double_quotes(title)
        url = entry[2]

        print_bk_info(author, title, url)

        driver = webdriver.Chrome(chrome_options=options)
        driver.get(url)

        page_count = 1
        # Goodreads keeps a collection of 10 pages of 30 reviews available on the
        # book's page at a time.
        for x in range(0, 10):
            print_pg_number(page_count)
            # grab every review on the current page and put it into "Reviews"
            reviews = driver.find_elements_by_class_name("reviewHeader")
            for i, review in enumerate(reviews):
                user, date, score = get_individual_review(review)
                insert_into_review_table(c, author, title, url,
                                         score, user, date)
                conn.commit()

            link_found = click_next_review_page(driver)

            if not link_found or len(reviews) < 30:
                break
            else:
                page_count += 1
                continue

        driver.close()
    conn.close()


if __name__ == "__main__":
    main()
