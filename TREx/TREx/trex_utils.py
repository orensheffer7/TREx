import collections

import itertools
import math
import random
import time

# How we represent nulls in holoclean.
NULL_REPR = '_nan_'

# A feature value to represent co-occurrence with NULLs, which is not applicable.
NA_COOCCUR_FV = 0


def dictify_df(frame):
    """
    dictify_df converts a frame with columns

      col1    | col2    | .... | coln   | value
      ...
    to a dictionary that maps values valX from colX

    { val1 -> { val2 -> { ... { valn -> value } } } }
    """
    ret = {}
    for row in frame.values:
        cur_level = ret
        for elem in row[:-2]:
            if elem not in cur_level:
                cur_level[elem] = {}
            cur_level = cur_level[elem]
        cur_level[row[-2]] = row[-1]
    return ret


def random_combination(iterable, r):
    "Random selection from itertools.combinations(iterable, r)"
    pool = tuple(iterable)
    n = len(pool)
    indices = sorted(random.Random(time.time()).sample(range(n), r))
    return tuple(pool[i] for i in indices)


def naive_algo(df, constraints):
    df_c = df.copy()
    if 1 in constraints:
        for i, r in df_c.iterrows():
            if r.Team != "NULL" and r.City != "NULL":
                errors = df_c[(df_c.Team == r.Team) & (df_c.City != r.City) & (df_c.City != "NULL")]
                if errors.shape[0] > 0:
                    c = collections.Counter(df_c[df_c.Team == r.Team].City)
                    if "NULL" in c:
                        c.pop("NULL")
                    if len(c) > 0:
                        df_c["City"][i] = c.most_common(1)[0][0] 

    if 2 in constraints:
        for i, r in df_c.iterrows():
            if r.League != "NULL" and r.Country != "NULL":
                errors = df_c[(df_c.League == r.League) & (df_c.Country != r.Country) & (df_c.Country != "NULL")]
                if errors.shape[0] > 0:
                    c = collections.Counter(df_c[df_c.League == r.League].Country)
                    if "NULL" in c:
                        c.pop("NULL")
                    if len(c) > 0:
                        df_c["Country"][i] = c.most_common(1)[0][0]
                                   
                        
    if 3 in constraints:
        for i, r in df_c.iterrows():
            if r.City != "NULL" and r.Country != "NULL":
                errors = df_c[(df_c.City == r.City) & (df_c.Country != r.Country) & (df_c.Country != "NULL")]
                if errors.shape[0] > 0:
                    c = collections.Counter(df_c[df_c.City == r.City].Country)
                    if "NULL" in c:
                        c.pop("NULL")
                    if len(c) > 0:
                        df_c["Country"][i] = c.most_common(1)[0][0]


    
    return df_c