import os
import sqlite3
import traceback
from datetime import datetime
import pandas as pd
from scipy.stats import ttest_ind
# my imports
from lists import movie_titles


n_reviews_rolling_avg = 20


def get_mv_release(bk_m, conn):
    """Gathers the movie release data for a corresponding book title.

    Args:
        bk_m(str): The title of the book.
        conn: Connection to SQLite3 database.
    Returns:
        df_rel["release_date"][0] (Release Date of Movie)
    Raises:
        IndexError if the program is unable to locate the proper table in the
        database."""
    try:
        df_rel = pd.read_sql_query(f"""SELECT * FROM Release_Dates
                                       WHERE book_title="{bk_m}"
                                       ;""", conn)
        return df_rel["release_date"][0]
    except IndexError:
        traceback.print_exc()
        print("""Hmm... it looks as though the program cannot find the
Release_Date table... ... did you run imdb_release.py yet?""")


def create_even_samples(df, df2):
    """Balances the data so that the before and after values have an equal #
    of sample sites.

    Args:
        df: The DataFrame of the review data prior to the release of the film.
        df2: The DataFrame of the review data after the release of the film.
    Returns:
        df: Above, but with the same amount of entries as df2.
        df2: Above, but with the same amount of entires as df."""

    sample_diff = df.shape[0] - df2.shape[0]
    if sample_diff > 0:
        return df.sample(df2.shape[0]), df2
    elif sample_diff < 0:
        return df, df2.sample(df.shape[0])
    return df, df2


def clean_review_data(movie_titles):
    """Iterates through all of the movie titles in 'movie_titles' and gets all
    the review data for the tiles, removes NaN values, and appends all of the
    the data into one DataFrame.

    Args:
        movie_title: A list of movie titles provided in 'lists.py'
    Returns:
        df_all: A pandas DataFrame with all of the review information for every
        book included in 'movie_titles'."""

    df_all = pd.DataFrame()

    for title in movie_titles:
        # Get movie release date for movie and df of reviews for the book.
        with sqlite3.connect(f"{os.getcwd()}/review_dbs/reviews.db") as conn:
            df = pd.read_sql_query("""SELECT * FROM Reviews
                                    WHERE book_title LIKE ?;""",
                                    conn, params=[title + '%'])

        df.drop(["matching_title", "book_url"], axis=1, inplace=True)
        mv_release = get_mv_release(title, conn)
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
        df["review_score_rolling"] = df["review_score"].rolling(window=n_reviews_rolling_avg,
                                                                center=False).mean()

        df_all = df_all.append(df)

    return df_all


def split_time_intervals(df_all, time_amt, how_many):
    """Creates new columns in the orginal DataFrame corresponding to various
    time differences before and after the release of a movie, then splits the
    DataFrame provided into DataFrames corresponding to the time before and
    after the release date.

    Args:
        df_all: a pandas DataFrame containing all of the book review data.
        time_amt(str): Time amount value, 'years' or 'months'.
        how_many(int): How many of the time amount to offset by.

    Returns:
        df_before: a pandas DataFrame with review data from before a movie's
        release, but after the specified time contraints begin.
        df_after: a pandas DataFrame with review data from after a movie's
        release, but before the specified time constraints end."""

    if time_amt == "years":
        df_all[f"{how_many}{time_amt}_before_release"] = df_all["movie_release"].apply(lambda x: x - pd.DateOffset(years=how_many))
        df_all[f"{how_many}{time_amt}_after_release"] = df_all["movie_release"].apply(lambda x: x + pd.DateOffset(years=how_many))
    elif time_amt == "months":
        df_all[f"{how_many}{time_amt}_before_release"] = df_all["movie_release"].apply(lambda x: x - pd.DateOffset(months=how_many))
        df_all[f"{how_many}{time_amt}_after_release"] = df_all["movie_release"].apply(lambda x: x + pd.DateOffset(months=how_many))

    df_before = df_all[df_all.index <= df_all["movie_release"]]
    df_after = df_all[df_all.index > df_all["movie_release"]]

    df_before_time = df_before[df_before.index >= df_before[f"{how_many}{time_amt}_before_release"]]
    df_after_time = df_after[df_after.index <= df_after[f"{how_many}{time_amt}_after_release"]]

    return (df_before_time, df_after_time)


def report_stats(df_before, df_after, time_period):
    """Prints various statistics about a given DataFrame.

    Args:
        df_before: a pandas DataFrame with review data from before a movie's
        release, but after the specified time contraints begin.
        df_after: a pandas DataFrame with review data from after a movie's
        release, but before the specified time constraints end.
        time_period(str): The amount of time from a release date the two
        DataFrames represent.

    Returns:
        None"""

    print("-" * 90)
    print(f"Time Period: {time_period}")
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


def main():
    
    df_all = clean_review_data(movie_titles)

    print(f"Mean review score: {df_all['review_score'].mean()}")
    print(f"Std review score: {df_all['review_score'].std()}")
    print(df_all["review_score"].value_counts())

    df_before_1yr, df_after_1yr = split_time_intervals(df_all, "years", 1)
    df_before_6mo, df_after_6mo = split_time_intervals(df_all, "months", 6)
    df_before_3mo, df_after_3mo = split_time_intervals(df_all, "months", 3)

    df_before = df_all[df_all.index <= df_all["movie_release"]]
    df_after = df_all[df_all.index > df_all["movie_release"]]

    df_after, df_before = create_even_samples(df_after, df_before)
    df_after_1yr, df_before_1yr = create_even_samples(df_after_1yr, df_before_1yr)
    df_after_6mo, df_before_6mo = create_even_samples(df_after_6mo, df_before_6mo)
    df_after_3mo, df_before_3mo = create_even_samples(df_after_3mo, df_before_3mo)

    report_stats(df_before, df_after, "All")
    report_stats(df_before_1yr, df_after_1yr, "1yr")
    report_stats(df_before_6mo, df_after_6mo, "6mo")
    report_stats(df_before_3mo, df_after_3mo, "3mo")


if __name__ == "__main__":
    main()
