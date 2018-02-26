import sqlite3
from datetime import date
from get_imdb_movie import get_imdb_movie

def get_movie_list(con):
    # Add in the old list of movies
    cur = con.cursor()
    movielist = []
    with open('MovieList.dat') as f:
        for line in f.readlines():
            pieces = line.split(':')
            l = tuple(p.strip() for p in pieces)
            if len(l) != 4:
                print(l)
            movielist.append(l)

    for m in movielist:
        if '_' in m[0]:
            m[0].replace('_', ':')

    # Sort movies watched by date
    movielist.sort(key=lambda x: x[2])

    # Unique list of movies
    allmovies = set((a, b) for a, b, _, _ in movielist)

    for movie in allmovies:
        # Find movie in imdb and
        idnum = get_imdb_movie(con, movie[0], movie[1])

        # Insert movie in to watched movie table
        for watched_movie in movielist:
            if ((watched_movie[0] == movie[0]) and
                (watched_movie[1] == movie[1])):
                yr, mon, dy = watched_movie[2].split('-')
                cur.execute('''insert
                               into watched(id, date_watched, medium)
                               values (?, ?, ?)''',
                            (idnum,
                             date(int(yr), int(mon), int(dy)),
                             watched_movie[3]))
                con.commit()


def initialize_db(dbfile):
    # Create the database
    con = sqlite3.connect(dbfile)
    cur = con.cursor()

    # Movies table
    movie_sql = '''create table movies (
                       id integer,
                       movie text,
                       year integer)'''
    cur.execute(movie_sql)
    con.commit()

    # Watched table
    cur.execute('''create table watched (
                        viewnum integer primary key autoincrement,
                        id integer,
                        date_watched text,
                        medium text)''')
    con.commit()

    # Populate tables from MovieList.dat and MoviesToWatch.dat
    get_movie_list(con)

    # Make table of movies to watch
    cur.execute('''create table towatch (
                        id integer primary key,
                        date_added text)''')
    con.commit()

    # Close the connection
    con.close()
