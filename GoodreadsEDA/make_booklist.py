import csv
import os
from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup

auth_urls = ["https://www.goodreads.com/author/list/322069.Liane_Moriarty",
             "https://www.goodreads.com/author/list/281810.Jojo_Moyes",
             "https://www.goodreads.com/author/list/3371.Dave_Eggers",
             "https://www.goodreads.com/author/list/2922229.Andr_Aciman",
             "https://www.goodreads.com/author/list/7353006.Nicola_Yoon",
             "https://www.goodreads.com/author/23613.Emma_Donoghue/questions",
             "https://www.goodreads.com/author/list/1351903.Colm_T_ib_n",
             "https://www.goodreads.com/author/list/6485178.Fredrik_Backman",
             "https://www.goodreads.com/author/list/3046613.Ransom_Riggs",
             "https://www.goodreads.com/author/list/1063732.Paula_Hawkins",
             "https://www.goodreads.com/author/list/5755257.M_L_Stedman",
             "https://www.goodreads.com/author/list/3377941.Rick_Yancey",
             "https://www.goodreads.com/author/list/978484.Lisa_Genova",
             "https://www.goodreads.com/author/list/3095919.Kody_Keplinger",
             "https://www.goodreads.com/author/list/27161.Uzodinma_Iweala",
             "https://www.goodreads.com/author/list/73187.Kevin_Wilson",
             "https://www.goodreads.com/author/list/26163.Jonathan_Tropper",
             "https://www.goodreads.com/author/list/5227163.Jesse_Andrews",
             "https://www.goodreads.com/author/list/3472.Margaret_Atwood",
             "https://www.goodreads.com/author/list/1245772.Herman_Koch",
             "https://www.goodreads.com/author/list/7079.Ben_Fountain",
             "https://www.goodreads.com/author/list/589.Orson_Scott_Card",
             "https://www.goodreads.com/author/list/295178.Gayle_Forman",
             ]

def get_auth_bks(url):
    """Opens a url for an author's booklist page on goodreads.com and returns
    a list of urls for each of the author's books."""

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
