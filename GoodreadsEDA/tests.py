import pandas as pd
import sqlite3
import os
import datetime

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

bk = "Ender's Game (Ender's Saga, #1)"

cwd = os.getcwd()

conn = sqlite3.connect(f"{cwd}/review_dbs/reviews.db")

df = pd.read_sql_query(f"""SELECT * FROM Reviews
                          WHERE book_title="{bk}"
                          """, conn)

df["review_date"] = pd.to_datetime(df["review_date"])
df.set_index("review_date", inplace=True)
df.sort_index(inplace=True)

df["review_score"] = df["review_score"].apply(pd.to_numeric, errors='coerce')

# monthly_avg["review_score"] = df["review_score"].resample("M").mean()
df.dropna(inplace=True)
df["review_score_rolling"] = df["review_score"].rolling(window=15, center=False).mean()
x = df.index
y = df["review_score_rolling"]

print(df)

plt.plot(x, y)
plt.title(f"Review Scores of '{bk}' over time.")
plt.show()

conn.close()
