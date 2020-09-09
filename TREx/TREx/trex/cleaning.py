import pandas as pd
import collections
import itertools
import math
import random
import time
import warnings
warnings.filterwarnings('ignore')
import timeit

import sys
sys.path.append('../')
import holoclean
from detect import NullDetector, ViolationDetector
from repair.featurize import *



class HoloCleaner:

    def __init__(self, data_df):
        hc = holoclean.HoloClean(
            db_name='holo',
            domain_thresh_1=0,
            domain_thresh_2=0,
            weak_label_thresh=0.99,
            max_domain=10000,
            cor_strength=0.6,
            nb_cor_strength=0.8,
            epochs=10,
            weight_decay=0.01,
            learning_rate=0.001,
            threads=1,
            batch_size=1,
            verbose=False,
            timeout=1*600,
            feature_norm=False,
            weight_norm=False,
            print_fw=False
        ).session

        hc.load_data('hospital', data_df)
        hc.load_dcs('./temp_constraints.txt')
        hc.ds.set_constraints(hc.get_dcs())

        hc.setup_domain(list(data_df.columns))
        return hc
        
        
        def create_constraints_file(relevant_attr):
            fr = open('./testdata/hospital_constraints.txt')
            fw = open('./temp_constraints.txt', "w+")
            attributes_to_keep = set()
            for line in fr:
                for attr in relevant_attr:
                    if attr in line:
                        fw.write(line)
                        for item in line.split("t2.")[1:]:
                            attributes_to_keep.add(item.split(")")[0])
            fr.close()
            fw.close()
            return attributes_to_keep
            
            
        def holoclean_detect(hc):
            detectors = [NullDetector(), ViolationDetector()]
            featurizers = [
                InitAttrFeaturizer(),
                OccurAttrFeaturizer(),
                FreqFeaturizer(),
                ConstraintFeaturizer(),
            ]
            
            hc.detect_errors(detectors)
            hc.repair_errors(featurizers)

            return hc


        def run_holoclean(df, columns):
            relevant_attributes = create_constraints_file(columns)
            df_in = df.copy()
            df_in = df_in[relevant_attributes]
            hc = holoclean_init(df_in)
            hc = holoclean_detect(hc)
            return hc

        


#class Naive:





    