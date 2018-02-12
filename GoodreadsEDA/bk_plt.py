import pandas as pd
import sqlite3
import os
import datetime

import matplotlib.pyplot as plt
plt.style.use('seaborn-pastel')
import matplotlib.dates as mdates

# Test Big Little Lies
# bk = "Big Little Lies"
# mv_release = "2017-02-19"

# Test Ender's Game
bk = "Ender's Game (Ender's Saga, #1)"
mv_release = '2013-11-01'

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
df["review_score_rolling"] = df["review_score"].rolling(window=15, center=False).mean()

# plotting parameters
x = df.index
y = df["review_score_rolling"]

print(df)

plt.plot(x, y)
plt.axvline(x=mv_release, color="r")
plt.title(f"Review Scores of '{bk}' over time.")
plt.show()

# QUESTION: Should I close the connection after df is created or wait until
# the end of the script?
conn.close()
