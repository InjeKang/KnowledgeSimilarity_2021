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

def ngi_firm(firm, firm_year, type_): # type_ = focal OR partner
    """
    a function to measure NGI of firms
    """
    df = firm_year
    # linking each firm with patent assigned year
    firm_list = []
    year_list = []
    for i in range(len(df)):
        if len(df["firm"].iloc[i]) == 1:
            firm_list.append("".join(df["firm"].iloc[i]))
            year_list.append(int(df["year"].iloc[i]))
        else:
            for j in range(len(df["firm"].iloc[i])):
                firm_list.append("".join(df["firm"].iloc[i][j]))
                year_list.append(int(df["year"].iloc[i]))
    # unify firms' names
    firm_list2 = lookup.unify_firm_name(firm_list, 1)
    firm_list2 = lookup.unify_firm_name2(firm_list2)
    df2 = pd.DataFrame((zip(firm_list2, year_list)), columns = ["firm", "year"])

    # measuring GI of every firms
    df2_mean = pd.Series(df2.groupby("firm")["year"].mean(), name = "mean")
    df2_min = pd.Series(df2.groupby("firm")["year"].min(), name = "min")
    df2_max = pd.Series(df2.groupby("firm")["year"].max(), name = "max")
    df3 = pd.concat([df2_mean, df2_min, df2_max], axis = 1)
    df3 = df3.drop(labels = "", axis = 0)
    df3["firm"]  = df3.index
    df3["gi"] = df3.apply(lambda x: ((x["mean"] - x["min"]) / (x["max"] - x["min"]))
    if x["max"] - x["min"] != 0 else 0, axis = 1)

    # measuring NGI of every firms
    gi_mean = df3["gi"].mean()
    gi_sd = df3["gi"].std()
    df3["ngi"] = df3["gi"].map(lambda x: (x-gi_mean)/gi_sd)

    # selecting GI of a focal/partner firm
    if type_ == "focal":
        focal = firm.lower()
        ngi_result = df3.loc[(df3["firm"].str.contains(focal))].reset_index(drop=True, inplace=False)
    else:
        partner = firm.lower()
        ngi_result = df3.loc[(df3["firm"].str.contains(partner))].reset_index(drop=True, inplace=False)        

    # check if the result is a unique value and measure NPI
    if len(ngi_result) == 1:
        # measuring NGI of every firms
        ngi_result2 = ngi_result["ngi"][0]
    else:
        ngi_result2 = ngi_result
        print("array format")
        print(ngi_result)
        if ngi_result.empty:
            ngi_result2 = ""
            
    return ngi_result2

  
def ngiFirm_to_alliance(data, patent_stock):
    """add NGI of firm to alliance data"""
    
    
    
    data2 = data.copy()    
    firm_list = data2["patent_stock_firm"].copy()
    year_list = data2["patent_stock_year"].copy()
    ngi_focal = []
    ngi_partner = []
    # ngi_focal, ngi_partner = data2.apply(lambda x:axis)
    
    for i in trange(len(data2)):
        # preliminary work to select patents applied by a focal/partner firm
        df_firm_year = pd.DataFrame((zip(firm_list.iloc[i], year_list.iloc[i])), columns = ["firm", "year"])        
        # ngi of a focal firm
        focal = ngi_firm(data2["focal"].iloc[i], df_firm_year, "focal")
        ngi_focal.append(focal)
        # ngi of a partner firm
        partner = ngi_firm(data2["partner"].iloc[i], df_firm_year, "partner")
        ngi_partner.append(partner)
        print("measuring NGI # {}".format(i+1))

    # make columns
    data2["ngi_focal"] = ngi_focal
    data2["ngi_partner"] = ngi_partner

    return data2

# def ngi_firm2(firm, firm_year, type_): # type_ = focal OR partner
#     """
#     a function to measure NGI of firms
#     """
#     df = firm_year
#     # linking each firm with patent assigned year
#     firm_list = []
#     year_list = []
#     for i in range(len(df)):
#         if len(df["firm"].iloc[i]) == 1:
#             firm_list.append("".join(df["firm"].iloc[i]))
#             year_list.append(int(df["year"].iloc[i]))
#         else:
#             for j in range(len(df["firm"].iloc[i])):
#                 firm_list.append("".join(df["firm"].iloc[i][j]))
#                 year_list.append(int(df["year"].iloc[i]))
#     # unify firms' names
#     firm_list2 = lookup.unify_firm_name(firm_list, 1)
#     firm_list2 = lookup.unify_firm_name2(firm_list2)
#     df2 = pd.DataFrame((zip(firm_list2, year_list)), columns = ["firm", "year"])

