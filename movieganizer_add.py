import sqlite3
from get_imdb_movie import get_imdb_movie
from datetime import date


def add_watched_movie(dbfile):
    # Ask what movie was watched
    title = input('What movie did you watch? ').strip()
    year = input('What year was it made? ').strip()
    good = False
    while not good:
        d = input('When did you watch it? ').strip()
        try:
            yr, mon, dy = d.split('-')
            when = date(int(yr), int(mon), int(dy))
            good = True
        except:
            print('Enter a date in form YYYY-MM-DD')

    medium = input('How did you watch it? ').strip()

    # Get movie id from database or add it
    idnum, movie = get_movie_id(dbfile, title, year)

    # Remove from to watch list if necessary
    con = sqlite3.connect(dbfile)
    cur = con.cursor()
    cur.execute(''' select id from towatch where id = ?''', (idnum, ))
    ii = cur.fetchall()
    if len(ii) == 1:
        cur.execute('''delete from towatch where id = ?''', (idnum, ))
        con.commit()
        print('Removed {} ({}) from to watch list.'.format(title, year))
    elif len(ii) > 1:
        assert 0, 'Movie was on to watch list more than once'
    else:
        pass

    # Add movie to watched list
    cur.execute('''insert
                   into watched(id, date_watched, medium)
                   values (?, ?, ?)''', (idnum, when, medium))
    con.commit()
    con.close()


def add_to_watch(dbfile):
    # Ask which movie to watch
    title = input('What movie do you want to watch? ').strip()
    year = input('What year was it made? ').strip()

    # Get movie id from database or add it
    idnum, movie = get_movie_id(dbfile, title, year)

    # Check to see if movie is already in watch list
    con = sqlite3.connect(dbfile)
    cur = con.cursor()
    cur.execute('select * from towatch where id = ?', (idnum, ))
    result = cur.fetchall()

    if len(result) == 0:
        # Add to watch list
        cur.execute('insert into towatch(id) values (?)', (idnum, ))
        con.commit()
        con.close()
    else:
        print('Movie is already in your watchlist')
