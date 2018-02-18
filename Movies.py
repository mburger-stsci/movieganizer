import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import os
from read_movie_list import read_movie_list
matplotlib.rcParams.update({'font.size': 16})

pd.set_option('display.notebook_repr_html', False)
pd.set_option('display.max_columns', 7)
pd.set_option('display.max_rows', 10)
pd.set_option('display.width', 100)

# Read in the list
movies = read_movie_list('MovieList.dat')
names = set(movies.Movie.tolist())

#print(movies)
print('Total Number of Movies Watched: %s' % len(movies))
print('Unique Movies Watched: %s' % len(names))

# Plot histogram of decade movie made
yr = np.array(movies.Year)
x = range(1930,2030, 10)
h, e = np.histogram(yr, bins=x)

fig, axes = plt.subplots(figsize=(10,8))
axes.bar(x[:-1], h, width=10, tick_label='', edgecolor='black')
axes.set_ylabel('Count')
axes.set_title('Decade Movies were Made')
for i in range(len(h)):
    axes.text(x[i], 0, str(x[i])+"'s", rotation=90, horizontalalignment='right', 
            verticalalignment='top')
fig.savefig('Movies_decade.png')

# pie chart of medium
allmed = sorted(movies.Medium.unique())
nmed = movies.Medium.value_counts()
nmed.sort_index(inplace=True)
x0 = list(nmed.index)
y0 = nmed.values
p2 = plt.pie(y0, labels=x0)
plt.title('Medium of Movies Watched')
plt.savefig('Movies_medium_pie.png')
plt.close()

# histogram of medium
plt.figure(figsize=(10,8))
plt.bar(np.arange(len(y0)), y0, tick_label='')
plt.ylabel('Count')
plt.title('Medium of Movies Watched')
for i in range(len(x0)):
    plt.text(i+.3, 0, x0[i], rotation=90, horizontalalignment='right', 
            verticalalignment='top')
plt.savefig('Movies_medium.png')
plt.close()

# histogram of year movie watched
yr = [d.year for d in movies['Date Watched']]
x2 = np.arange(min(yr),max(yr)+2)
h2, x2 = np.histogram(yr, bins=x2)
plt.figure(figsize=(10,8))
plt.bar(x2[:-1], h2, tick_label='')
plt.ylabel('Count')
plt.title('Years Movies Were Watched')
plt.rcParams['xtick.labelsize'] = 16 
for i in range(len(x2[:-1])):
    plt.text(x2[i]+.3, 0, str(x2[i]), rotation=90, horizontalalignment='right', 
            verticalalignment='top')
plt.savefig('Movies_yearwatched.png')
plt.close()

# output to other forms
movies.to_html('Movies.html')
#movies.to_latex('Movies.tex')
#movies.to_excel('Movies.xls')

# Reformat MovieList - only needed once
rewrite = True
if rewrite:
    os.system('cp MovieList.dat MovieList.bak')
    f = open('MovieList.dat', 'w')
    f.write('{:^40} : {} : {:12} : {:^20}\n'.format('Movie', 'Year', 'Date Watched', 
        'Medium'))
    for i,row in movies.iterrows():
        f.write('{:40} : {} : {:12} : {:20}\n'.format(row['Movie'], row['Year'], 
            row['Date Watched'].strftime('%Y-%m-%d'), row['Medium']))
    f.close()

os.system('open *.png')