#     # measuring GI of every firms
#     df2_mean = pd.Series(df2.groupby("firm")["year"].mean(), name = "mean")
#     df2_min = pd.Series(df2.groupby("firm")["year"].min(), name = "min")
#     df2_max = pd.Series(df2.groupby("firm")["year"].max(), name = "max")
#     df3 = pd.concat([df2_mean, df2_min, df2_max], axis = 1)
#     df3 = df3.drop(labels = "", axis = 0)
#     df3["firm"]  = df3.index
#     df3["gi"] = df3.apply(lambda x: ((x["mean"] - x["min"]) / (x["max"] - x["min"]))
#     if x["max"] - x["min"] != 0 else 0, axis = 1)

#     # measuring NGI of every firms
#     gi_mean = df3["gi"].mean()
#     gi_sd = df3["gi"].std()
#     df3["ngi"] = df3["gi"].map(lambda x: (x-gi_mean)/gi_sd)

#     # selecting GI of a focal/partner firm
#     if type_ == "focal":
#         focal = firm.lower()
#         ngi_result = df3.loc[(df3["firm"].str.contains(focal))].reset_index(drop=True, inplace=False)
#     else:
#         partner = firm.lower()
#         ngi_result = df3.loc[(df3["firm"].str.contains(partner))].reset_index(drop=True, inplace=False)
#     # check if the result is a unique value and measure NPI
#     if len(ngi_result) == 1:
#         # measuring NGI of every firms
#         ngi_result2 = ngi_result["ngi"].iloc[0]
#     elif ngi_result.empty:
#         ngi_result2 = ""
#     else:
#         print("array format")
#         print(ngi_result)
#         ngi_result2 = ngi_result    
#     return ngi_result2
    

# def ngi_firm(focal_ipc_, partner_ipc_, patent_firm_, patent_year_, firm_, type_): # type_ : focal or partner
#     if (focal_ipc_ == []) or (partner_ipc_ == []): # if any data is empty...make it empty
#         ngi = ""
#     else:
#         firm_list = patent_firm_.copy()
#         year_list = patent_year_.copy()
#         df_firm_year = pd.DataFrame((zip(firm_list, year_list)), columns = ["firm", "year"])
#         ngi = ngi_firm2(firm_, df_firm_year, type_)
#     return ngi
 

# def ngiFirm_to_alliance(data):
#     """add NGI of firm to alliance data"""
#     data2 = data.copy()    
#     data2["ngi_focal"] = data.apply(lambda x:
#             ngi_firm(x["focal_ipc"], x["partner_ipc"], x["patent_stock_firm"],x["patent_stock_year"], x["focal"], "focal"), axis = 1)

#     data2["ngi_partner"] = data.apply(lambda x:
#             ngi_firm(x["focal_ipc"], x["partner_ipc"], x["patent_stock_firm"],x["patent_stock_year"], x["partner"], "partner"), axis = 1)
#     return data2

def split_(data, splitter):
    """to split string with the consideration of NoneType Error"""
    try:
        return data.split(splitter)
    except:
        return ""


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


# def ipc_with_year(data):    
#     df_ipc = data[0]
#     df_year = data[1]
#     ipc_list = []    
#     year_list = []
#     if len(df_ipc) == 0: #in case when there was NoneType above
#         ipc_list.append("")
#         year_list.append("")
#     elif len(df_ipc) == 1:
#         # to remove whitespace...use iloc to work in general for any index (i.e. not necessarily to begin from 0)
#         # some data not start from 0 since np.array_split is used, which maintain the original index of each split
#         # ipc_list_ = list(x.replace(" ", "") for x in df_ipc)
#         ipc_list_ = [x.replace(" ","") for x in ipc_list_]
#         ipc_list.append("".join(ipc_list_))
#         year_list.append(int(df_year))        
#     else:
#         for j in range(len(df_ipc)):
#             ipc_list_ = list((x.replace(" ", "") for x in df_ipc)) # to remove whitespace
#             ipc_list.append("".join(ipc_list_[j]))
#             year_list.append(int(df_year))
#     output = pd.DataFrame((zip(ipc_list, year_list)), columns = ["ipc", "year"])
#     #remove empty rows
#     output.replace("", np.nan, inplace = True)
#     output.dropna(subset = ["ipc"], inplace = True)
#     return output


