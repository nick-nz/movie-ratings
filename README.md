movie-ratings
=============

## What is it?

Retrieves Rotten Tomatoes ratings for all movies in a directory and its sub-directories and presents them, in a webpage along with the runtime and 'critics consensus'.

## Requirements

`pip install rottentomatoes jinja2`

## Configuration

The following values can be modified at the top of *movie_ratings.py*.
1 MOVIE_PATH is the directory of movies you wish to analyze.
2 TEMPLATE_PATH is the directory of the Jinja2 template (currently the repository root).
3 RESULTS_PAGE_NAME is the name of the output html file.
4 EXT is a set containing the file extensions you wish to look at.
