import multiprocessing as mp
import pandas as pd
import os
import openpyxl
import glob
from tqdm import trange
from multiprocessing import Pool, cpu_count
import numpy as np
# from modules.StrategicDiagram_ngi import *
from os.path import join
from modules.GlobalVariables import *
from modules.StrategicDiagram_npi import *
from modules.lookup import *


# def alliance_with_patent(alliance_data, patent_data, time_):
#     """
#     retrieving patents (1) assigned by both focal/partner firms (2) after t yeas of alliance
#     """
#     alliance = alliance_data.copy()
#     patent = patent_data.copy()
#     # retrieving patents assigned during the designated period
#     year = int(alliance["year"])
#     patent2 = patent[(pd.to_numeric(patent[10] <= year + time_))].reset_index(drop=True, inplace=False)
#     # retrieving patent assigned by both firms
#     patent3 = patent2[(patent2[18].str.lower().contains(alliance["focal"].lower())) &
#     (patent2[18].str.lower().contains(alliance["partner"].lower()))]
#     # removing duplicated data
#     patent4 = patent3.drop_duplicates(subset = [9]).reset_index(drop=True, inplace=False)
#     # number of performance data
#     output = len(patent4)
#     return output

def alliance_with_patent(focal, partner, year_, patent_data, time_):
    """
    retrieving patents (1) assigned by both focal/partner firms (2) after t yeas of alliance
    """    
    patent2 = patent_data[(pd.to_numeric(patent_data[10]) >= int(year_)+1) &
                        (pd.to_numeric(patent_data[10]) <= int(year_) + time_)].reset_index(drop=True, inplace=False)
    # removing duplicated data
    patent2 = patent2.drop_duplicates(subset = [9]).reset_index(drop=True, inplace=False)
    # retrieving patent assigned by both firms
    patent4 = patent2[(patent2["firm"].str.lower() == focal.lower()) |
    (patent2["firm"].str.lower() == partner.lower())]

    # return number of performance data
    return patent4.duplicated(subset=[9]).sum()


def performance_stock(patent_data, data):
    """
    accumulating patent data applied after the alliance 
    """
    data["performance_t3"] = data.apply(lambda x: alliance_with_patent(
        x["focal"], x["partner"], x["year"], patent_data, time_=4), axis = 1)

    data["performance_t6"] = data.apply(lambda x: alliance_with_patent(
        x["focal"], x["partner"], x["year"], patent_data, time_=6), axis = 1)
    return data


# data = pd.read_pickle("D:/Analysis/2021_Similarity/data/03.Result_v6.2(thesaurus_applied)_pickle")
# # data = pd.read_pickle("D:/Analysis/2021_Similarity/data/03.Result_v6(year_added)_pickle")
# performance = performance_stock(data, 10)
# performance.to_pickle("04.Result_v8(performance)_pickle")