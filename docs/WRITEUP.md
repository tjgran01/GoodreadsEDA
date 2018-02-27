# Table of Contents
1. [Introduction](#introduction)
2. [Methods](#methods)
3. [Results](#results)
4. [Discussion](#Discussion)

# Introduction

It is a common notion amongst the reading populace that film is often unable
to capture some of the main elements that make a work of literary fiction so memorable.
The medium of film, it is argued, as a result of either time constraints, inability
to adequately portray an interior monologue from a first person perspective, or
that film as a whole is a collaborative medium and writing is solitary, often falls
short of the bar that was set by the work from which the film drew it's inspiration.

This concept isn't foreign to those outside of reading circles. It is well known
amongst literary publishers that an upcoming film or television program based off
of a book will translate to a large uptick in sales < citation needed >. People often
wish to read the original version of the story before seeing the film, or television
show, in order to compare the merits or both the original and adaptation. A reader
may also wish to get a deeper version of the story with the book compared to the
version they viewed on screen.

It comes as a surprise when a movie is better received than it's source material
(critically speaking, that is), so much so that this phenomenon requires further
investigation. Do we *actually* view the book as better than the film? And
if so, then *why?* or in *what way* to we view the book as a more valid
version of the story? Though there is a vast theoretical literature explaining why
this phenomenon might be the case, few efforts using publicly avilable data have
corroborated these claims < citation needed >.

The project aims investigate a small portion of this overarching question. Namely,
does the creation of a film or television show have a significant impact on how
people rate a book? Further, if an effect does exist as a result of an adaptation,
does this have any relation or impact on the author's other works?

# Methods

A list of twenty two authors who had one or more of their books adapted for either
film or television was created along with their book that was adapted for screen.
The final list used in the analysis for this version of the writeup is contained
within the primary `README.md` of this repository, and, as such, will not be reiterated
here. Authors were chosen based on a few *loose* criteria: That the author primarily
or exclusively wrote works of fiction, that the author had at least one other book
besides the book that had a screen adaptation, and that the author didn't have more than
four screen adaptations. The first criteria was set to to exclude cases like David
McCullough, whose non-fiction books have been adapted into historical dramas, as well as
contemporary non-fiction authors whose books are adapted into a documentaries, or other
non-fiction works. The second criteria was included to ensure that analysis could be
performed on the author's other works as a point of reference, or to act as a control
for the work that was given an adaptation. The third criteria was included to avoid large
names in the industry, such as Stephen King, whose various works have been given
multiple screen adaptations throughout the years, as cases like King's could have
the potential to act as an outliner and confound the results from the rest of the dataset.

After the authors had been chosen each of their individual https://www.goodreads.com book list
pages were scraped to obtain the whole collection of books avilable on the site. The process was
automated by:

```/GoodreadsEDA/GoodreadsEDA/make_booklist.py```

The urls used were retrieved and coded manually. For an overview of how the urls were obtained see
the "Inputting Your Own Authors" section in `README.md`.

Future versions of this project may update make_booklist.py to allow for the author URLs to be
obtained by automation, so that a user only need to input a list of authors in order for the program
to run. `make_booklist.py` then outputs a .csv file which included the URLs to every book each
author in the original author list had on avilable on Goodreads at that time. The .csv file is
included in this repository, and can be found at:

```GoodreadsEDA/GoodreadsEDA/csv_files/booksnlinks.csv```

For further documentation on `make_booklist.py`, see the `README.md` located within
`make_booklist.py`'s directory.

After the entire booklist was created the public facing review data avilable for that book on
Goodreads was then scraped and stored in an SQLite3 database. The resulting database is currently
located at:

```GoodreadsEDA/GoodreadsEDA/review_dbs/reviews.db```

in this repository. The process was automated via the `scp_bks.py` script, which took the
.csv file created from `make_booklist.py`, visited the URL for each entry, and retrieved every
review score, username, and review date from each review avilable on the site at that time.

Goodreads displays thirty reviews per page, and allows a user to view ten pages, totaling three
hundred reviews per book. Future versions of this script may also retrieve the review text from the
reviews, to allow for textual analysis. This current project, however, was only interested in
analyzing the review score, and so this feature was omitted. Another improvement might be to
integrate API calls, to see if more of the review data submitted to Goodreads could be combined with
the scraped data. However, the three hundred publicly avilable reviews per book were adequate for
the purposes of this project. For further documentation on `scp_bks.py`, see the `README.md`
located within `scp_bks.py`'s directory.

# Results

<small>Figure 1-1</small>
![Figure1-1](https://github.com/tjgran01/GoodreadsEDA/blob/master/docs/img/single_bks's.png)

# Discussion
