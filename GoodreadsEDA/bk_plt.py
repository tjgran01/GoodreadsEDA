import pandas as pd
import numpy as np
import sqlite3
import os
from datetime import datetime
from datetime import timedelta

import matplotlib.pyplot as plt
plt.style.use('seaborn-pastel')
import matplotlib.dates as mdates

n_reviews = 30

# Test Big Little Lies
bk = "Big Little Lies"
mv_release = "2017-02-19"

# Test Me Before You
# bk = "Me Before You (Me Before You, #1)"
# mv_release = "2016-05-23"

# Test Ender's Game
# bk = "Ender's Game (Ender's Saga, #1)"
# mv_release = '2013-11-01'

conn = sqlite3.connect(f"{os.getcwd()}/review_dbs/reviews.db")

df = pd.read_sql_query(f"""SELECT * FROM Reviews
                          WHERE book_title="{bk}"
                          """, conn)

# turn string dates into datetime objects, and sort the dataframe by date.
df["review_date"] = pd.to_datetime(df["review_date"])
df.set_index("review_date", inplace=True)
df.sort_index(inplace=True)

# change review scores to ints, if it cannot be converted to int, NaN.
df["review_score"] = df["review_score"].apply(pd.to_numeric, errors='coerce')

# drop rows with NaN values in them.
df.dropna(inplace=True)

# take rolling average of every fifteen review scores.
df["review_score_rolling"] = df["review_score"].rolling(window=n_reviews, center=False).mean()

# plotting parameters
x = df.index
y = df["review_score_rolling"]

print(df)

plt.plot(x, y)

plt.yticks(np.arange(3, 6, 1)) # books are seldom given a score < 3.
plt.ylabel(f"Average Rating Per {n_reviews} Reviews")

plt.xlabel("Year")

# plot release date of movie
plt.axvline(x=mv_release, color="#f99f75")
mv_release_datetime = datetime.strptime(mv_release, "%Y-%m-%d")
plt.text(mv_release_datetime + timedelta(days=10), 4,
                                         'Movie Release Date',
                                         rotation=90,
                                         color='#767a78')

plt.title(f"Review Scores of '{bk}' over time.")
plt.show()

# QUESTION: Should I close the connection after df is created or wait until
# the end of the script?
conn.close()
