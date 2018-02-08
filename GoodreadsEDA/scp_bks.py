import time
import csv
import os
import sqlite3
import sys

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


def get_book_urls():
    """Loads the export file from 'make_booklist.py', and gets the urls of All
    of the books to pull reviews for."""

    with open(f"{os.getcwd()}/csv_files/booksnlinks.csv", "r") as in_file:
        books = csv.reader(in_file, delimiter=",")

        book_urls = []
        for book in books:
            book_urls.append(book)

        return book_urls


def scores_to_numbers(review_text):
    """Goodreads ratings are stored as text, this function converts them to their
    numerical value. If there is no score given, this function returns None"""

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
    quotes, so they do not escape the insert command."""

    string = string.replace('"', "'")
    return(string)


# First, get a list of all the urls for the books by the authors.
book_urls = get_book_urls()

# Options for the Chrome driver. Chome operates without calling a window.
options = webdriver.ChromeOptions()
options.add_argument('headless')

# Create sqlite3 cursor
conn = sqlite3.connect(f"{os.getcwd()}/review_dbs/reviews.db")
c = conn.cursor()

# If no database exists, create one.
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
    print("Table already exists. The program will append the current table. \n")


# Remove Header row From booksnlinks.csv
book_urls.pop(0)

for entry in book_urls:
    author = entry[0]
    title = entry[1]
    url = entry[2]

    print(author, title)
    print("-" * 50)
    print(url)
    print("-" * 50)

    driver = webdriver.Chrome(chrome_options=options)
    driver.get(url)

    page_count = 1
    # Goodreads keeps a collection of 10 pages of 30 reviews available on the
    # books page at a time.
    for x in range(0, 10):
        print("-" * 50)
        print(f"Page: {page_count}")
        print("-" * 50)

        reviews = driver.find_elements_by_class_name("reviewHeader")

        for i, review in enumerate(reviews):
            user = review.find_element_by_class_name("user").text
            date = review.find_element_by_class_name("reviewDate").text
            try:
                score = review.find_element_by_class_name(" staticStars").text
            except NoSuchElementException as e:
                print("No Score Given")
                score = "No Score Given"
            # Convert Score to Number Value
            score = scores_to_numbers(score)
            print(f"{i + 1} | {user} | {date} | {score}")

            try:
                # Gets rid of escaping issues caused by title having "" chars in
                # it.
                if '"' in title:
                    title = replace_double_quotes(title)
                    print(title)
                c.execute(f"""INSERT INTO Reviews (
                             book_auth, book_title,
                             book_url, review_score,
                             user_name, review_date)
                             VALUES ("{author}", "{title}",
                             "{url}", "{score}",
                             "{user}", "{date}"
                             )""")
            # Some usernames have non ASCI text, this will throw an
            # OperationalError, to stop the program from halting just Mark
            # user_name as invalid, as it will not be used in analysis.
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
            conn.commit()

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
            page_count += 1
        except:
            print("Could Not Find a link!")
            break
            # keep an eye on this. might just need to adjust sleep time.

        # Pages have a len of 30 reviews. Though this won't catch all
        # cases, (if total reviews < 150 and % 30 == 0) this is a quick and
        # dirty way of avioding clicking on a link that leads nowhere
        if len(reviews) < 30:
            break

    driver.close()
