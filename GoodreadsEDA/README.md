# Table of Contents
1. [Overview](#overview)
    - [To Contribute](#to_contribute)
2. [Scripts](#scripts)
    - [make_booklist.py](#make_booklist.py)
    - [scp_bks.py](#scp_bks.py)
    - [imdb_release.py](#imdb_release.py)
    - [bk_plt.py](#bk_plt.py)
    - [all_bks.py](#all_bks.py)

# Overview

This README should be used as a reference for all of the scripts located within the
`/GoodreadsEDA/GoodreadsEDA/` directory of this project. Currently, this section is a work in
progress and will be updated as more general purpose scripts are created/updated

### To Contribute.

I will try to follow my own rules to the best of my ability, so that clear documentation
is provided for both contributors and users of this project.

This means that for every commit a developer makes to this repo they also need to include:

1. In line comments for non-function related changes.

  - Use your head when it comes to this, if you're just printing something out, you
    probably don't exhaustive documentation, but things like indexing certain elements
    in lists should probably include an in line comment explaining what you are grabbing
    from a list because it is not always clear.

  - You don't need to comment every single line, but should highlight what certain sections
    of the code are doing. Do these four lines process textual data? Comment it. Do these
    six lines check to make sure what the user inputed, and what data is actually in the data
    consistent? Comment it.

2. Docstrings for function related changes.

  - Every single function must include an INFORMATIVE docstring to be submitted to this repo.
   No matter how clear you think your code is, always assume it isn't. Comments and
   docstrings are quite literally free.

  - Dest practice is to write out what the inputs and outputs are for any function, that way
  no one has to read the function line by line to understand what it does.

3. An Update to this file, and it's table of contents.
  - Every script will have it's own section in this file, and will also have it's own link
    to that section in the TOC.

If in doubt, consider your audience might be users who are wholly unfamiliar with programming.
Or, assume I (who am looking over your code), am an idiot. Which is not a wholly unfound assumption.

For questions or suggestions on formatting, etc, feel free to contact Trevor Grant at tjgran01@syr.edu.

# Scripts

## make_booklist.py

##### Created: 1/2018
##### Created by: Trevor Grant
##### Email Support: tjgran01@syr.edu
##### Created for: Taking a list of author URLs on Goodreads.com, and outputting a .csv file that includes all of the urls for that author's books.

#### What this script does:

This script is a quick and dirty method for generating all the urls that will need to be scraped
by the next script in this repository `scp_bks.py`.

#### *This file takes as input*:

A list of urls called `auth_urls`. Currently, the authors used in this project are already
hardcoded into the project. If you would like to use the program to investigate authors other than
the ones provided you will need to:

1. Navigate to the author in question's book list page on
www.goodreads.com. The links come in a format such as the one listed below:

https://www.goodreads.com/author/list/author_id.author_name

  The easiest way to find this page is to:
  - Search for the author on www.goodreads.com,
  - Navigate to the author's page, and click on the link on the page that says
  "`author_name`'s books."
  - Copy the page url.

2. Navigate to `/GoodreadsEDA/make_booklist.py`.

3. In the top of the file there is a list of urls called `auth_urls`. Replace
the current values in this list with the author's you are interested in getting
review information for.

#### *This script gives as output*:

A .csv file located at: `/GoodreadsEDA/GoodreadsEDA/csv_files/booksnlinks.csv`. The .csv
file includes the a row entry for every book on Goodreads based on the author list provided to
the script as input. Each entry includes the author's name, the book's name, and the URL to find
that book on Goodreads.com

#### Notes, Future, etc:

Future updates might expand this script, or create another script that will allow just author
names to be inputted, rather than forcing the user to generate the URLs themselves.

## scp_bks.py

##### Created: 1/2018
##### Created by: Trevor Grant
##### Email Support: tjgran01@syr.edu
##### Created for: Creating a SQLite3 database with all of the public facing reviews for each of the books in the author list.

#### What this script does:

This script is what will be used to generate the dataset to run analysis on. It's primary function
is to iterate through all the of the rows a .csv file given as input, find a URL in each of those
rows, visit the URL using a headless browser, and pull selected information from that url and
store that information in a database.

*Note* All of this is done using the Selenium module. For more information on Selenium, visit:

https://www.seleniumhq.org/

#### *This file takes as input*:

The .csv file created by `make_booklist.py`.

#### *This script gives as output*:

An SQLite3 database (more accurately: a table called 'Reviews' in the database) which will be
stored in this repository at `/GoodreadsEDA/GoodreadsEDA/review_dbs/reviews.db`. This table contains
every review that gave the book a 1 - 5 rating on the books goodreads.com page. It currently holds
the date of the review, the review score, and the name of the user who left the review as well as
the author's name, the book title, and the url from which the information was retrieved.

#### Notes, Future, etc:

Currently this script takes about 8 hours to run to generate the current dataset. Keep this in mind before deciding to run this script. Make sure the authors you have are the authors you want to have.

## imdb_release.py

##### Created: 2/2018
##### Created by: Trevor Grant
##### Email Support: tjgran01@syr.edu
##### Created for: Creating a SQLite3 database with all of the public facing reviews for each of the books in the author list.

#### What this script does:

This script searches IMDB to find the release dates of the movies that were based off of books.
It then retreieves the release date from the movie's IMDB page, and stores that information in
a table named "Release_Dates" in the `/GoodreadsEDA/GoodreadsEDA/reviews.db` database.

#### *This file takes as input*:

A list of movie titles called `movie_titl`. Currently, the titles used in this project are already
hardcoded into the script. If you would like to use the program to investigate titles other than
the ones provided you will need to replace the strings in the list with the movie titles you are
interested in investigating.

#### *This script gives as output*:

An SQLite3 database (more accurately: a table called 'Release_Dates' in the database) which will be
stored in this repository at `/GoodreadsEDA/GoodreadsEDA/review_dbs/reviews.db`. This table contains
the release dates of the films listed in the `movie_titl` list. It also currently stores the title
of the movie.

#### Notes, Future, etc:

The original hope with this script was to be able to simply `LEFT JOIN` on the movie title in order
to get a movie release for each book, but because books sometimes have slightly different names
then the films, this didn't work out in practice. If you are attempting to use this project as a
baseline for your own analysis. Try to give the two tables a common key so that a merge can actually
be successful.
