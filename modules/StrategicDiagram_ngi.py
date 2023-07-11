from cmath import isnan
from posixpath import split
from modules.GlobalVariables import *
import multiprocessing as mp
import pandas as pd
import os
import openpyxl
import glob
from tqdm import trange
import math
from modules import lookup
from multiprocessing import Pool, cpu_count
import numpy as np
import swifter



def patent_stock_year(data): # data: alliance data
    """ accumulating patent data applied during t-5 and t-1"""
    # read all patent data into one dataframe
    # excel_files = glob.glob("D:/Analysis/2021_Similarity/data/patent/KISTI*.xlsx")
    data2 = data.copy()
    # excel_files = glob.glob("D:/Analysis/2021_Similarity" + "\*.xlsx") # for pilot test...524 data when using five companies
    excel_files = glob.glob("D:/Analysis/2021_Similarity/data/patent/KISTI" + "\*.xlsx")
    df = pd.concat((read_xlsx_glob(files) for files in excel_files))
    # select patent to make columns for StrategicDiagram
    patent_stock_list_year = []
    for i in trange(len(data2)):
        # select patent applied during the designated period
        year = int(data2["year"][i])
        patent_data = df[(pd.to_numeric(df[10]) >= year-5) & 
        (pd.to_numeric(df[10]) <= year-1)].reset_index(drop=True, inplace=False)         
        patent_data = patent_data.drop_duplicates(subset = [9]).reset_index(drop=True, inplace=False) 
        # make a list of assigned years
        patent_data_year = [patent_data[10].values.tolist()]
        patent_stock_list_year.extend(patent_data_year)
        print("accumulating patent stock # {}".format(i+1))
    # add the columns >> assigness/ipc of patents applied during the designated period
    data2["patent_stock_year"] = patent_stock_list_year    
    return data2

def ngi_firm(firm, year, patent): 
    """
    a function to measure NGI of firms
    """
    # select all firms' patents that were applied in the last five years
    # same with tech_similarity
    firm_patent = patent[(pd.to_numeric(patent[10]) >= year-5) & 
        (pd.to_numeric(patent[10]) <= year-1)].reset_index(drop=True, inplace=False)
    
    # measure GI of every firms in the list
    firm_patent[10] = pd.to_numeric(firm_patent[10])
    firm_patent_mean = pd.Series(firm_patent.groupby("firm")[10].mean(), name = "mean")
    firm_patent_min = pd.Series(firm_patent.groupby("firm")[10].min(), name = "min")
    firm_patent_max = pd.Series(firm_patent.groupby("firm")[10].max(), name = "max")
    df_gi = pd.concat([firm_patent_mean, firm_patent_min, firm_patent_max], axis = 1)
    
    # firms are in index...chnge to a column
    df_gi = df_gi.rename_axis("firm").reset_index()
    df_gi["gi"] = df_gi.apply(lambda x: ((x["mean"] - x["min"]) / (x["max"] - x["min"]))
    if x["max"] - x["min"] != 0 else 0, axis = 1)

    # measuring NGI of every firms
    gi_mean = df_gi["gi"].mean()
    gi_sd = df_gi["gi"].std()
    df_gi["ngi"] = df_gi["gi"].map(lambda x: (x-gi_mean)/gi_sd)

    # select NGI of a focal/partner firm
    ngi_firm = df_gi.loc[(df_gi["firm"].str.lower() == firm.lower())].reset_index(drop=True, inplace=False)
    if ngi_firm.empty:
        output = np.nan
    else:
        output = ngi_firm["ngi"][0].item()
    return output

  
def ngiFirm_to_alliance(patent_stock, data):
    """add NGI of firm to alliance data"""
    data2 = data.copy()
    data2["ngi_focal"] = data2.apply(lambda x:
                        np.nan if math.isnan(x["tech_sim"]) 
                        else ngi_firm(x["focal"], x["year"], patent_stock), axis = 1)
    data2["ngi_partner"] = data2.apply(lambda x:
                        np.nan if math.isnan(x["tech_sim"]) 
                        else ngi_firm(x["partner"], x["year"], patent_stock), axis = 1)
    return data2



def duplicate_ipc(focal, partner, year, patent):
    # select a focal and partner firms' patents that were applied in the last five years
    focal_patent = patent[(pd.to_numeric(patent[10]) >= year-5) & 
        (pd.to_numeric(patent[10]) <= year-1) &
        (patent["firm"].str.lower() == focal.lower())].reset_index(drop=True, inplace=False)
    partner_patent = patent[(pd.to_numeric(patent[10]) >= year-5) & 
        (pd.to_numeric(patent[10]) <= year-1) &
        (patent["firm"].str.lower() == partner.lower())].reset_index(drop=True, inplace=False)
    # make a list of a focal firm's IPC
    focal_list = flatten_ipc(focal_patent[32].tolist())
    # make a list of a partner firm's IPC
    partner_list = flatten_ipc(partner_patent[32].tolist())
    # make a duplicated IPC
    output = [x for x in focal_list if x in partner_list]
    return output


