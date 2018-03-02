# Table of Contents
1. [Overview](#overview)
    - [To Contribute](#to_contribute)
2. [Scripts](#scripts)
    - [mk_bklst.py](#make_booklistpy)
    - [scp_bks.py](#scp_bkspy)
    - [imdb_release.py](#imdb_releasepy)
    - [bk_plt.py](#bk_pltpy)
    - [all_bks.py](#all_bkspy)
    - [othr_chts.py](#othr_chtspy)

# Overview

This README should be used as a reference for all of the scripts located within the
`/GoodreadsEDA/GoodreadsEDA/` directory of this project. Currently, this section is a work in
progress and will be updated as more general purpose scripts are created/updated.

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
    six lines check to make sure what the user inputted, and what data is actually in the data
    consistent? Comment it.

2. Docstrings for function related changes.

  - Every single function must include an INFORMATIVE docstring to be submitted to this repo.
   No matter how clear you think your code is, always assume it isn't. Comments and
   docstrings are quite literally free. (I'm bad at this.)

  - Best practice is to write out what the inputs and outputs are for any function, that way
  no one has to read the function line by line to understand what it does. (I'm very bad at
  this.)

3. An Update to this file, and it's table of contents.
  - Every script will have it's own section in this file, and will also have it's own link
    to that section in the TOC. (I'm extremely bad at this.)

If in doubt, consider your audience might be users who are wholly unfamiliar with programming.
Or, assume I (who is looking over your code), am an idiot. Which is not a wholly unfounded assumption.

For questions or suggestions on formatting, etc, feel free to contact Trevor Grant at tjgran01@syr.edu.

# Scripts

## mk_bklst.py

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

2. Navigate to `/GoodreadsEDA/lists.py`.

3. In the bottom of the file there is a list of urls called `auth_urls`. Replace
the current values in this list with the author's you are interested in getting
review information for.

#### *This script gives as output*:

A .csv file located at: `/GoodreadsEDA/GoodreadsEDA/csv_files/booksnlinks.csv`. The .csv
file includes a row entry for every book on Goodreads based on the author list provided to
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
is to iterate through all the of the rows of a .csv file given as input, find a URL in each of
those rows, visit the URL using a headless browser, and pull selected information from that url and
store that information in a database.

*Note* All of this is done using the Selenium module. For more information on Selenium, visit:

https://www.seleniumhq.org/

#### *This file takes as input*:

The .csv file created by `mk_bklst.py`.

#### *This script gives as output*:

An SQLite3 database (more accurately: a table called 'Reviews' in the database) which will be
stored in this repository at `/GoodreadsEDA/GoodreadsEDA/review_dbs/reviews.db`. This table contains
every review that gave the book a 1 - 5 rating on the books goodreads.com page. It currently holds
the date of the review, the review score, the name of the user who left the review, as well as
the author's name, the book title, and the url from which the information was retrieved.

#### Notes, Future, etc:

Currently this script takes about 8 hours to run to generate the current dataset. Keep this in mind before deciding to run this script. Make sure the authors you have are the authors you want to have.

## imdb_release.py

##### Created: 2/2018
##### Created by: Trevor Grant
##### Email Support: tjgran01@syr.edu
##### Created for: Creating a table in SQLite3 database with all release dates for the movies based off of books in the dataset.

#### What this script does:

This script searches IMDB to find the release dates of the movies that were based off of books.
It then retrieves the release date from the movie's IMDB page, and stores that information in
a table named "Release_Dates" in the `/GoodreadsEDA/GoodreadsEDA/reviews.db` database.

#### *This file takes as input*:

A list of movie titles called `movie_titl`. Currently, the titles used in this project are already
hardcoded into the script `lists.py`. If you would like to use the program to investigate titles
other than the ones provided you will need to replace the strings in the list with the movie
titles you are interested in investigating. If you are only trying to visualize book scores over
time you can ignore this script entirely.

#### *This script gives as output*:

An SQLite3 database (more accurately: a table called 'Release_Dates' in the database) which will be
stored in this repository at `/GoodreadsEDA/GoodreadsEDA/review_dbs/reviews.db`. This table
contains the release dates of the films listed in the `movie_titl` list. It also currently stores
the title of the movie as it appears on IMDb.com

#### Notes, Future, etc:

The original hope with this script was to be able to simply `LEFT JOIN` on the movie title in order
to get a movie release for each book, but because books sometimes have slightly different names
then the films, this didn't work out in practice. If you are attempting to use this project as a
baseline for your own analysis. Try to give the two tables a common key so that a merge can
actually be successful.

This process was made much more of a pain in the a... ... neck when, halfway through working
on this script, I learned that this IMDb module is next to useless now. That is why the IMDb
package is only used to retrieve a movie ID, and Selenium is used to actually gather the release
date of the film. For more info:

https://imdbpy.sourceforge.io/

Or better yet, don't, because the site for it is down as well.

## bk_plt.py

##### Created: 2/2018
##### Created by: Trevor Grant
##### Email Support: tjgran01@syr.edu
##### Created for: Generating a line graph that looks at the rolling average of review scores of books that were adapted to film over time.

#### What this script does:

This script will iterate through the names in the same `movie_titl` list used in `imdb_release.py`,
make a pandas DataFrame of that particular book, get the release date listed in the "Release_Dates"
table in the `reviews.db` database, and plot all of this information in line graph, displaying the
movie release date as a solid line to indicate when a change in review scores might be expected.

#### *This file takes as input*:

In order for this script to work to it's full capacity both the "Reviews" and "Release_Date"
tables in the SQLite3 database must be generated via the scripts `scp_bks.py` and
`imdb_release.py`. However, if you are not interested in plotting a movie release date, and just
wish to get a visualization of a certain book over time, you can still run this script without the
movie release information. You will only need the output from `scp_bks.py` in that case.

#### *This script gives as output*:

A graph, or series of graphs depending on how many books the user is interested in plotting.

#### Notes, Future, etc:

Work will continue to be done on this script so that each book can act as a subplot, so that all
the books that the user wants to visualize will be displayed simultaneously, rather than having to
exit out of one graph in order to get the next, as this is tedious to do if the use is interested in looking at many books.

I didn't see a point in allowing users to print a solid orange line on a graph indicating when a
movie was released. If you disagree, and think I missed out on the next great app idea, which,
who knows? Feel free to send me a pull request. I only ask that you name the app "plttr" or
something with the equal ability to induce eye rolls.

## all_bks.py

##### Created: 2/2018
##### Created by: Trevor Grant
##### Email Support: tjgran01@syr.edu
##### Created for: Prints basic stats about book review scores out before and after the release of a movie adaptation of the book.

#### What this script does:

This script takes the average review score of all books before and after their release dates, and
compares it to the average review score of all books after their movie release dates. This script
looks at the overall change in the mean, the change in mean 1 year before the release of the film
to 1 year after, the change in mean 6 months before the release of the film and 6 months after, and
the change in mean 3 months before the release of the film and 3 months after.

#### *This file takes as input*:

In order for this script to work both the "Reviews" and "Release_Date" tables in the SQLite3
database must be generated via the scripts `scp_bks.py` and `imdb_release.py`.

#### *This script gives as output*:

Outputs to the console the mean, std, n, and t-test for each subdivision of time.

#### Notes, Future, etc:

This script still needs to be put into and better commented. Also, instead of printing
to the console, which is useless, it will export all of the data to either a .csv or
format it into a markdown or html table so that it can be more easily looked over.

## othr_chts.py

##### Created: 2/2018
##### Created by: Trevor Grant
##### Email Support: tjgran01@syr.edu
##### Created for: Creating charts from the information created bt all_bks.py.

#### What this script does:

This script was created as a quick and dirty way to make some extra data visualizations needed
for the writeup of this project. It's both unimpressive, and not useful for much of anything.

#### *This file takes as input*:

Nada, everything is hardcoded into this bad boy.

#### *This script gives as output*:

A line chart and a bar chart that were needed for `docs/WRITEUP.md`

#### Notes, Future, etc:

Nothing, I only included an explanation of it because it exists.
