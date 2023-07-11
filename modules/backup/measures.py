from modules import similarity as sim
from modules import StrategicDiagram_npi as npi
from modules.StrategicDiagram_npi import *
from modules import StrategicDiagram_ngi as ngi
from os import path
import pandas as pd
import os




tech_similarity = True
patent_stock = True
npi_firm = True
npi_ipc = True
ngi_firm = True
func_firm_revised = True
ngi_ipc = False


def main():
    # Load data
    input_path = path.join(os.getcwd(), "data")
    os.chdir(input_path)

    # Measure Similarity
    if tech_similarity == False:
        data = pd.read_excel("02.alliance_v3(firms_with_patents_v2).xlsx", engine="openpyxl", sheet_name="alliance")
        tech_sim = sim.measure_similarity(data)
        tech_sim.to_excel("03.Result_v1(20220405).xlsx")

    # Measure Strategic Diagram
    
    ## Accumulating Desginated Patents
    if patent_stock == False:
        tech_sim = pd.read_excel("03.Result_v1(20220405).xlsx", engine="openpyxl", sheet_name="Sheet1").drop("Unnamed: 0", axis=1)
        df = npi.patent_stock(tech_sim)
        df.to_excel("03.Result_v3(patent_stock).xlsx")
        df.to_pickle("03.Result_v4(patent_stock)_pickle")

    ## NPI of firms 
    if npi_firm == False:
        df = pd.read_pickle("03.Result_v4(patent_stock)_pickle")
        df2 = npi.npiFirm_to_alliance(df)
        df2.to_excel("03.Result_v4(npi).xlsx")
        df2.to_pickle("03.Result_v4(npi)_pickle")

    ## NPI of IPCs
    if npi_ipc == False:
        # df = pd.read_pickle("03.Result_v4(npi)_pickle")
        # df_IPC = npi.IPC_firm(df)
        # df_IPC.to_pickle("03.Result_v4.2(IPC_stock)")
        df_IPC2 = pd.read_pickle("03.Result_v4.2(IPC_stock)")
        df3 = npi.npiIPC_to_alliance(df_IPC2)
        df3.to_excel("03.Result_v5(npi_ipc).xlsx")
        df3.to_pickle("03.Result_v5(npi_ipc)_pickle")

    ## NGI of firms
    if ngi_firm == False:
        # df = pd.read_pickle("03.Result_v5(npi_ipc)_pickle")        
        # df_stock = ngi.patent_stock_year(df)
        # df_stock.to_pickle("03.Result_v6(year_added)_pickle")
        df_stock2 = pd.read_pickle("03.Result_v6(year_added)_pickle")
        df4 = ngi.ngiFirm_to_alliance(df_stock2)
        df4.to_pickle("03.Result_v6(ngi_firm)_pickle")

    ## modified thesaurus...because of standard deviation
    if func_firm_revised == False:
        df = pd.read_pickle("03.Result_v6(year_added)_pickle")
        df = df.drop(columns = ["npi_focal", "npi_partner"]) # because previous data has old results on NPIs of firms (but no results on NGIs)
        df = lookup.change_from_alliance(df)
        df2 = npi.npiFirm_to_alliance(df)
        # df2 = multi.multiprocess(df, npi.npiFirm_to_alliance, "focal")
        # df3 = multi.multiprocess(df2, npi.npiFirm_to_alliance, "partner")
        # test = df2[["no", "npi_focal", "npi_partner"]]
        df2.to_excel("99.test.xlsx")
        df2.to_pickle("99.test_pickle")
        df3 = ngi.ngiFirm_to_alliance(df2)        
        df3.to_pickle("03.Result_v6.2(thesaurus_applied)_pickle")
    
    ## NGI of IPCs
    if ngi_ipc == False:
        df = pd.read_pickle("03.Result_v6.2(thesaurus_applied)_pickle")
        
        # df2 = ngi.ngiIPC_to_alliance(df)        
        df2 = ngi.multi_process(df, ngi.ngiIPC_to_alliance, "df")
        
        df3 = df2[["no", "focal", "partner", "year", "concurrent", "similarity",
        "npi_ipc_focal", "npi_ipc_partner", "ngi_ipc_focal", "ngi_ipc_partner",
        "npi_focal", "npi_partner", "ngi_focal", "ngi_partner"]]        
        df3.to_pickle("04.Result_v7(ngi_ipc)_pickle")
        df3.to_excel("04.Result_v7(ngi_ipc).xlsx")

    return df3

if __name__ == "__main__":
    result = main()
    