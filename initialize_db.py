import sqlite3
from datetime import date

def get_movie_list(con):
    # Add in the old list of movies
    cur = con.cursor()
    movielist = []
    with open('MovieList.dat') as f:
        for line in f.readlines():
            pieces = line.split(':')
            l = tuple(p.strip() for p in pieces)
            movielist.append(l)

    allmovies = set((a, b) for a, b, _, _ in movielist)
    for i, movie in enumerate(allmovies):
        cur.execute('''insert into movies(id, movie, year)
                       values (?, ?, ?)''', (i, movie[0], movie[1]))
    con.commit()

    # Sort movies watched by date
    movielist.sort(key=lambda x: x[2])

    # make table of watched movies
    for movie in movielist:
        cur.execute('''select id from movies
                       where movie=? and year=?''',
                    (movie[0], movie[1]))

        ii = cur.fetchall()
        assert len(ii) == 1, 'A movie made it in twice'

        ii = ii[0][0]
        try:
            yr, mon, dy = movie[2].split('-')
            cur.execute('''insert
                           into watched(id, date_watched, medium)
                           values (?, ?, ?)''',
                        (ii, date(int(yr), int(mon), int(dy)), movie[3]))
        except:
            assert 0, '{}: Date format error'.format(movie[2])
        con.commit()

    # Do the same for MoviesToWatch.dat
    towatchlist = []
    with open('MoviesToWatch.dat') as f:
        for line in f.readlines():
            pieces = line.split()

def initialize_db(dbfile):
    # Create the database
    con = sqlite3.connect(dbfile)
    cur = con.cursor()

    # Movies table
    movie_sql = '''create table movies (
                       id integer,
                       movie text,
                       year integer,
                       url text)'''
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
    cur.execute('''create table towatch (id integer primary key)''')
    con.commit()

    # Close the connection
    con.close()
