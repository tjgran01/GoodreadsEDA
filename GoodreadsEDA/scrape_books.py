import csv
import os
from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup

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
                print("COULD NOT FIND A REVIEW SCORE")
                review_scores.append("")
            print(f"Review Score: {review_score}")
            review_scores.append(review_score)
        except AttributeError as e:
            print(e)
            print("Something is wonky with this one here.")
    return review_scores


def get_review_date(reviews):
    review_dates = []
    for review in reviews:
        date_text = review.find("a", {"class": "reviewDate"}).getText()
        print(f"Date of review: {date_text}")
        review_dates.append(date_text)
    return review_dates


with open(f"{os.getcwd()}/csv_files/booksnlinks.csv", "r") as in_file:
    books = csv.reader(in_file, delimiter=",")

    book_urls = []
    for book in books:
        book_urls.append(book[2])

# Remove Header From .csv
book_urls.pop(0)

for url in book_urls:
    print(url)
    reviews = get_book_info(url)
    review_scores = get_review_score(reviews)
    review_dates = get_review_date(reviews)

    with open(f"{os.getcwd()}/csv_files/bookreviews.csv", "a") as out_file:
        writer = csv.writer(out_file, delimiter=",")

        for i, review_score in enumerate(review_scores):
            writer.writerow([url, review_scores[i], review_dates[i]])
