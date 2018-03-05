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


def get_yes_or_no(prompt):
    """Sanitizes user input to yes or no questions.

    Args:
        Prompt(str): The question to display to the user.

    Returns:
        Bool: True if user answeres yes, False if user answers no."""

    while True:
        print(prompt)
        ans = input(">")
        if ans[0].upper() == "Y":
            return True
        elif ans[0].upper() == "N":
            return False
        else:
            print("Sorry, that is not a valid answer.")


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


def plot_results(df, n_reviews, book_title, mv_release, save_fig):
    """Plots the relationship between movie release and book ratings over time.

    Args:
        df (pandas.DataFrame): dataframe containing the values to plot.
        n_reviews (int): denominator to use for calculating rolling average.
        book_title (str): title of the book to plot.
        mv_release (str): the release date of the movie of the book.
    """

    # setting plotting parameters
    set_plotting_params()

    # plotting rolling average of book reviews over time and date of movie
    # release
    df.plot(x=df.index, y='review_score_rolling', color="#92c6ff")

    # adjusting plot labels and orientation
    plt.title(f"Review Scores of '{book_title}' over time.")
    plt.yticks(np.arange(2.5, 5.5, .5))  # books are seldom given a score < 3.
    plt.ylabel(f"Average Rating Per {n_reviews} Reviews")
    plt.xlabel("Time")
    plt.xticks(rotation=45)
    if mv_release:
        plot_mv_release(mv_release=mv_release)
    plt.subplots_adjust(bottom=0.2)
    sns.despine()
    if save_fig:
        plt.savefig(f"{os.getcwd()}/../docs/img/{book_title}_fig.png",
                      dpi=600, bbox_inches='tight')
    plt.show()


def plot_mv_release(mv_release):
    """Plots a solid, vertical, line to represent the day a movie was released
    on the plot of review scores. Adjusts the x axis of the plot to be within
    a year of this date.

    Args:
        mv_release(str): The date that the movie was release."""

    mv_release_datetime = datetime.strptime(mv_release, "%d %B %Y")
    plt.axvline(x=mv_release_datetime, color='#f99f75')
    plt.text(mv_release_datetime + timedelta(days=10),
             4,
             'Movie Release Date',
             rotation=90,
             color='#767a78')
    plt.xlim(mv_release_datetime - relativedelta(years=1),
             mv_release_datetime + relativedelta(years=1))


def main(movie_titles, n_reviews_rolling_avg, conn=None, mv_release=None):
    """Iterates through movies/book pairs, plotting each one's popularity as a
    book relative to its release date as a movie.

    Args:
        movie_titles ([str]): a sequence of strings of the titles of movies that
           were also books.
        n_reviews_rolling_avg (int): number of ratings to use when
          calculating the rolling average rating.
        conn: Optional connection to database if this function is being called
        from another script.
    """

    save_fig = get_yes_or_no("Would you like to save these figures?: ")

    for title in movie_titles:
        # Get df of reviews for the book
        if not conn:
            with sqlite3.connect(f"{os.getcwd()}/review_dbs/reviews.db") as conn:
                df = pd.read_sql_query("""SELECT * FROM Reviews
                                          WHERE book_title
                                          LIKE ?;""", conn, params=[title + '%'])
            print(df)
        else:
            df = pd.read_sql_query("""SELECT * FROM Reviews
                                      WHERE book_title
                                      LIKE ?;""", conn, params=[title + '%'])

        if "matching_title" in df.columns:
            df.drop(columns=["matching_title"], inplace=True)

        mv_release = get_mv_release(title, conn)
        print(mv_release)
        # turn string dates into datetime objects, and sort the dataframe by date.
        df["review_date"] = pd.to_datetime(df["review_date"])
        df.set_index("review_date", inplace=True)
        df.sort_index(inplace=True)
        print(df)
        # change review scores to ints, if it cannot be converted to int, NaN.
        df["review_score"] = df["review_score"].apply(pd.to_numeric, errors='coerce')

        # drop rows with NaN values in them.
        df.dropna(inplace=True)

        # take rolling average of every n_reviews_rolling_avg review scores.
        df["review_score_rolling"] = df["review_score"].rolling(window=n_reviews_rolling_avg, center=False).mean()

        # dropping the top n_reviews_rolling_avg values, as they have no rolling average value
        df = df.iloc[(n_reviews_rolling_avg - 1):]
        plot_results(df, n_reviews_rolling_avg, title, mv_release, save_fig)


if __name__ == '__main__':
    main(movie_titles, 20)
