from os import walk, getcwd
from operator import itemgetter
import re

from rottentomatoes import RT
from jinja2 import Environment, FileSystemLoader

MOVIE_PATH = 'C:\Users\Nick\Videos'
TEMPLATE_PATH = getcwd()
RESULTS_PAGE_NAME = 'my_movies'

EXT = {'avi', 'mp4', 'mkv'}

results = []
ids = set()


def get_movies():
    movies = []
    for (dirpath, dirnames, filenames) in walk(MOVIE_PATH):
        for index, filename in enumerate(filenames):
            extension = filename.split('.')[-1]
            if extension not in EXT:
                filenames.pop(index)
        movies.extend(filenames)
    print "Found %d movies" % len(movies)
    return movies


def get_title_and_year(f_name):
    if len(f_name) > 1:
        temp = f_name
        f_name = list()
        f_name.append('.'.join(temp))
    f_name = re.split('\[(.*?)\]', f_name[0])  # Extract the year from within square brackets eg. 'Toy Story [1995]'
    if f_name[-1] == '':
        f_name.pop()
    if len(f_name) == 1:
        f_title = f_name[0].strip()
    else:
        f_title = ' '.join(f_name[:-1]).strip()
    f_year = False
    if len(f_name) == 2:  # Likely contains the title and year.
        f_year = f_name[1]
    return f_title, f_year


def save_movie(selected_movie):
    movie_dict = {}
    try:
        movie_dict['title'] = selected_movie['title']
        movie_dict['rating'] = selected_movie['ratings']['critics_score']
        movie_dict['year'] = selected_movie['year']
        movie_dict['runtime'] = selected_movie['runtime']
        movie_dict['link'] = selected_movie['links']['alternate']
        movie_dict['critics_consensus'] = selected_movie['critics_consensus']
    except KeyError:
        pass
    print movie_dict.get('title'), movie_dict.get('rating')
    return movie_dict


def try_save_movie(selected_movie):
    # Prevent duplicates and results with no data
    if selected_movie['id'] not in ids and selected_movie['ratings']['critics_score'] != -1:
        results.append(save_movie(selected_movie))
        ids.add(selected_movie['id'])


def create_results_webpage(results):
    env = Environment(loader=FileSystemLoader(TEMPLATE_PATH))
    template = env.get_template('display.html')
    output_from_parsed_template = template.render(results=results)

    # Save the results
    with open(RESULTS_PAGE_NAME + '.html', "wb") as fh:
        fh.write(output_from_parsed_template)


for movie in get_movies():
    name = movie.split('.')[:-1]  # Remove file extension
    title, year = get_title_and_year(name)

    if title:
        search_results = RT().search(title)
    else:
        continue
    if year:
        for result in search_results:
            if str(result['year']) == year:
                try_save_movie(result)
                break  # Just take the first search result with matching year.
    elif len(search_results) > 0:
        try_save_movie(search_results[0])
    else:
        continue # No results for this movie.

results = sorted(results, key=itemgetter('rating'), reverse=True)

create_results_webpage(results)