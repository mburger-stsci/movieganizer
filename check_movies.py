import os
import sqlite3
import webbrowser
import time


con = sqlite3.connect('Movies.sql3')
cur = con.cursor()

cur.execute('''select watched.id, movies.movie,
               movies.year, watched.date_watched
               from watched, movies
               where watched.id = movies.id
               order by watched.date_watched''')
for row in cur.fetchall():
    print(row)
    url = 'http://www.imdb.com/title/tt{:07d}/'.format(row[0])
    print(url)
    webbrowser.open(url)
    #time.sleep(2)
    input('type something. ')
