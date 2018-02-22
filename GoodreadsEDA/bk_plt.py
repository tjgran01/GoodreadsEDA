import pandas as pd
import numpy as np
import sqlite3
import os
from datetime import datetime
from datetime import timedelta
import sys

import matplotlib.pyplot as plt
plt.style.use('seaborn-pastel')
import matplotlib.dates as mdates
from dateutil.relativedelta import relativedelta
import seaborn as sns
sns.set_style("white")

def get_mv_release(bk_m):
    try:
        df_rel = pd.read_sql_query(f"""SELECT * FROM Release_Dates
                                       WHERE book_title="{bk_m}"
                                       ;""", conn)
        return df_rel["release_date"][0]
    except IndexError as e:
        print(f"{e} \n")
        print("""Hmm... it looks as though the program cannot find the
Release_Date table... ... did you run imdb_release.py yet?""")


n_reviews = 20

movie_titl = ["Big Little Lies", "Me Before You", "The Circle",
              "Call Me By Your Name", "Everything, Everything",
              "Brooklyn", "A Man Called Ove",
              "Miss Peregrine’s Home for Peculiar Children",
              "The Girl on the Train", "The Light Between Oceans",
              "The 5th Wave", "Still Alice", "The DUFF",
              "Beasts of No Nation", "The Family Fang",
              "This Is Where I Leave You", "Me and Earl and the Dying Girl",
              "The Handmaid's Tale", "The Dinner",
              "Billy Lynn’s Long Halftime Walk", "Ender’s Game", "If I Stay"]

for i, titl in enumerate(movie_titl):
    try:
        bk = movie_titl[i]
        # Get movie release date for movie and df of reviews for the book.
        conn = sqlite3.connect(f"{os.getcwd()}/review_dbs/reviews.db")
        mv_release = get_mv_release(bk)
        # These two cases seemed to be giving me trouble, so I'm just hard coding them
        # For now.
        if titl == "Ender’s Game":
            df = pd.read_sql_query(f"""SELECT * FROM Reviews
                                       WHERE book_title = "Ender's Game (Ender's Saga, #1)"
                                       ;""", conn)
        elif titl == "Billy Lynn’s Long Halftime Walk":
            df = pd.read_sql_query(f"""SELECT * FROM Reviews
                                   WHERE book_title LIKE "Billy Lynn%"
                                   ;""", conn)
        else:
            df = pd.read_sql_query(f"""SELECT * FROM Reviews WHERE book_title LIKE "{bk}%";""", conn)

        conn.close()

        df.drop(["matching_title", "book_url"], axis=1, inplace=True)

        # turn string dates into datetime objects, and sort the dataframe by date.
        df["review_date"] = pd.to_datetime(df["review_date"])
        df.set_index("review_date", inplace=True)
        df.sort_index(inplace=True)

        # change review scores to ints, if it cannot be converted to int, NaN.
        df["review_score"] = df["review_score"].apply(pd.to_numeric, errors='coerce')

        # drop rows with NaN values in them.
        df.dropna(inplace=True)

        # take rolling average of every fifteen review scores.
        df["review_score_rolling"] = df["review_score"].rolling(window=n_reviews,
                                                                center=False).mean()

        # plotting parameters
        x = df.index
        y = df["review_score_rolling"]

        plt.plot(x, y)

        plt.yticks(np.arange(2.5, 5.5, .5)) # books are seldom given a score < 3.
        plt.ylabel(f"Average Rating Per {n_reviews} Reviews")

        # plot release date of movie as a line and label it.
        plt.axvline(x=mv_release, color="#f99f75")
        mv_release_datetime = datetime.strptime(mv_release, "%d %B %Y")
        plt.text(mv_release_datetime + timedelta(days=10), 4,
                                                 'Movie Release Date',
                                                 rotation=90,
                                                 color='#767a78')

        plt.xlabel("Year")
        plt.xlim(mv_release_datetime - relativedelta(years=1),
                 mv_release_datetime + relativedelta(years=1))
        plt.title(f"Review Scores of '{bk}' over time.")
        sns.despine()
        plt.show()
    except ValueError as e:
        print(e)
        print(df)
        continue
