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

def affil_country(data):
    affiliation = data["patent_stock_firm"].copy()
    affiliation_splitted = split_column_into_lists(affiliation, ";")
    placeholder_list = create_placeholder_list(affiliation_splitted)
    # create an empty placeholder list
    country_list = copy.deepcopy(placeholder_list)
    # Selecting countries from the column
    for i in range(len(data)):
        for j in range(len(affiliation_splitted[i])):      
            try:
                country_list[i][j] = affiliation_splitted[i][j].split("`")[0]
            except:
                country_list[i][j] = ""
    return country_list
 
def affil_firm(data, type_): # type_ : affil_firm for 'npi' or 'perf'
    data2 = data.copy()
    # data2 = patent_data.copy() # for test
    affiliation = data2[18].copy()
    affiliation = affiliation.str.replace(" ", "")
    affiliation_splitted = split_column_into_lists(affiliation, ";")
    placeholder_list = create_placeholder_list(affiliation_splitted)
    # create an empty placeholder list
    firm_list = copy.deepcopy(placeholder_list)
    # Selecting countries from the column
    stopwords = ["corporate", "corporation", "us", "fr", "company", "corporate", "corp"]
    for i in range(len(data2)):
        for j in range(len(affiliation_splitted[i])):    
            try:
                # [-2:-1] because there are some data that ends with ' '
                # while others ends with 'corp_name'
                firm_list[i][j] = affiliation_splitted[i][j].split("`")[-5:]
                # firm_list[i][j] = affiliation_splitted[i][j].split("``")
                # remove punctuations or unnecessary words
                firm_list[i][j] = " ".join(firm_list[i][j]) # list to string
                firm_list[i][j] = firm_list[i][j].lower()
                firm_list[i][j] = firm_list[i][j].replace("`", " ")
                firm_list[i][j] = re.sub(r'[^\w\s]','',firm_list[i][j])
                firm_list[i][j] = [word for word in firm_list[i][j].split() if word not in stopwords]
                if type_ == "npi":
                    firm_list[i][j] = list(set(firm_list[i][j]))
                else: # type_ == "perf" >> should not remove duplicate data
                    pass
                firm_list[i][j] = lookup.unify_firm_name(firm_list[i][j], 0)
                firm_list[i][j] = ", ".join(firm_list[i][j]) # list to string                                

            except:
                firm_list[i][j] = ""    
    return firm_list

def accumulate_patent_stock(data): # data: alliance data
    """ accumulating patent data applied during t-5 and t-1"""
    # read all patent data into one dataframe
    # excel_files = glob.glob("D:/Analysis/2021_Similarity/data/patent/KISTI*.xlsx")
    data2 = data.copy()
    # excel_files = glob.glob("D:/Analysis/2021_Similarity" + "\*.xlsx") # for pilot test...524 data when using five companies
    excel_files = glob.glob("D:/Analysis/2021_Similarity/data/patent/KISTI" + "\*.xlsx")
    df = pd.concat((read_xlsx_glob(files) for files in excel_files))
    # select patent to make columns for StrategicDiagram
    patent_stock_list_firm = []
    patent_stock_list_ipc = []
    for i in trange(len(data2)):
        # select patent applied during the designated period
        year = int(data2["year"][i])
        patent_data = df[(pd.to_numeric(df[10]) >= year-5) & 
        (pd.to_numeric(df[10]) <= year-1)].reset_index(drop=True, inplace=False) 
        patent_data = patent_data.drop_duplicates(subset = [9]).reset_index(drop=True, inplace=False) 
        # make a list of assignees(18)
        # # cleansing firm data
        patent_data_firm = [affil_firm(patent_data), "npi"]
        patent_stock_list_firm.extend(patent_data_firm)        
        # make a list of ipc(32)
        patent_data_ipc = [patent_data[32].values.tolist()]
        patent_stock_list_ipc.extend(patent_data_ipc)
        print("accumulating patent stock # {}".format(i+1))
    # add the columns >> assigness/ipc of patents applied during the designated period
    data2["patent_stock_firm"] = patent_stock_list_firm
    data2["patent_stock_ipc"] = patent_stock_list_ipc
    return data2

