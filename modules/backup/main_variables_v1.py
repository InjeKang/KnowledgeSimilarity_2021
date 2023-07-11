from modules.similarity import *
from modules.StrategicDiagram_npi import *
from modules.StrategicDiagram_ngi import *
from modules.MultiProcessFunc import *
from modules.AlliancePerformance import *
from modules.GlobalVariables import *
from os import path
import pandas as pd
import os
from functools import partial

def main():
    data = functions_(
        # read/clean data
        read_data = True, read_patent = False, affil_cleaned = False, patent_stock = False,
        # similarity
        tech_sim = False,
        # strategic diagram of firms
        npi_firm = False, ngi_firm = False, firm_revised = False,
        # strategic diagram of IPCs
        npi_ipc = False, ngi_ipc = False, alliance_performance = True)


def functions_(read_data, tech_sim, patent_stock, npi_firm, ngi_firm, firm_revised, npi_ipc, ngi_ipc, alliance_performance):
    raw_data = func_read_data("04.Result_v7(ngi_ipc)_pickle", read_data)
    data1 = func_tech_sim(raw_data, tech_sim)
    data2 = func_patent_stock(data1, patent_stock)
    data3 = func_npi_firm(data2, npi_firm)
    data4 = func_ngi_firm(data3, ngi_firm)
    data5 = func_firm_revised(data4, firm_revised)
    data6 = func_npi_ipc(data5, npi_ipc)
    data7 = func_ngi_ipc(data6, ngi_ipc)
    data8 = func_perf(raw_data, alliance_performance)
    return data8

     

# Measure Similarity
def func_tech_sim(df, tech_sim):
    if tech_sim:
        output = measure_similarity(df)
        output.to_excel("03.Result_v1(20220405).xlsx")
        return output


# Measure Strategic Diagram

## Accumulating Patents Applied duirng the Designated Period
def func_patent_stock(df, patent_stock):
    if patent_stock:
        tech_sim = pd.read_excel("03.Result_v1(20220405).xlsx", engine="openpyxl", sheet_name="Sheet1").drop("Unnamed: 0", axis=1)
        df = accumulate_patent_stock(tech_sim)
        df.to_excel("03.Result_v3(patent_stock).xlsx")
        df.to_pickle("03.Result_v4(patent_stock)_pickle")
        return df

## NPI of firms 
def func_npi_firm(df, npi_firm):
    if npi_firm:
        df = pd.read_pickle("03.Result_v4(patent_stock)_pickle")
        df2 = npiFirm_to_alliance(df)
        df2.to_excel("03.Result_v4(npi).xlsx")
        df2.to_pickle("03.Result_v4(npi)_pickle")
        return df2

## NPI of IPCs
def func_npi_ipc(df, npi_ipc):
    if npi_ipc:
        # df = pd.read_pickle("03.Result_v4(npi)_pickle")
        # df_IPC = npi.IPC_firm(df)
        # df_IPC.to_pickle("03.Result_v4.2(IPC_stock)")
        df_IPC2 = df
        df_IPC2 = pd.read_pickle("03.Result_v4.2(IPC_stock)")
        df3 = npiIPC_to_alliance(df_IPC2)
        df3.to_excel("03.Result_v5(npi_ipc).xlsx")
        df3.to_pickle("03.Result_v5(npi_ipc)_pickle")
        return df3

## NGI of firms
def func_ngi_firm(df, ngi_firm):
    if ngi_firm:
        # df = pd.read_pickle("03.Result_v5(npi_ipc)_pickle")        
        # df_stock = ngi.patent_stock_year(df)
        # df_stock.to_pickle("03.Result_v6(year_added)_pickle")
        df_stock2 = df
        df_stock2 = pd.read_pickle("03.Result_v6(year_added)_pickle")
        df4 = ngiFirm_to_alliance(df_stock2)
        df4.to_pickle("03.Result_v6(ngi_firm)_pickle")
        return df4

## modified thesaurus...because of standard deviation
def func_firm_revised(df, firm_revised):
    if firm_revised:
        df = pd.read_pickle("03.Result_v6(year_added)_pickle")
        df = df.drop(columns = ["npi_focal", "npi_partner"]) # because previous data has old results on NPIs of firms (but no results on NGIs)
        df = lookup.change_from_alliance(df)
        df2 = npiFirm_to_alliance(df)
        # df2 = multi.multiprocess(df, npi.npiFirm_to_alliance, "focal")
        # df3 = multi.multiprocess(df2, npi.npiFirm_to_alliance, "partner")
        # test = df2[["no", "npi_focal", "npi_partner"]]
        df2.to_excel("99.test.xlsx")
        df2.to_pickle("99.test_pickle")
        df3 = ngiFirm_to_alliance(df2)        
        df3.to_pickle("03.Result_v6.2(thesaurus_applied)_pickle")
        return df3

## NGI of IPCs
def func_ngi_ipc(df, ngi_ipc):
    if ngi_ipc:
        df = pd.read_pickle("03.Result_v6.2(thesaurus_applied)_pickle")
        df2 = multi_process(df, ngiIPC_to_alliance, "df")
        df3 = df2[["no", "focal", "partner", "year", "concurent", "similarity",
        "npi_ipc_focal", "npi_ipc_partner", "ngi_ipc_focal", "ngi_ipc_partner",
        "npi_focal", "npi_partner", "ngi_focal", "ngi_partner"]]        
        df3.to_pickle("04.Result_v7(ngi_ipc)_pickle")
        df3.to_excel("04.Result_v7(ngi_ipc).xlsx")
        return df3

def func_perf(df, alliance_performance):
    if alliance_performance:
        data = df
        data2 = performance_stock(data)
        # data2 = multi_process(data, performance_stock, "df") #keyerror: year
        data2.to_excel("04.Result_v8(performance).xlsx")
        return data2

if __name__ == "__main__":
    result = main()
    