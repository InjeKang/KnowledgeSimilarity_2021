import os, time, re, glob
import numpy as np
import pandas as pd
from tqdm import trange, tqdm
from random import randint
from urllib import request
from bs4 import BeautifulSoup
from multiprocessing import Pool, cpu_count

PAUSE = 1
MAX_PAUSE = 10

def multi_process(df, target_func, type_): # type_ = df // list
    n_cores = cpu_count()-2
    # n_cores = 10
    if type_ ==  "df":        
        df_split = np.array_split(df, n_cores)
        pool = Pool(n_cores)
        df = pd.concat(pool.map(target_func, df_split))
    # elif type_ == "df2list":
    #     list_ = []
    #     df_split = np.array_split(df, n_cores)
    #     pool = Pool(n_cores)
    #     target_func2 = partial(target_func, "perf")
    #     df = list_.append(pool.map(target_func2, df_split))
    else: #  type_ == "list"
        list_ = []        
        list_split = np.array_split(df, n_cores)
        pool = Pool(n_cores)
        df = list_.append(pool.map(target_func, list_split))
    # elif type_ == "multiple_arg": # https://stackoverflow.com/questions/25553919/passing-multiple-parameters-to-pool-map-function-in-python
    #     df_split = np.array_split(df, n_cores)
    #     pool = Pool(n_cores)
    #     # target_func_ = partial(target_func, multi_)
    #     df = pd.concat(pool.map(target_func, df_split))
    """
    pool.apply: the function call is performed in a seperate process / blocks until the function is completed / lack of reducing time
    pool.apply_async: returns immediately instead of waiting for the result / the orders are not the same as the order of the calls
    pool.map: list of jobs in one time (concurrence) / block / ordered-results
    pool.map_async: 
    http://blog.shenwei.me/python-multiprocessing-pool-difference-between-map-apply-map_async-apply_async/
    """
    pool.close()
    pool.join()
    return df