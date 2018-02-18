import sqlite3
from datetime import date

def textbackup(dbfile):
    # Make an ascii table of database
    con = sqlite3.connect(dbfile)
    cur = con.cursor()

    # Make the watched table
    cur.execute('''select movies.movie, movies.year,
                          watched.date_watched, watched.medium
                   from movies, watched
                   where movies.id = watched.id''')

    result = cur.fetchall()
    result.sort(key=lambda x: x[2], reverse=True)

    with open('MovieList.dat', 'w') as f:
        for r in result:
            f.write('{:30} : {} : {} : {:10}\n'.format(
                r[0], r[1], r[2], r[3]))


    # make the to watch table
    cur.execute('''select movie, year
                   from movies, towatch
                   where movies.id = towatch.id''')
    result = cur.fetchall()

    with open('MoviesToWatch.dat', 'w') as f:
        for r in result:
            f.write('{} : {}\n'.format(r[0], r[1]))
