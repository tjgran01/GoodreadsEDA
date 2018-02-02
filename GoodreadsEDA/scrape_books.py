import csv
import os
import time

from selenium import webdriver
from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
from selenium import webdriver

def get_book_info(url):

    try:
        html = urlopen(url)
        bsObj = BeautifulSoup(html, "html.parser")
    except HTTPError as e:
        print(e)
        return None
    try:
        auth_bks = bsObj.findAll("div", {"itemprop": "reviews"})
    except AttributeError as e:
        print(e)
        return None
    return auth_bks


def get_review_score(reviews):
    review_scores = []
    for review in reviews:
        try:
            review_text = review.find("span", {"class": " staticStars"}).getText()
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
                review_scores.append("")
            print(f"Review Score: {review_score}")
            review_scores.append(review_score)
        except AttributeError as e:
            print(e)
            print("No Stars Given")
            review_scores.append("")
    return review_scores


def get_review_date(reviews):
    review_dates = []
    for review in reviews:
        date_text = review.find("a", {"class": "reviewDate"}).getText()
        print(f"Date of review: {date_text}")
        review_dates.append(date_text)
    return review_dates


def get_review_users(reviews):
    review_users = []
    for review in reviews:
        user_name = review.find("a", {"class": "user"}).getText()
        print(f"Reviewer Username: {user_name}")
        review_users.append(user_name)
    return review_users


def click_through_reviews(url):

    # Make chrome run in the background
    options = webdriver.ChromeOptions()
    options.add_argument('headless')

    driver = webdriver.Chrome(chrome_options=options)
    driver.get(url)

    try:
        driver.find_element_by_class_name("next_page").click()
        print("sleeping... ...")
        time.sleep(2)
        print(driver.find_element_by_class_name("reviewDate").text)
        driver.close()
        return True
    except:
        return False


with open(f"{os.getcwd()}/csv_files/booksnlinks.csv", "r") as in_file:
    books = csv.reader(in_file, delimiter=",")

    book_urls = []
    for book in books:
        book_urls.append(book[2])


# Remove Header From .csv
book_urls.pop(0)

for url in book_urls:
    reviews = get_book_info(url)

    review_scores = []
    review_dates = []
    reviewers = []

    while True:
        print(url)

        review_scores_pg = get_review_score(reviews)
        review_dates_pg = get_review_date(reviews)
        reviewers_pg = get_review_users(reviews)

        review_scores.append(review_scores_pg)
        review_dates.append(review_dates_pg)
        reviewers.append(reviewers_pg)

        next_page = click_through_reviews(url)

        if not next_page:
            break

    with open(f"{os.getcwd()}/csv_files/bookreviews.csv", "a") as out_file:
        writer = csv.writer(out_file, delimiter=",")

        for i, review_score in enumerate(review_dates):
            # Think carefully about this if date isn't tracked then index is
            # messed up - make sure review_scores are printing None for reviews
            # that don't include a score
            writer.writerow([url, review_scores[i], review_dates[i],
                             reviewers[i]])
