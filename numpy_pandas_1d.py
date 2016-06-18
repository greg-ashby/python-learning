import numpy as np
import pandas as pd

# ---------- numpy arrays ----------
# all elements must be of the same type
ar1 = np.array([1, 2, 3])
ar2 = np.array([1, 2, 3])

# math
print ar1 + ar2
print ar1 - ar2
print ar1 * ar2
print ar1 / ar2
print ar1 ** ar2
print ar1 + 100 # 'scalar' gets 'broadcast' as an array(3), so this works

# comparison
print ar1 == ar2
print ar1 < ar2
print ar1 != 2 # again, 'scalar' get 'broadcast' as an array(3)

# indexing
print ar1[0]  # element at i
print ar1[1:2]  # list of elements from [x to y)
print ar1[0:3:2]  # list of elements, step 2
print ar1[::]  # defaults of start to end, step 1

# assignment
ar1[0] = 9
print ar1
ar1[0:2] = ar2[1:3]
print ar1
ar1[1:3] = 5
print ar1
# ar1[0:2] = ar2[0:3] <- this would FAIL
# can 'broadcast' from value to array(n), cannot 'broadcast' from array(n)
# to array(m) if m != n (would need to 'align' the shapes first)

print 'boolean arrays'
bar1 = np.array([True, True, False, False])
bar2 = np.array([True, False, True, False])
print bar1 - bar2  # will do same operation as python would do for these data types
print bar1 != bar2
# logical operators
print bar1 & bar2
print bar1 | bar2
print ~bar1
print bar1 ^ bar2


# ---------- panda series ----------
# elements can be different types, but operations might not make sense/work
# difference between array and series is series has an Index
s1 = pd.Series([1, 2, 3, 4], index=['a', 'b', 'c', 'd'])
print s1
s2 = pd.Series([1, 2, 3, 4], index=['a', 'b', 'c', 'e'])

# math
print s1 + 9990 # scalar gets broadcast
print s1 + s2  # d and e become NaN because they are each added with np.NaN
# Two ways to deal with 'missing values'
# 1: use method and fill_value
print s1.add(s2, fill_value=0)
# 2: re-index for missing indexes, and fill in blanks with a default value
full_index = s1.index | s2.index
s1 = s1.reindex(full_index).fillna(5)
s2 = s2.reindex(full_index).fillna(5)
print s1 + s2


# reset examples
s1 = pd.Series([1, 2, 3, 4], index=['a', 'b', 'c', 'd'])
s2 = pd.Series([4, 1, 3, 2], index=['d', 'a', 'c', 'b'])

# comparison
# compares elements in order regardless of index names, returns index on
# left (positional instead of label (see below))
print s1 == s2
print s2 != s1  # ditto

# indexing
print s1['a']  # element for index, can also be an integer if index is integers
print s1.at['a']  # equivalent
print s1[['a', 'b', 'd']]  # series with these indexes
print s1[['a']]  # note: series with 1 element, not just an element
print s1['a':'c']  # note: range is [x, y] as opposed to integer slicing [x, y)
print s2['a':'b']  # note: index order is important... 'c' is included
print s1['a':'b']  # but not help
print s1[1:3]  # in either case, slices are still '::' format
print s1[[True, False, True, False]]  # <-- this is an index array... select
print s2[[True, False, True, False]]

# notice... proof that comparison operators go by order and not index matching
print s1 == s2
print s1[['a', 'b', 'c', 'd']] == s2[['a', 'b', 'c', 'd']]

# loc, iloc, ix indexing
index_names = ['a', 'b', 'd']
index_positions = [0, 1, 3]
print s1.loc[index_names]
print s1.iloc[index_positions]
print s1.ix[index_names]
print s1.ix[index_positions]

print s1.loc['a':'c']
print s1.iloc[0:3]
print s1.ix['a':'c']
print s1.ix[0:3]

index_array = [True, True, False, True]
print s1.loc[index_array]
print s1.iloc[index_array]
print s1.ix[index_array]

# So basically:
# - s[selector] == s.ix[selector]
# - s.loc[selector] <- only works for labels (name, list, slice, index_array)
# - s.iloc[selector] <- only works for positions (name, list, slice, index_array)
# - s.ix <- attempts to do .loc but falls back to .iloc, with exception that it won't fall back if index is ints
# note: in 0.18.1, selectors can be callables, but i'm not at that yet

# assignment
s1[0] = 9
print s1
s1[0:2] = s2[1:3]  # note, positional vs label index! Ah, so math operators are label based, comparison operators are position based!!!
print s1
s1[1:3] = 5
print s1
# s1[0:2] = s2[0:3]# <- this would FAIL... again - can't broadcast to
# different shapes
# note: indexing returns views (vs copies, so you can assign to them)
# operators on the other hand return copies, so you have to do x = x + y, or x += y


# boolean math, comparisons, and logic
print 'boolean arrays'
bs1 = pd.Series([True, True, False, False], index=['a', 'b', 'c', 'd'])
bs2 = pd.Series([True, True, False, False], index=['a', 'c', 'b', 'd'])
print bs1 - bs2  # will do same operation as python would do for these data types
print bs1 != bs2
# logical operators
print bs1 & bs2
print bs1 | bs2
print ~bs1
print bs1 ^ bs2
# note the difference in True|False orders for bs2 vs bar2... this is to
# show whether logical operators are label or positional indexed (appears
# to be label)

print bs1[['a', 'b', 'c', 'd']] ^ bs2[['a', 'b', 'c', 'd']]
print bs1[[0, 1, 2, 3]] ^ bs2[[0, 1, 2, 3]]
#regardless of the index orders, logical operations are done via label-indexing (as is math, only comparisons are positional)


# so for operators: form is x op y, where
# - x is a Series
# - y is a:
#     - Series (of same shape (i.e. length))
#     - Scalar (single value that gets 'broadcast' to that shape)
# - op is a:
#     - math operator (+, -, *, /, **), performed by label-matching
#     - logical operator (&, |, ~, ^), performed by label-matching
#     - comparison operator (==, !=, <, >, <=, >=), performed by positional-matching
# can also use the equivalent function (e.g. s.add(other)) to get more capability (like auto-fill missing values)

#----- APPLY a function to a series -----
print s1
print s1.apply(lambda x: x * 2)

