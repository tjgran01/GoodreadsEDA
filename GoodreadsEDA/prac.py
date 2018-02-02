import time
import csv
import os

from selenium import webdriver


def scores_to_numbers(review_text):

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
        review_score = None

    return review_score


# Make chrome run in the background
options = webdriver.ChromeOptions()
options.add_argument('headless')

# url = "https://www.goodreads.com/book/show/2784923-something-happened?from_search=true"

with open(f"{os.getcwd()}/csv_files/booksnlinks.csv", "r") as in_file:
    books = csv.reader(in_file, delimiter=",")

    book_urls = []
    for book in books:
        book_urls.append(book[2])

# Remove Header From .csv
book_urls.pop(0)

for url in book_urls:
    print(url)

    driver = webdriver.Chrome(chrome_options=options)
    driver.get(url)

    page_count = 1
    while True:
        no_next = False
        print("-" * 50)
        print(f"Page: {page_count}")
        print("-" * 50)

        dates = driver.find_elements_by_class_name("reviewDate")
        users = driver.find_elements_by_class_name("user")
        scores = driver.find_elements_by_class_name(" staticStars")

        for date in dates:
            print(date.text)
        for user in users:
            print(f"User Name: {user.text}")
        for score in scores:
            score = scores_to_numbers(score.text)
            print(f"Score: {score}")

        try:
            print("clicking link!")
            driver.find_element_by_class_name("next_page").click()
                print("sleeping... ...")
                time.sleep(2)
        except:
            no_next = True

        if no_next:
            print("Nothing to see here! Moving On.")
            break

        page_count += 1

    driver.close()
