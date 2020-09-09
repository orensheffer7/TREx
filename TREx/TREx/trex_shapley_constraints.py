import pandas as pd
import numpy as np
import collections

import itertools
import math
import random
import warnings
import time
warnings.filterwarnings('ignore')


results = {}
for i in range(len(constraints) + 1):
    for comb in itertools.combinations(constraints, i):
        df_repair = algo(df, comb)
        results[comb] = df["Country"][0] != df_repair["Country"][0]
print (results)


for i in constraints:
    shapley_value = 0
    for comb in results:
        if i not in comb:
            
            # Find comb_i             
            for comb_i in results:
                if i in comb_i and len(comb_i) == len(comb) + 1:
                    is_match = True
                    for x in comb:
                        if x not in comb_i:
                            is_match = False
                    if is_match:
                        break
            factor = math.factorial(len(comb)) * math.factorial(len(constraints) - len(comb) - 1)
            factor /= math.factorial(len(constraints))
            shapley_value += factor * (results[comb_i] - results[comb])
    print(i, shapley_value)