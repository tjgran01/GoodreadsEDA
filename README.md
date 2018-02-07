# GoodreadsEDA
### By: Trevor Grant

This project was created the satisfy the requirements for the EDA project
at K2 Data Science bootcamp.

## Goal:

This project is meant to take a list of authors and store all of the public
facing review information on Goodreads.com about each of that author's books into
a sqlite3 database so that exploratory data analysis may be performed on the
scraped data.

## Quickstart.

To run all the scripts in the proper order navigate to `GoodreadsEDA/GoodreadsEDA
/main.py`.

If you wish to run the scripts individually they should be run in this order:

1. `./make_booklist.py`
2. `./scp_bks.py`

As `scp_bks.py` depends on a .csv file in created as output for `make_booklist.py`
in order to run.

## Current Author List:

The data the current iteration of the project is looking into is lesser known
author's who have had at least one of their books optioned for either film or
television.

The current author list for the project is below:

* Liane Moriarty – Big Little Lies (series)
* Jojo Moyes – Me Before You
* Dave Eggers – The Circle
* André Aciman – Call Me By Your Name
* Nicola Yoon – Everything Everything
* Emma Donoghue – Room
* Colm Tóibín – Brooklyn
* Fredrik Backman – A Man Called Ove
* Ransom Riggs - Miss Peregrine’s Home for Peculiar Children
* Paula Hawkins – The Girl on the Train
* M.L. Stedman – The Light Between Oceans
* Rick Yancey – The 5th Wave
* Lisa Genova – Still Alice
* Kody Keplinger – The D.U.F.F.
* Uzodinma Iweala – Beasts of No Nation
* Kevin Wilson – The Family Fang
* Jonathan Tropper – This Is Where I Leave You
* Jesse Andrews – Me and Earl and the Dying Girl
* Margaret Atwood – The Handmaid’s Tale
* Herman Koch – The Dinner
* Ben Fountain - Billy Lynn’s Long Halftime Walk
* Orson Scott Card – Ender’s Game
* Gayle Forman – If I Stay

### Inputing your own authors.

If you would like to use the program to investigate authors other than the ones
provided you will need to:

1. Navigate to the author in question's book list page on
www.goodreads.com. The links come in a format such as the one listed below:

https://www.goodreads.com/author/list/`author_id`.`author_name`

The easiest way to find this page is to:
- Search for the author on www.goodreads.com,
- Navigate to the author's page, and click on the link on the page that says
"`author_name`'s books."
- Copy the page url.

2. Inside of this project navigate to `/GoodreadsEDA/make_booklist.py`.

3. In the top of the file there is a list of urls called `auth_urls`. Replace
the current values in this list with the author's you are interested in getting
review information for.

## EDA Questions.

The project as it currently stands is interested in exploring two questions:

1. Does a movie / television show made about a work of fiction effect the average
rating of the <em>book</em>?

2. If an effect <em>exists</em> does it carry over to the author's other works?
