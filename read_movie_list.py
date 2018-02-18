import pandas as pd

def read_movie_list(mfile):
    # Read in the list
    movies = pd.read_csv(mfile, delimiter=':')

    # Clean up the column names
    for col in movies.columns:
        movies = movies.rename(columns={col:str(col).strip()})
    for col in movies.columns:
        try:
            movies[col] = movies[col].str.strip()
        except:
            pass

    # Convert date watched to datetime
    movies['Date Watched'] = pd.to_datetime(movies['Date Watched'])
#    movies.set_index('Date Watched', inplace=True)

    return movies

