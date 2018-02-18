import sqlite3
from imdb import IMDb


def get_movie_id(dbfile, title, year):
    con = sqlite3.connect(dbfile)
    cur = con.cursor()
    cur.execute('''select id from movies
                   where movie=? and year=?''', (title, year))
    result = cur.fetchall()
    if len(result) == 0:
        # New movie - placeholder function until I figure out IMDB searching
        cur.execute('select id from movies')
        ids = cur.fetchall()
        idnum = max([i[0] for i in ids]) + 1

        # Add movie into movies
        cur.execute('''insert into movies(id, movie, year)
                       values (?, ?, ?)''', (idnum, title, year))
        con.commit()
    elif len(result) == 1:
        idnum = result[0][0]
    else:
        assert 0, 'Movie in database is duplicated.'

    con.close()
    return idnum
