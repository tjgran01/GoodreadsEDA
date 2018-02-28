import pandas as pd
import numpy as np
import sqlite3
import os
from datetime import datetime
from scipy.stats import ttest_ind
import sys
from dateutil.relativedelta import relativedelta

from lists import movie_titl

def get_mv_release(bk_m):
    """Gathers the movie release data for a corresponding book title.

    IN: bk_m (book title)
    OUT: df_rel["release_date"][0] (Release Date of Movie)"""
    try:
        df_rel = pd.read_sql_query(f"""SELECT * FROM Release_Dates
                                       WHERE book_title="{bk_m}"
                                       ;""", conn)
        return df_rel["release_date"][0]
    except IndexError as e:
        print(f"{e} \n")
        print("""Hmm... it looks as though the program cannot find the
Release_Date table... ... did you run imdb_release.py yet?""")

# Create empty df to append each book to after preprocessing.
df_all = pd.DataFrame()

# Go through every title in the list above.
for i, titl in enumerate(movie_titl):
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
    mv_release_datetime = datetime.strptime(mv_release, "%d %B %Y")
    df_all["movie_release"] = mv_release_datetime

    # turn string dates into datetime objects, and sort the dataframe by date.
    df["review_date"] = pd.to_datetime(df["review_date"])
    df.set_index("review_date", inplace=True)
    df.sort_index(inplace=True)

    # change review scores to ints, if it cannot be converted to int, NaN.
    df["review_score"] = df["review_score"].apply(pd.to_numeric, errors='coerce')

    # drop rows with NaN values in them.
    df.dropna(inplace=True)

    # take rolling average of review scores.
    df["review_score_rolling"] = df["review_score"].rolling(window=n_reviews,
                                                            center=False).mean()

    df_all = df_all.append(df)

# Print out of info about all data
print(f"Mean review score: {df_all['review_score'].mean()}")
print(f"Std review score: {df_all['review_score'].std()}")
print(df_all["review_score"].value_counts())

# Create a Column to split DataFrame for each of the different time intervals.
df_all["year_before_release"] = df_all["movie_release"].apply(lambda x: x - pd.DateOffset(years=1))
df_all["year_after_release"] = df_all["movie_release"].apply(lambda x: x + pd.DateOffset(years=1))
df_all["6mo_before_release"] = df_all["movie_release"].apply(lambda x: x - pd.DateOffset(months=6))
df_all["6mo_after_release"] = df_all["movie_release"].apply(lambda x: x + pd.DateOffset(months=6))
df_all["3mo_before_release"] = df_all["movie_release"].apply(lambda x: x - pd.DateOffset(months=3))
df_all["3mo_after_release"] = df_all["movie_release"].apply(lambda x: x + pd.DateOffset(months=3))

# Split the large DataFrame based on the values calulated before.
df_before = df_all[df_all.index <= df_all["movie_release"]]
df_after = df_all[df_all.index > df_all["movie_release"]]

df_before_1yr = df_before[df_before.index >= df_before["year_before_release"]]
df_after_1yr = df_after[df_after.index <= df_after["year_after_release"]]

df_before_6mo = df_before[df_before.index >= df_before["6mo_before_release"]]
df_after_6mo = df_after[df_after.index <= df_after["6mo_after_release"]]

df_before_3mo = df_before[df_before.index >= df_before["3mo_before_release"]]
df_after_3mo = df_after[df_after.index <= df_after["3mo_after_release"]]

# Report Stats.
print("-" * 90)
print("ALL REVIEWS")
print("-" * 90)
print(f"Mean review score before movie release: {df_before['review_score'].mean()}")
print(f"Mean review score after movie release: {df_after['review_score'].mean()}")
print(f"Difference in mean: {df_after['review_score'].mean() - df_before['review_score'].mean()}")
print(f"Std. review score before movie release: {df_before['review_score'].std()}")
print(f"Std. review score after movie release: {df_after['review_score'].std()}")
print(f"T-Test (t-statistic): {ttest_ind(df_after['review_score'], df_before['review_score'])}")
print(f"n Before: {df_before.shape[0]}")
print(f"n After: {df_after.shape[0]}")
print("-" * 90)
print("ALL REVIEWS WITHIN 1 YEAR OF MOVIE RELEASE")
print("-" * 90)
print(f"Mean review score before movie release: {df_before_1yr['review_score'].mean()}")
print(f"Mean review score after movie release: {df_after_1yr['review_score'].mean()}")
print(f"Difference in mean: {df_after_1yr['review_score'].mean() - df_before_1yr['review_score'].mean()}")
print(f"Std. review score before movie release: {df_before_1yr['review_score'].std()}")
print(f"Std. review score after movie release: {df_after_1yr['review_score'].std()}")
print(f"T-Test (t-statistic): {ttest_ind(df_after_1yr['review_score'], df_before_1yr['review_score'])}")
print(f"n Before: {df_before_1yr.shape[0]}")
print(f"n After: {df_after_1yr.shape[0]}")
print("-" * 90)
print("ALL REVIEWS WITHIN 6 MONTHS OF MOVIE RELEASE")
print("-" * 90)
print(f"Mean review score before movie release: {df_before_6mo['review_score'].mean()}")
print(f"Mean review score after movie release: {df_after_6mo['review_score'].mean()}")
print(f"Difference in mean: {df_after_6mo['review_score'].mean() - df_before_6mo['review_score'].mean()}")
print(f"Std. review score before movie release: {df_before_6mo['review_score'].std()}")
print(f"Std. review score after movie release: {df_after_6mo['review_score'].std()}")
print(f"T-Test (t-statistic): {ttest_ind(df_after_6mo['review_score'], df_before_6mo['review_score'])}")
print(f"n Before: {df_before_6mo.shape[0]}")
print(f"n After: {df_after_6mo.shape[0]}")
print("-" * 90)
print("ALL REVIEWS WITHIN 3 MONTHS OF MOVIE RELEASE")
print("-" * 90)
print(f"Mean review score before movie release: {df_before_3mo['review_score'].mean()}")
print(f"Mean review score after movie release: {df_after_3mo['review_score'].mean()}")
print(f"Difference in mean: {df_after_3mo['review_score'].mean() - df_before_3mo['review_score'].mean()}")
print(f"Std. review score before movie release: {df_before_3mo['review_score'].std()}")
print(f"Std. review score after movie release: {df_after_3mo['review_score'].std()}")
print(f"T-Test (t-statistic): {ttest_ind(df_after_3mo['review_score'], df_before_3mo['review_score'])}")
print(f"n Before: {df_before_3mo.shape[0]}")
print(f"n After: {df_after_3mo.shape[0]}")
