import csv
import os
from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup

auth_urls = ["https://www.goodreads.com/author/list/322069.Liane_Moriarty",
             "https://www.goodreads.com/author/list/4178.Cormac_McCarthy",
             "https://www.goodreads.com/author/list/603698.Nic_Pizzolatto",
             "https://www.goodreads.com/author/list/23510.Upton_Sinclair",
             "https://www.goodreads.com/author/list/3472.Margaret_Atwood",
             "https://www.goodreads.com/author/list/170665.James_Bailey",
             "https://www.goodreads.com/author/list/344522.P_D_James",
             "https://www.goodreads.com/author/list/5735.Anthony_Burgess",
             ]

def get_auth_bks(url):
    try:
        html = urlopen(url)
        bsObj = BeautifulSoup(html, "html.parser")
    except HTTPError as e:
        print(e)
        return None
    try:
        auth_bks = bsObj.findAll("a", {"class": "bookTitle"})
    except AttributeError as e:
        print(e)
        return None
    return auth_bks

for auth_url in auth_urls:
    auth_name = auth_url[auth_url.rfind(".") + 1:]
    print(auth_name)
    auth_bks = get_auth_bks(auth_url)

    if not os.path.exists(f"{os.getcwd()}/csv_files/booksnlinks.csv"):
        with open(f"{os.getcwd()}/csv_files/booksnlinks.csv", "w") as out_file:
            writer = csv.writer(out_file, delimiter=",")

            writer.writerow(["Author_Name", "Book_Title", "Goodreads_Link"])

            for index, row in enumerate(auth_bks):
                info = [auth_name,
                        auth_bks[index].get_text()[1:-1],
                        f"https://www.goodreads.com{auth_bks[index].attrs['href']}",
                        ]
                print(info)
                writer.writerow(info)
    else:
        with open(f"{os.getcwd()}/csv_files/booksnlinks.csv", "a") as out_file:
            writer = csv.writer(out_file, delimiter=",")

            for index, row in enumerate(auth_bks):
                info = [auth_name,
                        auth_bks[index].get_text()[1:-1],
                        f"https://www.goodreads.com{auth_bks[index].attrs['href']}",
                        ]
                print(info)
                writer.writerow(info)