def ngi_ipc(ipc_firm, ipc_year):
    """
    a function to measure NGI of IPCs
    """
    df = ipc_year.copy()    
    df["ipc"] = df["ipc"].apply(lambda x: split_(x, ";"))

    # # linking each ipc with patent assigned year by multiprocessing    
    # df2 = multi_process(df, ipc_with_year, "df")
    
    # linking each ipc with patent assigned year without multiprocessing
    # df2 = df.apply(lambda x: ipc_with_year(x["ipc"], x["year"]), axis =1)
    # df2.head()
    # df2.columns = ["ipc", "year"]
    
    ipc_list = []    
    year_list = []         
    for i in range(len(df)):
        if len(df["ipc"][i]) == 0: #in case when there was NoneType above
            ipc_list.append("")
            year_list.append("")
        elif len(df["ipc"][i]) == 1:
            ipc_list_ = list(x.replace(" ", "") for x in df["ipc"][i]) # to remove whitespace
            ipc_list.append("".join(ipc_list_))
            year_list.append(int(df["year"][i]))        
        else:
            for j in range(len(df["ipc"][i])):
                ipc_list_ = list((x.replace(" ", "") for x in df["ipc"][i])) # to remove whitespace
                ipc_list.append("".join(ipc_list_[j]))
                year_list.append(int(df["year"][i]))
    df2 = pd.DataFrame((zip(ipc_list, year_list)), columns = ["ipc", "year"])
    df2.replace("", np.nan, inplace = True)
    df2.dropna(subset = ["ipc"], inplace = True)
    
    
    # measuring GI of every IPC
    df2_mean = pd.Series(df2.groupby("ipc")["year"].mean(), name = "mean")
    df2_min = pd.Series(df2.groupby("ipc")["year"].min(), name = "min")
    df2_max = pd.Series(df2.groupby("ipc")["year"].max(), name = "max")
    df3 = pd.concat([df2_mean, df2_min, df2_max], axis = 1)
    try:
        df3 = df3.drop(labels = "", axis = 0) 
    except: # "[''] not found in axis"
        pass
    df3["ipc"]  = df3.index
    df3["gi"] = df3.apply(lambda x: ((x["mean"] - x["min"]) / (x["max"] - x["min"]))
    if x["max"] - x["min"] != 0 else 0, axis = 1)

    # measuring NGI of every IPCs
    gi_mean = df3["gi"].mean()
    gi_sd = df3["gi"].std()
    df3["ngi"] = df3["gi"].map(lambda x: (x-gi_mean)/gi_sd)

    # selecing NGIs of non-overlapping IPCs of focal/partner firm
    ngi_result= df3[df3.apply(lambda x: any([y in x["ipc"] for y in ipc_firm]), axis = 1)].reset_index(drop=True, inplace=False)

    # average of the selected NPIs
    ngi_result2 = ngi_result["ngi"].mean()
            
    return ngi_result2

def ngiIPC_to_alliance(data):
    """add NGI of IPC to alliance data"""
    data2 = data.copy()
    ipc_list = data2["patent_stock_ipc"].copy()    
    year_list = data2["patent_stock_year"].copy()
    ngi_focal = []
    ngi_partner = []    
    for i in trange(len(data2)):
    # for i in range(3, 4): # for test
        if (data2["focal_ipc"].iloc[i] == []) or (data2["partner_ipc"].iloc[i] == []): # if any data is empty...make it empty
            ngi_focal.append("")
            ngi_partner.append("")
        else:        
            # preliminary work to select patents applied by a focal/partner firm
            df_ipc_year = pd.DataFrame((zip(ipc_list.iloc[i], year_list.iloc[i])), columns = ["ipc", "year"])        
            # ngi of a focal firm
            focal_ipc_list = list((x.replace(" ", "") for x in data2["focal_ipc"].iloc[i])) # to remove white space
            focal = ngi_ipc(focal_ipc_list, df_ipc_year)
            ngi_focal.append(focal)
            # ngi of a partner firm        
            partner_ipc_list = list((x.replace(" ", "") for x in data2["partner_ipc"].iloc[i]))
            partner = ngi_ipc(partner_ipc_list, df_ipc_year)
            ngi_partner.append(partner)
        print("measuring NGI # {}".format(i+1))

    # make columns
    data2["ngi_ipc_focal"] = ngi_focal
    data2["ngi_ipc_partner"] = ngi_partner

    return data2