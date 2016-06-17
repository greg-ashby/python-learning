import numpy as np
import pandas as pd

df = pd.DataFrame({'A': ['foo', 'bar', 'foo', 'bar',
                         'foo', 'bar', 'foo', 'foo'],
                   'B': ['one', 'one', 'two', 'three',
                         'two', 'two', 'one', 'three'],
                   'C': np.random.randn(8),
                   'D': np.random.randn(8)},
                  index=['i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii'])

print
print '***** a simple dataframe *****'
print df

print
print '***** selecting a column *****'
print df['A']  # NOTE, equivalent to df.A
print df.A

print
print '***** selecting multiple columns *****'
# NOTE df[['A']] returns a data frame, df['A'] returns a series
print df[['A', 'B']]

print
print '***** selecting rows *****'
print df[0:2]
print df[[True, True, False, False, False, False, False, False]]
print df['i': 'ii']

print
print '***** selectors *****'
print df[['A', 'B']][0:2]['ii':]['A']

# ok, so format for selectors is:
# df<selectors>
# where a selectors can be any number of a selector, in any order, and a selector can be:
# [column_name] <- returns a series
# [[list_of_column_names]]
# [x:y] <- same as python list slice, works on rows, except x & y can be integers (row position) or strings (row index names)
#       NOTE: can also use steps, like 0:5:2 (select every second row between 0 and 5) or ::-1 (select all in reverse order)
# [[list_of_booleans]] <- True for rows to select
# callable function? TODO figure out how this works, or is that just for loc/iloc?
#
# what about loc, iloc?

#.loc selects based on labels
#.iloc selects based on positions
# both take a row and (optional) column selector
# both include the start and stop bounds
# where the selectors can be:
# - a single label (or integer for iloc)
# - a list/array of labels (integers for iloc)
# - a slice (x:y:z) of labels/integers (here's where loc will treat x/y as labels instead of integer positions, ix does same but falls back to integers?)
# - a boolean array
# - callable function TODO still need to figure out how this works

print
print '***** selecting with loc *****'
print df.loc[['i', 'iv']]
print df.loc[['i', 'iv'], 'A':'B']
print df.loc[[True, False, False, True, False, False, False, False], [True, True, False, False]]
# NOTE returns a series where the index is now the column names(?)
print df.loc['ii']

print
print '***** selecting with loc example *****'
print df.loc['iii']  # selects row labeled iii
# gets a boolean area where the entries in row 3 are > 0
print df.loc['iii'] > 0.1
# selects all rows, and the columns as per the boolean array above...
# starting to make sense now :)
print df.loc[:, df.loc['iii'] > 0]

# loc and iloc function mostly the same, except for loc at least 1 label must match (or will get a keyerror) and
# for iloc, out of bounds is handled gracefully (may just return an empty data frame instead), unless it's a single integer selector (indexerror)
# TODO make sure you understand Return view or copy before moving on

# print df.loc[:, lambda df: ['A', 'B']]
# AAAAHHHH... callables aren't working because they are new in 0.18.1... I've got 0.18.0 installed right now :)
# without upgrading, should be able to invoke a function that returns the
# boolean array you want instead, right?

test = lambda x: [True, True, False, False]
print df.loc[:, test(None)]
# yup... so could pass in a series/data frame and compute the boolean array

# can enlarge dataframes
# should add a new column 'E' with the value True for all rows where C's
# value is greater than 0
df.loc[:, 'E'] = df.loc[:, 'C'] >= 0
print df  # bingo! getting the hang of this finally :)

# use at/iat to get a specific cell (faster the loc/iloc because they have
# to handle different types of conditions)

# ix tries to behave like loc, but falls back to iloc
# can be tricky... e.g. ix will always treat ints as labels, unless the index is mixed type, then it treats it as positions
# generally, stick to loc, iloc, unless you have mixed index types and
# need to select based on both labels and positions

# so df<selector> is kind of a weird mix of loc/iloc
# can't take 2 selectors, and in some cases selects columns, in others it selects rows
# if it's identifiers (string or number) or a list of identifiers, it's assumed to be column names
# if it's a slice or boolean area, it is assumed to be row positions
# like ix, probably best to stick to loc/iloc for more predictable/intuitive behavior until I get comfortable with it (or find situations where I need it)
# the one exception might be where it is more intuitive to use it (like df[df['A'] > 2])


df2 = pd.DataFrame({'vals': [1, 2, 3, 4], 'ids': ['a', 'b', 'f', 'n'], 'ids2': ['a', 'n', 'c', 'n']})
print df2.isin({'ids': ['a', 'b'], 'ids2': ['a', 'c'], 'vals': [1, 3]}).all()

# ok, that's neat, but could do the same thing with selectors and boolean operators to specify 'where' clauses
# keep in mind as more succinct way of expressing it though (and can use .any() too)

#where() does same thing as selector, but returns a df of the same 'shape' (i.e. rows/columns)
#will have NaN for cells that don't match, and also takes another data frame 'other' to fill in those blanks
#e.g. convert all number columns to negative (if not already)... would need to change this to preserve strings... wonder if I can do that using .dtype? Probably with apply()!
print df.where(df[['C', 'D']] < 0, -df[['C', 'D']]) 

#mask is inverse of where

#query() lets you specify something as a more englishy string
# df.query('a < b and b < c') vs df['a'] < df['b'] & df['b'] < df['c']
# probably a bit slower though...
#you can name your index
df.index.name='Greg'
# to refer to it in a query, or just refer to it as IndexError

# can also drop duplicates

#at this point, I gotta say, I am getting the hang of this, but there would be a huge difference between someone
# who has a feel for it after a nanodegree vs someone who has really mastered it after a few years of experience.
# I think just to be proficient with it, I need to:
#TODO
# - go through the 'Essential Basic Functionality' and 'Group-By' pages
# - understand how operators work on dataframes
# - understand how to use apply and applymap
# - understand views vs copies (~ pass by reference vs value)
#     - seems like loc/iloc returns views where as chaining can be copies or views
#     - can be tricky to tell if you are getting a view or copy, watch for 'setting on copy' errors
# - understand multi-indexing (maybe)
# - do the nanodegree project
#
# From there, it should just be a matter of optimizing proficiency... 'practice makes perfect'


# and 'public'' methods you can call are:
for attribute in dir(df):
    attr = getattr(df, attribute)
    if not attribute.startswith('_') and hasattr(attr, '__call__'):
        pass
        # print attribute
