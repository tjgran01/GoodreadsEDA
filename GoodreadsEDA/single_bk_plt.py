from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time

import scp_bks
import imdb_release
import bk_plt

def main():
    book = input("Please insert a book title you would like to graph: ")
    movie = input("Enter 'yes' if this book has a movie: ")

    options = webdriver.ChromeOptions()
    options.add_argument('headless')

    driver = webdriver.Chrome()
    driver.get("https://www.goodreads.com/")
    s_field = driver.find_element_by_css_selector("input[placeholder='Title / Author / ISBN']")
    s_field.send_keys(f"{book}")
    s_field.send_keys(Keys.RETURN)
    first_book = driver.find_element_by_class_name("bookTitle")
    driver.execute_script("arguments[0].click()", first_book)
    scp_bks.main(book_urls=driver.current_url(scp_bks))




if __name__ == "__main__":
    main()
