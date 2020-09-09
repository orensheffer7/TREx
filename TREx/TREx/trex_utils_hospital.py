import pandas as pd
import numpy as np
import collections

import itertools
import math
import random
import warnings
import time
warnings.filterwarnings('ignore')


def random_combination(iterable, r):
    "Random selection from itertools.combinations(iterable, r)"
    pool = tuple(iterable)
    n = len(pool)
    indices = sorted(random.Random(time.time()).sample(range(n), r))
    return tuple(pool[i] for i in indices)


def naive_algo(df, constraints):
    df_c = df.copy()

    if 2 in constraints:
        for i, r in df_c.iterrows():
            if r.City != "NULL" and r.County != "NULL":
                errors = df_c[(df_c.City == r.City) & (df_c.County != r.County) & (df_c.County != "NULL")]
                if errors.shape[0] > 0:
                    c = collections.Counter(df_c[df_c.City == r.City].County)
                    if "NULL" in c:
                        c.pop("NULL")
                    if len(c) > 0:
                        df_c["County"][i] = c.most_common(1)[0][0]
                                   
                        
    if 3 in constraints:
        for i, r in df_c.iterrows():
            if r.Name != "NULL" and r.County != "NULL":
                errors = df_c[(df_c.Name == r.Name) & (df_c.County != r.County) & (df_c.County != "NULL")]
                if errors.shape[0] > 0:
                    c = collections.Counter(df_c[df_c.Name == r.Name].County)
                    if "NULL" in c:
                        c.pop("NULL")
                    if len(c) > 0:
                        df_c["County"][i] = c.most_common(1)[0][0]


    
    return df_c
    
    
    
    
    
   