def npi_firm(firm, list_full, type_): # type_ = focal OR partner
    """
    a function to measure NPI of firms
    """
    #1 measuirng NPI of a focal firm
    #2 making a dataframe to match total production for each firm
    #2.1 measuring total production of each firm
    vals = collections.Counter(list_full).values()
    keys = collections.Counter(list_full).keys()
    df = pd.DataFrame({"firm": keys, "tp": vals})

    #3 measuring npi of firms
    df["log_tp"] = df["tp"].map(lambda x: math.log(x)) # map can be used in Series...progress_map/process_map does not work
    tp_mean = df["log_tp"].mean() # https://towardsdatascience.com/dplyr-style-data-manipulation-with-pipes-in-python-380dcb137000
    tp_sd = df["log_tp"].std()
    df["npi"] = df["log_tp"].map(lambda x: (x-tp_mean)/tp_sd)
    #3.1 selecting npi of a focal/partner firm    
    if type_ == "focal":
        focal = firm.lower()
        npi_result = df.loc[(df["firm"].str.contains(focal))].reset_index(drop=True, inplace=False)        
    else:
        partner = firm.lower()
        npi_result = df.loc[(df["firm"].str.contains(partner))].reset_index(drop=True, inplace=False)
    #3.2 check if there is a unique value
    if len(npi_result) == 1:    
        npi_result2 = npi_result.iloc[0]["npi"]
        print("pass") # no meaning of using "i" >> remove when re-run
    else: # checked if they are the same company
        npi_result2 = npi_result
        print("array format") # no meaning of using "i" >> remove when re-run
        print(npi_result)        
        # add the same firm with different names
        if npi_result.empty:
            npi_result2 = ""
        # else:
        #     sum_ = math.log(npi_result["tp"].sum())
        #     npi_result2 = ((sum_ - tp_mean)/tp_sd)
        #     print(sum_)
        #     print(npi_result2)

    return npi_result2

def npiFirm_to_alliance(data):
    """add NPI of firm to alliance data"""
    data2 = data.copy()
    # data2 = patent_stock(data2)
    firm_list = data2["patent_stock_firm"].copy()    
    npi_focal = []
    npi_partner = []    
    for i in trange(len(data2)):   
        if (data2["focal_ipc"].iloc[i] == []) or (data2["partner_ipc"].iloc[i] == []): # if any data is empty...make it empty
            npi_focal.append("")
            npi_partner.append("")
        else:
            firm_list_full = []
            #1 making a full list of firms
            for j in range(len(firm_list.iloc[i])):
                if len(firm_list.iloc[i][j]) == 1:
                    list_to_string = "".join(firm_list.iloc[i][j])
                    firm_list_full.append(list_to_string)
                else:
                    for k in range(len(firm_list.iloc[i][j])):
                        list_to_string = "".join(firm_list.iloc[i][j][k])
                        firm_list_full.append(list_to_string)
            # unify firms' names
            firm_list_full = lookup.unify_firm_name(firm_list_full, 1)
            firm_list_full = lookup.unify_firm_name2(firm_list_full)
        #2 npi of a focal firm
            focal = npi_firm(data2["focal"].iloc[i], firm_list_full, "focal")
            # focal = multi.multiprocess(data2["focal"][i], npi_firm, "focal")
            npi_focal.append(focal)
        #3 npi of a partner firm
            partner = npi_firm(data2["partner"].iloc[i], firm_list_full, "partner")
            npi_partner.append(partner) #add print(i) after this line
            print("measuring NPI # {}".format(i+1))
    #4 make columns        
    data2["npi_focal"] = npi_focal
    data2["npi_partner"] = npi_partner
    return data2

def npi_ipc(ipc_firm, list_full):
    """
    a function to measure NPI of IPC
    """
    #1 making a dataframe to match total production for each IPC
    vals = collections.Counter(list_full).values()
    keys = collections.Counter(list_full).keys()
    df = pd.DataFrame({"ipc": keys, "tp": vals})
    #2 measuring NPI of IPC
    df["log_tp"] = df["tp"].map(lambda x: math.log(x)) # map can be used in Series...progress_map/process_map does not work
    tp_mean = df["log_tp"].mean() # https://towardsdatascience.com/dplyr-style-data-manipulation-with-pipes-in-python-380dcb137000
    tp_sd = df["log_tp"].std()
    df["npi"] = df["log_tp"].map(lambda x: (x-tp_mean)/tp_sd)
    #3 selecting NPIs of non-overlapping IPCs of focal/partner firm    
    npi_result_ = df[df.apply(lambda x: any([y in x["ipc"] for y in ipc_firm]), axis = 1)].reset_index(drop=True, inplace=False)
    #4 average of the selected NPIs
    npi_result = npi_result_["npi"].mean()
    return npi_result



