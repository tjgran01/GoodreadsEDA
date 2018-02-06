import time
import csv
import os
import sqlite3

from selenium import webdriver


def get_book_urls():
    """Loads the export file from 'make_booklist.py', and gets the urls of All
    of the books to pull reviews for."""

    with open(f"{os.getcwd()}/csv_files/booksnlinks.csv", "r") as in_file:
        books = csv.reader(in_file, delimiter=",")

        book_urls = []
        for book in books:
            book_urls.append(book[2])

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
                  book_url TEXT(9999),
                  review_score INT(100),
                  user_name TEXT(100),
                  review_date TEXT(100)
                  );""")
except sqlite3.OperationalError as e:
    print("Table 'Reviews' already exists.")

# Remove Header row From booksnlinks.csv
book_urls.pop(0)

for url in book_urls:
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

        dates = driver.find_elements_by_class_name("reviewDate")
        users = driver.find_elements_by_class_name("user")
        scores = driver.find_elements_by_class_name(" staticStars")

        # First instances of scores is not tied to a user review. It is the avg
        # review listed at the top of the book page.
        scores.pop(0)

        # Turn scores from string value to interger
        int_scores = []
        for i, score in enumerate(scores):
            score = scores_to_numbers(score.text)
            print(f"Score: {score} {dates[i].text}")
            int_scores.append(score)

        # Sometimes people do not leave a star rating with their review.
        # This is an issue I will have to work out. Currently, it ignores the page.
        if len(int_scores) != len(dates):
            print("Inconsistent number of scores and entries on page.")
        else:
            # Need to find a way to discard dates and user_names when no score was given.
            for i, date in enumerate(dates):
                try:
                    c.execute(f"""INSERT INTO Reviews (
                                 book_url, review_score,
                                 user_name, review_date)
                                 VALUES ('{url}', '{int_scores[i]}',
                                 '{users[i].text}', '{date.text}'
                                 )""")
                # Some usernames have non ASCI text, this will throw an
                # OperationalError, to stop the program from halting just Mark
                # user_name as invalid, as it will not be used in analysis.
                except sqlite3.OperationalError as e:
                    print(e)
                    c.execute(f"""INSERT INTO Reviews (
                                 book_url, review_score,
                                 user_name, review_date)
                                 VALUES ('{url}', '{int_scores[i]}',
                                 'invalid_username', '{date.text}'
                                 )""")
                conn.commit()

        print("clicking link!")
        try:
            next_link = driver.find_element_by_class_name("next_page")
            driver.execute_script("arguments[0].click()", next_link)
            print(driver.find_element_by_class_name("next_page").text)
            print("sleeping... ...")
            # after experimenting with a few different sleep times, this
            # time (3.5) seems to have allowed the page the peroper amount of
            # time to load.
            time.sleep(3.5)
            page_count += 1
        except:
            print("Could Not Find a link")
            print("reloading page...")
            # keep an eye on this. might just need to adjust sleep time.

        if len(dates) < 30:
            break

    driver.close()
