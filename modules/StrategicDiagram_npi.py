from modules.GlobalVariables import *
from tracemalloc import stop
from os import path
from tqdm import trange
from tqdm import tqdm
from modules import lookup
import pandas as pd
import os
import openpyxl #https://stackoverflow.com/questions/54024504/reading-and-passing-excel-filename-with-pandas
import math
import statistics
import copy
import glob
import re
import collections

def npi_firm(firm, year, patent):
    """
    a function to measure NPI of firms
    """
    # select all firms' patents that were applied in the last five years
    # same with tech_similarity
    firm_patent = patent[(pd.to_numeric(patent[10]) >= year-5) & 
        (pd.to_numeric(patent[10]) <= year-1)].reset_index(drop=True, inplace=False)
    # firm frequency
    firm_list = firm_patent["firm"].tolist()
    vals = collections.Counter(firm_list).values()
    keys = collections.Counter(firm_list).keys()
    df_pi = pd.DataFrame({"firm": keys, "tp": vals})

    #3 measuring npi of firms
    df_pi["log_tp"] = df_pi["tp"].map(lambda x: math.log(x)) # map can be used in Series...progress_map/process_map does not work
    tp_mean = df_pi["log_tp"].mean() # https://towardsdatascience.com/dplyr-style-data-manipulation-with-pipes-in-python-380dcb137000
    tp_sd = df_pi["log_tp"].std()
    df_pi["npi"] = df_pi["log_tp"].map(lambda x: (x-tp_mean)/tp_sd) 
    #3.1 selecting npi of a focal/partner firm
    npi_result = df_pi.loc[(df_pi["firm"].str.lower() == firm.lower())].reset_index(drop=True, inplace=False)
    if npi_result.empty:
        output = np.nan
    else:
        output = npi_result["npi"][0].item()
    return output


def npiFirm_to_alliance(patent_stock, data):
    """add NPI of firm to alliance data"""
    data2 = data.copy()
    data2["npi_focal"] = data2.apply(lambda x:
                        np.nan if math.isnan(x["tech_sim"]) 
                        else npi_firm(x["focal"], x["year"], patent_stock), axis = 1)
    data2["npi_partner"] = data2.apply(lambda x:
                        np.nan if math.isnan(x["tech_sim"]) 
                        else npi_firm(x["partner"], x["year"], patent_stock), axis = 1)
    return data2


def npi_IPC(firm, full_ipc, year, patent):
    """
    a function to measure NPI of IPCs
    """
    # make a list of IPCs
    firm_patent = patent[(pd.to_numeric(patent[10]) >= year-5) & 
            (pd.to_numeric(patent[10]) <= year-1) &
            (patent["firm"].str.lower() == firm.lower())].reset_index(drop=True, inplace=False)
    firm_ipc_list = flatten_ipc(firm_patent[32].tolist())   
    # firm_ipc_unique = list(set(firm_ipc_list).difference(list(set(full_ipc))))
    firm_ipc_unique = [x for x in firm_ipc_list if x not in full_ipc]
    # count frequency of each IPC
    vals = collections.Counter(firm_ipc_list).values()
    keys = collections.Counter(firm_ipc_list).keys()
    df_pi = pd.DataFrame({"ipc": keys, "tp": vals})    
    # measuring npi of IPCs
    df_pi["log_tp"] = df_pi["tp"].map(lambda x: math.log(x)) # map can be used in Series...progress_map/process_map does not work
    tp_mean = df_pi["log_tp"].mean() # https://towardsdatascience.com/dplyr-style-data-manipulation-with-pipes-in-python-380dcb137000
    tp_sd = df_pi["log_tp"].std()
    df_pi["npi"] = df_pi["log_tp"].map(lambda x: (x-tp_mean)/tp_sd) # RuntimeWarning: invalid value encountered in double_scalars
    #3 selecting NPIs of non-overlapping IPCs of focal/partner firm    
    npi_result_ = df_pi[df_pi.apply(lambda x:
            any([y in x["ipc"] for y in firm_ipc_unique]), axis = 1)].reset_index(drop=True, inplace=False)
    #4 average of the selected NPIs
    npi_result = npi_result_["npi"].mean()
    return npi_result


def npiIPC_to_alliance(patent_stock, data):
    """add NPI of IPC to alliance data"""
    data2 = data.copy()
    data2["npi_IPC_focal"] = data2.apply(lambda x:
                            np.nan if math.isnan(x["tech_sim"])
                            else npi_IPC(x["focal"], x["duplicate_ipc"], x["year"], patent_stock), axis = 1)
    data2["npi_IPC_partner"] = data2.apply(lambda x:
                            np.nan if math.isnan(x["tech_sim"])
                            else npi_IPC(x["partner"], x["duplicate_ipc"], x["year"], patent_stock), axis = 1)
    return data2