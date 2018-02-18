#!/usr/bin/env python

import os
import sqlite3
import argparse
from textbackup import textbackup

#DEFAULT_FILE = '/Volumes/mburger/Dropbox/Movies/Movies.sql3'
DEFAULT_FILE = '/Users/mburger/Personal/Movies/Movies.sql3'


def run_stats(dbfile):
    con = sqlite3.connect(dbfile)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description='Keep track of movies watched and movies to watch.')
    parser.add_argument('action', type=str, default=None,
                        help='Action to perform')
    parser.add_argument('-f', dest='dbfile', help='Database file',
                        default=DEFAULT_FILE, type=str)

    args = parser.parse_args()

    if args.action == 'reset':
        from initialize_db import initialize_db
        if os.path.isfile(args.dbfile):
            os.remove(args.dbfile)
        initialize_db(args.dbfile)
    elif args.action == 'watched':
        from movieganizer_add import add_watched_movie
        add_watched_movie(args.dbfile)
    elif args.action == 'towatch':
        from movieganizer_add import add_to_watch
        add_to_watch(args.dbfile)
    elif args.action == 'delete':
        delete_movie(args.dbfile)
    elif args.action == 'stats':
        run_stats(args.dbfile)
    elif args.action == 'list':
        run_list_movies(args.dbfile)
    else:
        print('Available actions:\n'
              '\treset -> Reset the database\n'
              '\twatched -> Add a movie you watched\n'
              '\ttowatch -> Add a movie you want to watch\n'
              '\tdelete -> Remove a movie from the database\n'
              '\tlist -> List movies watched & watch list')

    textbackup(args.dbfile)
