import pandas as pd
import numpy as np
import collections

import sys
import itertools
import math
import random
import warnings
import time
import signal

from multiprocessing import Pool
from trex_utils import naive_algo, random_combination
warnings.filterwarnings('ignore')


def calc_cell_shap(cell_shap, cell_repair, repeats=10, cols=None):
    i_shap, col_shap = cell_shap[0], cell_shap[1]
    i_repair, col_repair = cell_repair[0], cell_repair[1]

    cells = list(itertools.product(df.index, df.columns if cols is None else cols))
    cells.remove((i_repair, col_repair))
    cells.remove((i_shap, col_shap))
    
    shap = 0
    for i in range(repeats):
        df_c = df.copy()
        m = np.random.binomial(len(cells),0.5)
        comb = random_combination(cells, m)

        for cell in comb:
            df_c[cell[1]][cell[0]] = "NULL"

        df_repair = naive_algo(df_c, constraints)
        is_repair_with = df_repair[col_repair][i_repair] == 'Spain'

        df_c[col_shap][i_shap] = "NULL"

        df_repair = naive_algo(df_c, constraints)
        is_repair_without = df_repair[col_repair][i_repair] == 'Spain'

        a = int(is_repair_with) - int(is_repair_without)
        shap += a
    
    
    return shap 



m = int(sys.argv[1])
path_to_data = None
if len(sys.argv) == 3:
    path_to_data = sys.argv[2] 
    
default_data = [
    ["Barcelona F.C.", "Barcelona", "Spain", "La Liga"],
    ["Athletico Madrid", "Madrid", "Spain", "La Liga"],
    ["Real Madrid", "Madrid", "Spain", "La Liga"],
    ["Barcelona F.C.", "Barcelona", "Catalonia", "La Liga"],
    ["Athletico Madrid", "Capitol", "Espana", "La Liga"],
    ["Real Madrid", "Madrid", "Spain", "La Liga"],
]

if not path_to_data:
    df = df = pd.DataFrame(default_data, columns=["Team", "City", "Country", "League"])
else:
    df = pd.read_csv(path_to_data)

constraints = [1, 2, 3]

cols = list(df.columns)
cells = list(itertools.product(df.index, cols))
cell_repair = (4, "Country")
cells.remove(cell_repair)

results = {}


def multi_shap(cell):
    #print(cell)
    return calc_cell_shap(cell, cell_repair, repeats=m, cols=cols) 


if __name__ == '__main__':
    start = time.time()
    with Pool() as pool:
        results = pool.map(multi_shap, cells)
        print()
        print("Running time: " + str(time.time() - start))
        print()
        print({k: v for k, v in sorted(zip(cells,results), key=lambda item: -item[1])[:10]})
        
        
        
        
        
        
        