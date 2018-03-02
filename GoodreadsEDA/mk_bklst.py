import csv
import os
import traceback
from urllib.error import HTTPError
from urllib.request import urlopen
from bs4 import BeautifulSoup
# my imports
from lists import auth_urls


def get_auth_bks(url):
    """Opens a url for an author's booklist page on goodreads.com and returns
    a list of urls for each of the author's books.

    INPUT
     url (str): Author's URL
    OUTPUT
     [str]: List of links to author's books if the parsing is successful
     None: prints the encountered Exception and returns None if an exception is encountered in bs4 parsing.
     """

    try:
        html = urlopen(url)
        bs_obj = BeautifulSoup(html, "html.parser")
    except HTTPError:
        traceback.print_exc()
        return None
    try:
        auth_bks = bs_obj.findAll("a", {"class": "bookTitle"})
    except AttributeError:
        traceback.print_exc()
        return None
    return auth_bks


def write_to_csv(out_file, auth_bks, auth_name, append=True):
    writer = csv.writer(out_file, delimiter=",")
    # Write header to .csv file.
    if not append:
        writer.writerow(["Author_Name", "Book_Title", "Goodreads_Link"])
    # Write all of the boot data.
    for index in range(len(auth_bks)):
        info = [auth_name,
                auth_bks[index].get_text()[1:-1],
                f"https://www.goodreads.com{auth_bks[index].attrs['href']}",
               ]
        writer.writerow(info)


def main():
    for auth_url in auth_urls:
        # The author's name is listed at the end of each url, after the last '.'
        auth_name = auth_url[auth_url.rfind(".") + 1:]
        print(f"Scraping books by {auth_name}")
        auth_bks = get_auth_bks(auth_url)

        # Create booksnlinks.csv if it doesn't exist already.
        if os.path.exists(f"{os.getcwd()}/csv_files/booksnlinks.csv"):
            with open(f"{os.getcwd()}/csv_files/booksnlinks.csv", "a") as out_file:
                write_to_csv(out_file, auth_bks, auth_name)
        else:
            with open(f"{os.getcwd()}/csv_files/booksnlinks.csv", "w") as out_file:
                write_to_csv(out_file, auth_bks, auth_name, append=False)

    print("-" * 80)
    print("All done.")
    print(f"File exported to: {os.getcwd()}/csv_files/booksnlinks.csv")
    print("-" * 80)


if __name__ == "__main__":
    main()
