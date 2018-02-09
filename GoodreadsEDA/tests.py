import pandas as pd
import sqlite3
import os
import datetime

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

cwd = os.getcwd()

conn = sqlite3.connect(f"{cwd}/review_dbs/reviews.db")

df = pd.read_sql_query("""SELECT * FROM Reviews
                          WHERE book_title="Truly Madly Guilty"
                          """, conn)

df["review_date"] = pd.to_datetime(df["review_date"])
df.set_index("review_date", inplace=True)
df.sort_index(inplace=True)

df["review_score"] = df["review_score"].apply(pd.to_numeric, errors='coerce')


print(df.head())

# monthly_avg["review_score"] = df["review_score"].resample("M").mean()
x = df.index
y = df["review_score"]

plt.plot(x, y)
plt.title("Review Scores of 'Truly Madly Guilty' over time.")
plt.show()

conn.close()
