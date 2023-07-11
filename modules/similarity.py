from modules.GlobalVariables import *
import pandas as pd
from os import path
import os
import openpyxl #https://stackoverflow.com/questions/54024504/reading-and-passing-excel-filename-with-pandas
import math


def jaffe_similarity(focal, partner, unique): # ..._patent_list
    """measuring technological similarity"""
    focal_list = focal
    partner_list = partner
    unique_list = unique
    unique_focal = create_placeholder_list(unique_list)
    unique_partner = create_placeholder_list(unique_list)
    #remove whitespace to unify the format
    unique_list = [x.replace(" ", "") for x in unique_list]
    focal_list = [x.replace(" ", "") for x in focal_list]
    partner_list = [x.replace(" ", "") for x in partner_list]
    # fraction of a focal and partner firm   
    for i in range(len(unique_list)):
        unique_focal[i] = 0
        unique_partner[i] = 0
        for j in range(len(focal_list)):
            if unique_list[i] == focal_list[j]:
                unique_focal[i] = unique_focal[i] + 1
        for k in range(len(partner_list)):
            if unique_list[i] == partner_list[k]:
                unique_partner[i] = unique_partner[i] + 1
    # measuring similarity
    if len(focal_list)*len(partner_list) != 0: # in case when a focal or partner firm does not have patents in the designated period
        unique_focal = [i/len(focal_list) for i in unique_focal]
        unique_partner = [i/len(partner_list) for i in unique_partner]
        focalXpartner = [a*b for a,b in zip(unique_focal, unique_partner)]
        unique_focal2 = [i**2 for i in unique_focal]
        unique_partner2 = [i**2 for i in unique_partner]
        Jaffesimilarity = sum(focalXpartner) / (math.sqrt(sum(unique_focal2)) * math.sqrt(sum(unique_partner2)))
    else:
        Jaffesimilarity = ""
    return Jaffesimilarity


def measure_similarity2(focal, partner, year, patent_stock):
    # type(focal, partner, year) = str, str, int
    # list of a focal firm's IPC
    focalPatent = patent_stock.loc[(patent_stock["firm"].str.lower() == focal.lower()) &
                            (pd.to_numeric(patent_stock[10]) >= year-5) & # to select patent applied in between t-1 and t-5
                            (pd.to_numeric(patent_stock[10]) <= year-1)].reset_index(drop=True, inplace=False)
    focalPatentIPC = column_to_list(focalPatent, focalPatent[32])
    # list of a partner firm's IPC
    partnerPatent = patent_stock.loc[(patent_stock["firm"].str.lower() == partner.lower()) &
                            (pd.to_numeric(patent_stock[10]) >= year-5) & # to select patent applied in between t-1 and t-5
                            (pd.to_numeric(patent_stock[10]) <= year-1)].reset_index(drop=True, inplace=False)
    partnerPatentIPC = column_to_list(partnerPatent, partnerPatent[32])
    # making a unique patent list
    unique_patent_list = []
    unique_patent_list = focalPatentIPC + partnerPatentIPC
    unique_patent_list = list(set(unique_patent_list))
    # measuring similarity between a focal and partner firm
    similarity_result = jaffe_similarity(focalPatentIPC, partnerPatentIPC, unique_patent_list)
    return similarity_result

def measure_similarity(patent_data, data):
    data["tech_sim"] = data.apply(lambda x:
        measure_similarity2(x["focal"], x["partner"], x["year"], patent_data), axis = 1)
    return data
    


# def measure_similarity(data):
#     """making a variable of technological similarity"""
#     tech_similarity = []
#     alliance_firm = []
#     for i in range(len(data)):    
#         # loading a focal firm        
#         for focal_name in os.listdir("./patent/KISTI/"):
#             if focal_name.lower().startswith(data["focal"][i].lower()): # read a focal firm's patents
#                 focal_firm=""
#                 focalFirm = focal_firm + focal_name            
#                 focalFirm_patent = read_xlsx(focalFirm)          
#                 year = int(data["year"][i])
#                 focal_patent = focalFirm_patent[(pd.to_numeric(focalFirm_patent[10]) >= year-5) &
#                 (pd.to_numeric(focalFirm_patent[10]) <= year-1)].reset_index(drop=True, inplace=False)  # select patents applied in between t-5 ~ t-1
#                 focal_patent = focal_patent.drop_duplicates(subset = [9]).reset_index(drop=True, inplace=False) 
#                 focal_patent_list = []
#                 focal_patent_list = column_to_list(focalFirm, focal_patent[32])
#                 # loading a partner firm
#                 for partner_name in os.listdir("./patent/KISTI/"):    
#                     if partner_name.lower().startswith(data["partner"][i].lower()): # read a partner firm's patenets
#                         partner_firm=""
#                         partnerFirm = partner_firm + partner_name            
#                         partnerFirm_patent = read_xlsx(partnerFirm)
#                         partner_patent = partnerFirm_patent[(pd.to_numeric(partnerFirm_patent[10]) >= year-5) & 
#                         (pd.to_numeric(partnerFirm_patent[10]) <= year-1)].reset_index(drop=True, inplace=False)  # select patents applied in between t-5 ~ t-1
#                         partner_patent = partner_patent.drop_duplicates(subset = [9]).reset_index(drop=True, inplace=False) 
#                         partner_patent_list = []
#                         partner_patent_list = column_to_list(partnerFirm, partner_patent[32])
#                         # making a unique patent list
#                         unique_patent_list = []
#                         unique_patent_list = focal_patent_list + partner_patent_list
#                         unique_patent_list = list(set(unique_patent_list))
#                         # measuring similarity between a focal and partner firm
#                         similarity_result = jaffe_similarity(focalFirm, partnerFirm, focal_patent_list, partner_patent_list, unique_patent_list)
#                         tech_similarity.append([similarity_result])
#                         # tech_similarity = [x for x in tech_similarity if str(x) != "na"] # remove 'na' >> should not remove because of length
#                         partners = focalFirm + "-" + partnerFirm
#                         alliance_firm.append(partners)                        
#         print("measuring similarity # {}".format(i+1))
#     data["similarity"] = tech_similarity
#     return data