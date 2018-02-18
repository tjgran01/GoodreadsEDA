import pandas as pd
import numpy as np
import sqlite3
import os
from datetime import datetime
from datetime import timedelta

import matplotlib.pyplot as plt
plt.style.use('seaborn-pastel')
import matplotlib.dates as mdates

def get_mv_release(bk_m):

    df_rel = pd.read_sql_query(f"""SELECT * FROM Release_Dates
                                   WHERE book_title="{bk_m}"
                                   ;""", conn)

    return df_rel["release_date"][0]


n_reviews = 30

movie_titl = ["Big Little Lies", "Me Before You", "The Circle",
              "Call Me By Your Name", "Everything Everything",
              "Room", "Brooklyn", "A Man Called Ove",
              "Miss Peregrine’s Home for Peculiar Children",
              "The Girl on the Train", "The Light Between Oceans",
              "The 5th Wave", "Still Alice", "The D.U.F.F.",
              "Beasts of No Nation", "The Family Fang",
              "This Is Where I Leave You", "Me and Earl and the Dying Girl",
              "The Handmaid’s Tale", "The Dinner",
              "Billy Lynn’s Long Halftime Walk", "Ender’s Game", "If I Stay"]

# Test Cases.

# Test Big Little Lies
# bk = "Big Little Lies"
# bk_m = movie_titl[0]

# Test Me Before You
# bk = "Me Before You (Me Before You, #1)"
# bk_m = movie_titl[1]

# Test Ender's Game
bk = "Ender's Game (Ender's Saga, #1)"
bk_m = movie_titl[-2]

# Get movie release date for movie and df of reviews for the book.
conn = sqlite3.connect(f"{os.getcwd()}/review_dbs/reviews.db")
mv_release = get_mv_release(bk_m)
df = pd.read_sql_query(f"""SELECT * FROM Reviews
                          WHERE book_title="{bk}"
                          ;""", conn)
conn.close() # db no longer needed.

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

plt.yticks(np.arange(3, 6, 1)) # books are seldom given a score < 3.
plt.ylabel(f"Average Rating Per {n_reviews} Reviews")

plt.xlabel("Year")

# plot release date of movie as a line and label it.
plt.axvline(x=mv_release, color="#f99f75")
mv_release_datetime = datetime.strptime(mv_release, "%d %B %Y")
plt.text(mv_release_datetime + timedelta(days=10), 4,
                                         'Movie Release Date',
                                         rotation=90,
                                         color='#767a78')

plt.title(f"Review Scores of '{bk}' over time.")
plt.show()
