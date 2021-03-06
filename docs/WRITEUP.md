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
of a book will translate to a large uptick in sales ([Respers](http://marquee.blogs.cnn.com/2010/08/12/movies-based-on-books-increase-book-sales/)). People often
wish to read the original version of the story before seeing the film, or television
show, in order to compare the merits or both the original and adaptation. A reader
may also wish to get a deeper version of the story with the book compared to the
version they viewed on screen.

It comes as a surprise when a movie is better received than it's source material
(critically speaking, that is), so much so that this phenomenon requires further
investigation. Do we *actually* view the book as better than the film? And
if so, then *why?* or in *what way* to we view the book as a more valid
version of the story? Though there is theoretical literature explaining why
this phenomenon might be the case, few efforts using publicly avilable data have
corroborated these claims.

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

```/GoodreadsEDA/GoodreadsEDA/mk_bklst.py```

The urls used were retrieved and coded manually. For an overview of how the urls were obtained see
the "Inputting Your Own Authors" section in `README.md`.

Future versions of this project may update mk_bklst.py to allow for the author URLs to be
obtained by automation, so that a user only need to input a list of authors in order for the program
to run. `mk_bklst.py` then outputs a .csv file which included the URLs to every book each
author in the original author list had on avilable on Goodreads at that time. The .csv file is
included in this repository, and can be found at:

```GoodreadsEDA/GoodreadsEDA/csv_files/booksnlinks.csv```

For further documentation on `mk_bklst.py`, see the `README.md` located within
`mk_bklst.py`'s directory.

After the entire booklist was created the public facing review data avilable for that book on
Goodreads was then scraped and stored in an SQLite3 database. The resulting database is currently
located at:

```GoodreadsEDA/GoodreadsEDA/review_dbs/reviews.db```

The process was automated via the `scp_bks.py` script, which took the .csv file created from
`mk_bklst.py`, visited the URL for each entry, and retrieved every review score, username, and
review date from each review avilable on the site at that time.

Goodreads displays thirty reviews per page, and allows a user to view ten pages, totaling three
hundred reviews per book. Future versions of this script may also retrieve the review text from the
reviews, to allow for textual analysis. This current project, however, was only interested in
analyzing the review score, and so this feature was omitted. Another improvement might be to
integrate API calls, to see if more of the review data submitted to Goodreads could be combined with
the scraped data. However, the three hundred publicly avilable reviews per book were adequate for
the purposes of this project. For further documentation on `scp_bks.py`, see the `README.md`
located within `scp_bks.py`'s directory. Movie or television releases were also scraped, albeit
through a much less labor intensive process, via the `imdb_release.py` file, which iterated through
the original movie titles, searched imdb.com for the relevant release dates, and stored them in
another table (Release_Dates) within the `reviews.db` database.

After the database was formed individual books were plotted, along with their corresponding
movie release dates, on separate charts in order to get a better understanding of what (if anything)
was worth further exploration. This process was done using `bk_plt.py`. After Looking over the
resulting plots it was clear that the plots needed a little more refinement if they were to be
elucidating. `bk_plt.py` was then adjusted to plot only review scores between three to five (being
that it was **rare** for the book to dip below an average score of three), as well as adjusting the
plots to focus only on a year before and after the release of the movie to better highlight what
effect (in any) a film adaptation may have had on the reception of the book.

After the plots were generated, independent t-tests were performed between the mean review scores
before and after the movie release date in four different timeframes: The entire timeframe, one
year before the movie's release against one year after, six months before the movie's release
against six months after, and three months before the movie's release against three months after.
This process was accomplished using the `all_bks.py` script.

# Results:

## Individual Books.

![Figure1-1](https://github.com/tjgran01/GoodreadsEDA/blob/master/docs/img/FourFigs.png)

*Above: Four Line Charts indicating a particular book's rolling review score (n=20) from one
year before to one year after a screen adaptation's release date. The orange, solid, horizontal
line indicates the release date of a screen adaptation. For all single book figures created by
the project visit: `/docs/img/...`*

---

Visualizing certain books around the time of their release date did suggest some interesting trends.
Oftentimes the review scores of a book would begin to dip a few months before the release of a
screen adaptation and then spike shortly after the release of the film. However, in the aggregate
this trend vanished. Perhaps there are some similarities in these books that follow this pattern
that were not able to be explored via the current dataset, such as genre of the book, or how well
the screen adaptation was received.

## Overall:

The mean review score of all of the original books mentioned in the main `README.md` was:
3.92 (std=1.13). With the distribution of scores below:

---

|Review Score|# of Scores|        
|------------|-----------|
|     5.0    |    2986   |
|     4.0    |    2618   |
|     3.0    |    1240   |
|     2.0    |    621    |
|     1.0    |    371    |

---

![ttl_dist_scores](https://github.com/tjgran01/GoodreadsEDA/blob/master/docs/img/ttl_review_scores.png)

As mentioned earlier the overall results were heavily skewed towards positive ratings with 71.5% of
all reviews in the dataset being either a four or a five. A reason for this might be that people
only feel inclined to review a book once they have finished it. Considering the time investment
involved in finishing a book, if someone does not like a book they are unlikely to finish it and
therefore unlikely to leave a negative review of it. If this is the case then this positive skew should be
expected across all reviews on Goodreads.com. Another possibility for the existence of this positive
skew could be that since all of these books were adapted into films, they were presumably well
received amongst readers prior to the film's release, making the production of the film less risky
of an investment for the studio involved.

Whatever the case may be for the existence of this positive skew, keeping it in mind can help to
conceptualize what variances in scores overtime might mean. If an average review score for a period
of time drops from 3.4 to 3.2, this could be seen as more significant a change than if the scores
were evenly or normally distributed.

## Before and After Movie Releases:

---

|                                |   3mo     |   6mo     |   1yr     |   All    |
|--------------------------------|-----------|-----------|-----------|----------|
| Mean Before (In Stars)         |   4.11    |   3.98    |   3.89    |   3.88   |
| Mean After (In Stars)          |   3.93    |   3.89    |   3.84    |   3.95   |
| **Mean Difference (In Stars)** | **-0.18** | **-0.08** | **-0.05** | **0.06** |
| Std. Before                    |   1.08    |   1.17    |   1.2     |   1.20   |
| Std. After                     |   1.17    |   1.16    |   1.17    |   1.09   |
| T-Statistic                    |   -1.83   |   -1.17   |   -0.94   |   2.42   |
| P-Value                        |   .06     |   0.24    |   0.35    |   0.02   |
| N (Both)                       |   285     |   440     |   798     |   2519   |

---

![mean_diff](https://github.com/tjgran01/GoodreadsEDA/blob/master/docs/img/mean_diff.png)

*Above: A line chart plotting the difference in average review scores of different time periods
before and after a book's release (3mo, 6mo, 1yr, and All Reviews). Values in the red section of
the chart indicate that the score was negative, or that the average review score for that timeframe
was **lower** following the film's release than prior. Values in green indicate that the average
review score for that time frame was positive, or that the average review score for that
timeframe was **higher** following the film's release than prior.*

---

The final analysis involved taking the entire collection of books, splitting them into separate
groups based on different times before and after the release of the film, and balancing the
datasets to be of equal size (n), so that more accurate t-tests could be performed on the samples.
The results of the computations can be found in the table above. A visualization was also created
to help show the difference in means for all of the different sets of data. Values in red indicate
that the change in mean was negative, or that books were reviews less favorably in the time after
the release of the film compared to before.

Overall, it appears that books are more favorably reviewed after the release of the film. The
t-test results generated a t-statistic of 2.344 (p=.02).

# Discussion

Although there seems to be a slight change in review scores over time based on the overall
difference in review scores reported before and after the release of a film the change
is a rather small (.06 of a 'star') difference. Though this difference could be considered
statistically significant it is possible that there are other confounding factors generating the
results seen in this analysis, especially taking into consideration that the review scores in this
sample decreased with greater magnitude closer to the the release date of the film. In order to be
certain that the release of a film has a *positive* impact on the reception of a book more
investigation is needed, preferably with a control group of books that were not given a screen
adaptation to rule out the possibility that average review scores increase over time regardless
of whether or not they were given a screen adaptation.

The findings posted above do not indicate that a clear effect exists over the entire dataset, at
least not to a magnitude that warrants further investigation into how an author's other book
reviews are affected by the release of a film.

Others using Goodreads.com as a sample should be aware of the potential skew within the data,
mentioned in the Results (Overall) section of this writeup, and should consider that skew when
working out their final analysis. The low differences in means in this particular project could be
attributable to this effect.

Another interesting project that could come out of these findings would be to see if one could
train a model to predict based only on review data if a book had been adapted to the screen. Other
variables to consider to improve upon this project in future iterations would be to look at volume
of reviews over a given period of time, which could indicate that although a book isn't reviewing
better, it could be gaining popularity due to the film adaptation. Another project could be to
perform a textual analysis, looking for certain words, or factoring word count in order to give a
little more depth to the scores beyond the five point rating scale provided by Goodreads. A
combination of the projects mentioned above may give better insights, or better results, than the
ones found in this analysis. Though it should be mentioned that some of the above projects would
likely require access to the entire review dataset from Goodreads.com which is beyond the scope of
this particular project.
