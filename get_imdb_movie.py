import sqlite3
from imdb import IMDb


def get_imdb_movie(db, title, year):
    if type(db) == str:
        con = sqlite3.connect(db)
    else:
         con = db
    cur = con.cursor()
    cur.execute('''select id from movies
                   where movie=? and year=?''', (title, year))
    result = cur.fetchall()
    if len(result) == 0:
        ia = IMDb()
        search = ia.search_movie(' '.join((title, year)))
        if len(search) > 0:
            print('Movie to search for: {} ({})'.format(title, year))
            for i,m in enumerate(search):
                t = m['title'] if 'title' in m.keys() else None
                y = m['year'] if 'year' in m.keys() else None
                print('({}) {} ({})'.format(i+1, t, y))
            #num = input('Which movie did you watch (0 for none of these)? ')
            num = 1
            try:
                n = int(num)
            except:
                n = 0
            if n>0:
                # Get the IMDB id number
                movie = search[n-1]
                idnum = movie.getID()
                t = movie['title'] if 'title' in movie.keys() else title
                y = movie['year'] if 'year' in movie.keys() else year

                # Add movie into movies
                cur.execute('''insert into movies(id, movie, year)
                               values (?, ?, ?)''', (idnum, t, y))
                con.commit()
            else:
                idnum, movie = -1, None
        else:
            print('No possible movies found')

            # Need to choose a random, negative id number
            from numpy.random import randint
            cur.execute('select id from movies')
            ids_temp = cur.fetchall()
            all_ids = [i[0] for i in ids_temp]

            idnum = all_ids[0]
            while idnum in all_ids:
                idnum = randint(-100000, -1)
            idnum, movie = -1, {'title':title, 'year':year}
    elif len(result) == 1:
        idnum = result[0][0]
    else:
        assert 0, 'Movie in database is duplicated.'

    if type(db) == str:
        con.close()
    return idnum