def ngi_ipc(firm, full_ipc, year, patent):
    """ a function to measure NGI of IPCs"""
    # select a focal/partner firm's unique IPC list
    firm_patent = patent[(pd.to_numeric(patent[10]) >= year-5) & 
            (pd.to_numeric(patent[10]) <= year-1) &
            (patent["firm"].str.lower() == firm.lower())].reset_index(drop=True, inplace=False)
    firm_ipc_list = flatten_ipc(firm_patent[32].tolist())
    firm_ipc_unique = list(set(firm_ipc_list).difference(list(set(full_ipc))))
    
    # select all firms' patents that were applied in the last five years
    # same with tech_similarity
    patent[32] = patent[32].apply(lambda x:
                        np.nan if x is None
                        else (flatten_ipc(list(x.split(";")) 
                        if isinstance(x, str) 
                        else x))) # if x is alrealy well splitted...ex) ["a", "b", "c"]

    patent2 = patent[(pd.to_numeric(patent[10]) >= year-5) & 
        (pd.to_numeric(patent[10]) <= year-1)].reset_index(drop=True, inplace=False)
    # to make a new dataframe that matches IPC and year
    ipc_list = []
    year_list = []
    for i in range(len(patent2)):        
            try:
                for j in range(len(patent2[32][i])):
                    patent[32][i][j] = patent[32][i][j].replace(" ", "")
                    ipc_list.append(patent2[32][i][j])
                    year_list.append(pd.to_numeric(patent[10][i]))
            except: # object of type 'NoneType' has no len()
                ipc_list.append("")
                year_list.append("")
    df2 = pd.DataFrame((zip(ipc_list, year_list)), columns = ["ipc", "year"])
    df2.replace("", np.nan, inplace = True)
    df2.dropna(subset = ["ipc"], inplace = True)

    # measure GI of every IPCs in the list
    df2_mean = pd.Series(df2.groupby("ipc")["year"].mean(), name = "mean")
    df2_min = pd.Series(df2.groupby("ipc")["year"].min(), name = "min")
    df2_max = pd.Series(df2.groupby("ipc")["year"].max(), name = "max")
    df3 = pd.concat([df2_mean, df2_min, df2_max], axis = 1)
    try:
        df3 = df3.drop(labels = "", axis = 0) 
    except: # "[''] not found in axis"
        pass
    df3 = df3.rename_axis("ipc").reset_index()
    df3["gi"] = df3.apply(lambda x: ((x["mean"] - x["min"]) / (x["max"] - x["min"]))
                     if x["max"] - x["min"] != 0 else 0, axis = 1)

    # measure NGI of every IPCs in the list
    gi_mean = df3["gi"].mean()
    gi_sd = df3["gi"].std()
    df3["ngi"] = df3["gi"].map(lambda x: (x-gi_mean)/gi_sd)

    # select NGIs of non-overlapping IPCs 
    ngi_result= df3[df3.apply(lambda x:
                    any([y in x["ipc"] for y in firm_ipc_unique]), axis = 1)].reset_index(drop=True, inplace=False)
    
    # average of the selected IPCs' NGI
    return ngi_result["ngi"].mean()
    # if ngi_result.empty:
    #     output = np.nan
    # else:
    #     output = ngi_result["ngi"].mean()
    # return output


def ngiIPC_to_alliance(patent_stock, data):
    """add NGI of IPC to alliance data"""
    data2 = data.copy()
    # select IPCs that were used by both a focal and partner firm
    data2["duplicate_ipc"] = data2.apply(lambda x:
                            np.nan if math.isnan(x["tech_sim"])
                            else duplicate_ipc(x["focal"], x["partner"], x["year"], patent_stock), axis = 1)
    # # ngi of focal's IPC
    # data2["ngi_IPC_focal"] = data2.apply(lambda x:
    #                         np.nan if math.isnan(x["tech_sim"])
    #                         else ngi_ipc(x["focal"], x["duplicate_ipc"], x["year"], patent_stock), axis = 1)
    # ngi of partner's IPC
    data2["ngi_IPC_partner"] = data2.apply(lambda x:
                            np.nan if math.isnan(x["tech_sim"])
                            else ngi_ipc(x["partner"], x["duplicate_ipc"], x["year"], patent_stock), axis = 1)
    return data2



def ipc_with_year(df_ipc, df_year):
    ipc_list = []    
    year_list = []    
    # for i in range(len(df_ipc)):
    if len(df_ipc) == 0: #in case when there was NoneType above
        ipc_list.append("")
        year_list.append("")
    elif len(df_ipc) == 1:
        # to remove whitespace...use iloc to work in general for any index (i.e. not necessarily to begin from 0)
        # some data not start from 0 since np.array_split is used, which maintain the original index of each split
        ipc_list_ = list(x.replace(" ", "") for x in df_ipc)
        ipc_list.append("".join(ipc_list_))
        year_list.append(int(df_year))        
    else:
        for j in range(len(df_ipc)):
            ipc_list_ = list((x.replace(" ", "") for x in df_ipc)) # to remove whitespace
            ipc_list.append("".join(ipc_list_[j]))
            year_list.append(int(df_year))
    # output = pd.DataFrame((zip(ipc_list, year_list)), columns = ["ipc_list", "year_list"])
    # # remove empty rows
    # output.replace("", np.nan, inplace = True)
    # output.dropna(subset = ["ipc_list"], inplace = True)
    # return output
    return [ipc_list, year_list]