def IPC_firm(data):
    """read IPC for each focal and partner firm"""
    data2 = data.copy()
    # IPCs that do not overlap between a focal and partner firm
    ipc_focal_unique = [] 
    ipc_partner_unique = []
    # IPCs that overlap between a focal and partner firm
    ipc_overlap = []
    for i in trange(len(data2)):
        # loading IPCs of a focal firm
        for focal_name in os.listdir("./patent/KISTI/"):
            if focal_name.lower().startswith(data["focal"][i].lower()): # read a focal firm's patents
                focal_firm=""
                focalFirm = focal_firm + focal_name            
                focalFirm_patent = read_xlsx(focalFirm)   
                year = int(data["year"][i])
                focal_patent = focalFirm_patent[(pd.to_numeric(focalFirm_patent[10]) >= year-5) &
                (pd.to_numeric(focalFirm_patent[10]) <= year-1)].reset_index(drop=True, inplace=False)  # select patents applied in between t-5 ~ t-1
                focal_patent = focal_patent.drop_duplicates(subset = [9]).reset_index(drop=True, inplace=False)
                focal_patent_list = []
                focal_patent_list = list(set(column_to_list(focal_patent[32].map(lambda x: x.replace(" ", "")))))
                # focal_patent_list = list(set(column_to_list(focal_patent[32].map(lambda x: x.replace(" ", "")))))
                
                # loading a partner firm
                for partner_name in os.listdir("./patent/KISTI/"):    
                    if partner_name.lower().startswith(data["partner"][i].lower()): # read a partner firm's patenets
                        partner_firm=""
                        partnerFirm = partner_firm + partner_name            
                        partnerFirm_patent = read_xlsx(partnerFirm)
                        partner_patent = partnerFirm_patent[(pd.to_numeric(partnerFirm_patent[10]) >= year-5) & 
                        (pd.to_numeric(partnerFirm_patent[10]) <= year-1)].reset_index(drop=True, inplace=False)  # select patents applied in between t-5 ~ t-1
                        partner_patent = partner_patent.drop_duplicates(subset = [9]).reset_index(drop=True, inplace=False) 
                        partner_patent_list = []
                        try:
                            partner_patent_list = list(set(column_to_list(partner_patent[32].map(lambda x: x.replace(" ", "")))))
                        except AttributeError:
                            partner_patent_list = []
                        # list of overlapping IPC
                        ipc_overlap_ = focal_patent_list + partner_patent_list
                        ipc_overlap_ = list(set(ipc_overlap_))

                        # list of non-overlapping IPC
                        ipc_focal_unique_ = list(set(focal_patent_list).difference(partner_patent_list))
                        ipc_partner_unique_ = list(set(partner_patent_list).difference(focal_patent_list)) 
                        
                        # list to a row of a column
                        ipc_focal_unique.append(ipc_focal_unique_)
                        ipc_partner_unique.append(ipc_partner_unique_)                        
                        ipc_overlap.append(ipc_overlap_)
        print("ipc stock # {}".format(i+1))
    # list to column
    data2["focal_ipc"] = ipc_focal_unique
    data2["partner_ipc"] = ipc_partner_unique
    data2["both_ipc"] = ipc_overlap
    return data2


def npiIPC_to_alliance(data):
    """add NPI of IPC to alliance data"""
    data2 = data.copy()
    ipc_list = data2["patent_stock_ipc"].copy()
    npi_focal = []
    npi_partner = []
    for i in trange(len(data2)):
        ipc_list_full_ = []
        # making a full list of IPCs       
        for j in range(len(ipc_list[i])):
            try:
                if len(list(ipc_list[i][j].split(";"))) == 1:
                    ipc_list_full_.append(ipc_list[i][j])
                else:
                    for k in range(len(ipc_list[i][j].split(";"))):
                        list_to_string = "".join(ipc_list[i][j].split(";")[k])
                        ipc_list_full_.append(list_to_string)
            except AttributeError:
                ipc_list_full_.append("")                
        ipc_list_full_ = [x for x in ipc_list_full_ if x.strip()] # remove blank string
        ipc_list_full = list((x.replace(" ", "") for x in ipc_list_full_)) # remove whitespace
        #2 npi of of a focal firm's non-overlapping ipc
        focal = npi_ipc(data2["focal_ipc"][i], ipc_list_full)
        npi_focal.append(focal)
        #3 npi of of a partner firm's non-overlapping ipc
        partner = npi_ipc(data2["partner_ipc"][i], ipc_list_full)
        npi_partner.append(partner)
        print("measuring NPI_IPC # {}".format(i+1))
    #4 make columns
    data2["npi_ipc_focal"] = npi_focal
    data2["npi_ipc_partner"] = npi_partner
    return data2