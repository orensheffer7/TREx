import pandas as pd
import numpy as np
import collections

import sys
import itertools
import math
import random
import warnings
import time

from collections import Counter
from multiprocessing import Pool
from trex_utils_met import naive_algo, random_combination
warnings.filterwarnings('ignore')


def calc_cell_shap():
    r = np.random.binomial(len(cells),0.5)
    comb = set(random_combination(cells, r))
    comb_bar = set(cells) - comb
    df_c = df.copy()

    for cell in comb:
        df_c[cell[1]][cell[0]] = "NULL"

    df_repair = naive_algo(df_c, constraints_for_alg)
    is_repair_first = (df_repair[col_repair][row_repair] == after_fix)
    
    for cell in comb:
        memo_dict[str(cell)]["without"] = is_repair_first
    for cell in comb_bar:
        memo_dict[str(cell)]["with"] = is_repair_first
    
    if not is_repair_first:
        for cell in comb:
            df_c[cell[1]][cell[0]] = df[cell[1]][cell[0]] 
            df_repair2 = naive_algo(df_c, constraints_for_alg)

            is_repair_second = (df_repair2[col_repair][row_repair] == after_fix)
            memo_dict[str(cell)]["with"] = is_repair_second
            df_c[cell[1]][cell[0]] = "NULL"
    else:
        for cell in comb_bar:
            df_c[cell[1]][cell[0]] = "NULL" 
            df_repair2 = naive_algo(df_c, constraints_for_alg)

            is_repair_second = (df_repair2[col_repair][row_repair] == after_fix)
            memo_dict[str(cell)]["without"] = is_repair_second
            df_c[cell[1]][cell[0]] = df[cell[1]][cell[0]]
            
            
    return Counter({x:int(y['with'])*(1 - int(y['without'])) if ("with" in y.keys() and "without" in y.keys()) else 0 for (x, y) in memo_dict.items()})
        


m = sys.argv[1]
path_to_data = None
if len(sys.argv) == 3:
    path_to_data = sys.argv[2]

    
default_data = [
    ["La Liga", "Madrid", "Real Madrid", "Espana"],
    ["La Liga", "Madrid", "Real Madrid", "Spain"],
    ["La Liga", "Barcelona", "Barcelona F.C.", "Spain"],
    ["Spanish_League", "Madrid", "Athletico Madrid", "Spain"],
    ["La Liga", "Madrid", "Real Madrid", "Spain"],
    ["La Liga", "Madrid", "Real Madrid", "Catalunia"]
]

df = pd.DataFrame(default_data, columns=["League", "City", "Team", "Country"])

cell_repair = (0, "City")
constraints_for_alg = [2, 3]

if not path_to_data:
    df = pd.DataFrame(default_data, columns=["League", "City", "Team", "Country"])
else:
    df = pd.read_csv(path_to_data)


#df = pd.read_csv('./testdata/La_liga.csv')
# constraints_path = './testdata/La_liga_constraints.txt'
df_copy = df.copy()
row_repair, col_repair = cell_repair[0], cell_repair[1]

df_repair = naive_algo(df_copy, constraints_for_alg)
after_fix = df_repair[col_repair][row_repair]

relevant_rows = df_repair[df_repair[col_repair]==df_repair[col_repair][row_repair]]
#relevant_attributes = list(df.columns)
relevant_attributes = ["Reign", "City", "Region"]
cells = list(itertools.product(relevant_rows.index, relevant_attributes))

print("!!!")

cols = relevant_attributes
cells.remove(cell_repair)
cells_copy = cells.copy()


memo_dict = {}
for cell in cells:
    memo_dict[str(cell)] = {}


def multi_shap(x):
    return calc_cell_shap() 


if __name__ == '__main__':
    start = time.time()
    with Pool(3) as pool:
        results = pool.map(multi_shap, range(int(m)))
        print(results)
        a = Counter()
        for res in results:
            a += res
        print(a)
        print("Running time: " + str(time.time() - start))
        print()
        #print({k: v for k, v in sorted(zip(cells,results), key=lambda item: -item[1])[:10]})
        
        
        
        
        
        
        