import os
import sqlite3
import traceback
from datetime import datetime, timedelta
# plotting imports
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from dateutil.relativedelta import relativedelta
# my imports
from lists import movie_titles


def get_mv_release(book_title, conn):
    """Gets the release date movie that corresponds with the book title from the sqlite DB.

    Args:
        book_title (str): title of the book that the movie was based up for SQL lookup.
        conn (sqlite.connection): sqlite connection instance to use for DB queries.

    Returns:
        A string denoting the date that the movie in question was released on.

    Raises:
        IndexError: An error indicating that the book title was not in the DB.
    """
    try:
        df_rel = pd.read_sql_query("SELECT * FROM Release_Dates WHERE book_title = ?;", conn, params=[book_title])
        return df_rel["release_date"][0]
    except IndexError:
        traceback.print_exc()
        print("""Hmm... it looks as though the program cannot find the
        Release_Date table... ... did you run imdb_release.py yet?""")


def set_plotting_params():
    """Setting package-wide plotting parameters"""
    plt.style.use('seaborn-pastel')
    sns.set_style("ticks")


def plot_results(df, n_reviews, book_title, mv_release):
    """Plots the relationship between movie release and book ratings over time.

    Args:
        df (pandas.DataFrame): dataframe containing the values to plot.
        n_reviews (int): denominator to use for calculating rolling average.
        book_title (str): title of the book to plot.
        mv_release (str): the release date of the movie of the book.
    """

    # getting movie release date
    mv_release_datetime = datetime.strptime(mv_release, "%d %B %Y")
    # setting plotting parameters
    set_plotting_params()

    # plotting rolling average of book reviews over time and date of movie
    # release
    df.plot(x=df.index, y='review_score_rolling', color="#f99f75")
    plt.axvline(x=mv_release, color="#f99f75")

    # adjusting plot labels and orientation
    plt.title(f"Review Scores of '{book_title}' over time.")
    plt.yticks(np.arange(2.5, 5.5, .5))  # books are seldom given a score < 3.
    plt.ylabel(f"Average Rating Per {n_reviews} Reviews")
    plt.text(mv_release_datetime + timedelta(days=10),
             4,
             'Movie Release Date',
             rotation=90,
             color='#767a78')
    plt.xlabel("Time")
    plt.xticks(rotation=45)
    plt.xlim(mv_release_datetime - relativedelta(years=1),
             mv_release_datetime + relativedelta(years=1))
    plt.subplots_adjust(bottom=0.2)

    sns.despine()
    plt.show()


def main(movie_titles, n_reviews_rolling_avg):
    """Iterates through movies/book pairs, plotting each one's popularity as a
    book relative to its release date as a movie.

    Args:
        movie_titles ([str]): a sequence of strings of the titles of movies that
           were also books.
        n_reviews_rolling_avg (int): number of ratings to use when
          calculating the rolling average rating.

    Raises:
        ValueError: I suppose this would be to account for an error in reading the SQL query into a DataFrame, not
          entirely sure.
    """

    for title in movie_titles:
        try:
            # Get df of reviews for the book
            with sqlite3.connect(f"{os.getcwd()}/review_dbs/reviews.db") as conn:
                df = pd.read_sql_query("SELECT * FROM Reviews WHERE book_title LIKE ?;", conn, params=[title + '%'])
                mv_release = get_mv_release(title, conn)

            # formatting book reviews
            df.drop(["matching_title", "book_url"], axis=1, inplace=True)

            # turn string dates into datetime objects, and sort the dataframe by date.
            df["review_date"] = pd.to_datetime(df["review_date"])
            df.set_index("review_date", inplace=True)
            df.sort_index(inplace=True)

            # change review scores to ints, if it cannot be converted to int, NaN.
            df["review_score"] = df["review_score"].apply(pd.to_numeric, errors='coerce')

            # drop rows with NaN values in them.
            df.dropna(inplace=True)

            # take rolling average of every n_reviews_rolling_avg review scores.
            df["review_score_rolling"] = df["review_score"].rolling(window=n_reviews_rolling_avg, center=False).mean()

            # dropping the top n_reviews_rolling_avg values, as they have no rolling average value
            df = df.iloc[(n_reviews_rolling_avg - 1):]
            plot_results(df, n_reviews_rolling_avg, title, mv_release)

        except ValueError:
            traceback.print_exc()
            continue


if __name__ == '__main__':
    main(movie_titles, 20)