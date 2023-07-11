import pandas as pd
import numpy as np
import copy

def create_placeholder_list(list_of_list):
    """Create a placeholder list (a) to prevent error of index out of range and
    (b) to have a word (instead of an alphabet) as a string"""
    if isinstance(list_of_list, list):
        placeholder_list = []
        for i, _ in enumerate(list_of_list):
            placeholder_list_row = []
            for j, _ in enumerate(list_of_list[i]):
                placeholder_list_row.append("")
            placeholder_list.append(placeholder_list_row)
        return placeholder_list
    else:
        placeholder_list = []
        for i, _ in enumerate(list_of_list):
            placeholder_list_row = []
            for j, _ in enumerate(list_of_list.iloc[i]):
                placeholder_list_row.append("")
            placeholder_list.append(placeholder_list_row)
        return placeholder_list


def unify_firm_name(data, type_): #type = 0 if unique list needed, if not 1
    """making dictionary to deal with the name of institutes with different expression"""    
    # make a lookup table
    lookup_table = pd.DataFrame(np.array([
        ["cree", "creecorp"],

        ["ecirruslogic", "cirruslogic"],

        ["sunbeamproducts", "sunbeam"],
        ["sunbeamplastics", "sunbeam"],

        ["polaroidgraphicsimaging", "polaroid"],
        ["polaroid, polaroidcorporationpatentdepartment", "polaroid"],

        ["creativetechnologyapplic", "creativetechnology"],

        ["varianassociates, varian", "varianassociates"],

        ["ramtronint", "ramtroninternational"],
        ["ramtron", "ramtroninternational"],

        ["pmcsierrainertnational", "pmcsierra"],

        ["hewlettpackardyokogawa", "hewlettpackard"],
        ["hewlettpackard, hewlettpackarddevelopment", "hewlettpackard"],
        ["hewlettpackarddevelopment, hewlettpackard", "hewlettpackard"],
        ["hewlettpackarddevelopmemt", "hewlettpackard"],
        ["hewlettpackardcompany", "hewlettpackard"],
        ["hewlettpackardcompanu", "hewlettpackard"],
        ["hewlettpackardlab", "hewlettpackard"],
        ["hewlettpackardcomany", "hewlettpackard"],
        ["hewlettpackardcolegaldept", "hewlettpackard"],

        ["toshibaamericamri", "toshiba"],
        ["kawasakikaishatoshiba", "toshiba"],
        ["toshiba, toshibaheatingappliances", "toshiba"],
        ["toshibalightingtechnology, toshiba", "toshiba"],
        ["toshiba, toshibatungaloy", "toshiba"],
        ["toshiba, toshibacomponents", "toshiba"],
        ["toshiba, tokyoshibauradenki ", "toshiba"],
        ["toshibamonofrax", "toshiba"],
        ["toshiba, kabushikikaishatoshiba", "toshiba"],
        ["toshibamaterialengineeringc", "toshiba"],
        ["toshibacomputereng", "toshiba"],
        ["toshibashilicone", "toshiba"],
        ["toshibaamericainformationsystems", "toshiba"],
        ["kanushikikaishatoshiba", "toshiba"],
        ["tsugarutoshibasoundequipment", "toshiba"],
        ["toshiba, toshibamachine", "toshiba"],
        ["toshiba, toshibasilicone", "toshiba"],
        ["kasuhikikaishatoshiba", "toshiba"],
        ["toshiba, toshibaceramics", "toshiba"],
        ["toshibabattery, toshiba", "toshiba"],
        ["toshibaelectricappliances", "toshiba"],
        ["toshibaelectronicsystems", "toshiba"],
        ["kabushikikasihatoshiba", "toshiba"],
        ["toshiba, toshibakikai", "toshiba"],
        ["toshibaamericainfsyst", "toshiba"],
        ["toshiba, toshibaaudiovideoeng", "toshiba"],
        ["toshiba, tokyoshibauraelectric", "toshiba"],
        ["toshiba, toshibaelectricequip", "toshiba"],
        ["toshibaautomation", "toshiba"],
        ["kabushikikaishatoshiba", "toshiba"],
        ["toshibaceramicscompanylimit", "toshiba"],
        ["toshiba, toshibachem", "toshiba"],
        ["toshiba, toshibaglass", "toshiba"],
        ["kahishikikaishatoshiba", "toshiba"],
        ["tokyoshibauraelectric, toshiba", "toshiba"],
        ["toshibamachine, toshiba", "toshiba"],
        ["toshibaaudiovideoeng, toshiba", "toshiba"],
        ["toshibasilicone, toshiba", "toshiba"],
        ["toshibaceramics, toshiba", "toshiba"],
        ["toshibakikai, toshiba", "toshiba"],
        ["toshibatungaloy, toshiba", "toshiba"],
        ["kabushikikaishatoshiba, toshiba", "toshiba"],
        ["toshibachem, toshiba", "toshiba"],
        ["toshibacomponents, toshiba", "toshiba"],
        ["tokyoshibauradenki, toshiba", "toshiba"],
        ["toshibaelectricequip, toshiba", "toshiba"],
        ["toshibaglass, toshiba", "toshiba"],
        ["toshibaheatingappliances, toshiba", "toshiba"],

        ["microntechnologying", "microntechnology, micron"],
        ["microntechnologyincv", "microntechnology, micron"],
        ["microntechnologyiinc", "microntechnology, micron"],
        ["microntechnologyinst", "microntechnology, micron"],
        ["microntechnologylnc", "microntechnology, micron"],
        ["microntechnologyincl", "microntechnology, micron"],
        
        ["kawatetsuadvantech", "advantech"],

        ["smistmicroelectronics", "stmicroelectronics"],

        ["ptctherpeutics", "ptctherapeutics"],

        ["advancedmicrodevicesincspansion", "advancedmicrodevices"],
        ["amdadvancedmicrodevices", "advancedmicrodevices"],
        ["advancedmicrodevicesamd", "advancedmicrodevices"],
        ["advancedmicrodevicesi", "advancedmicrodevices"],
        ["amdincadvancedmicrodevices", "advancedmicrodevices"],
        ["advancedmicrodevicesincs", "advancedmicrodevices"],
        ["advancedmicrodevicesins", "advancedmicrodevices"],
        ["advancedmicrodevicessinc", "advancedmicrodevices"],
        ["advancedmicrodevicesproducts", "advancedmicrodevices"],
        ["advancedmicrodevicess", "advancedmicrodevices"],
        ["advancedmicrodevicesincamd", "advancedmicrodevices"],
        ["amd", "advancedmicrodevices"],

        ["orange", "orangebusiness"],
        ["orange, orangepersonalcommunicationsservices", "orangebusiness"],


        ["bellatlantic, bellatlanticnetworkservices", "bellatlantic"],

        # ["alcatellucent", "alcatel"], 
        # ["tclalcatelmobilephones", "alcatel"],
        # ["alcatelcommunications", "alcatel"],
        # ["alcateloptronics", "alcatel"],
        # ["alcatelusasourcing", "alcatel"],

        ["motorolafreescalesemiconductor", "freescale, freescalesemiconductor"],

        ["motorolaelectronics", "motorola"],
        ["motorolafreescalesemiconductor", "motorola"],
        ["motorolainc", "motorola"],
        ["motorolaelectronicssdnbhd", "motorola"],
        ["nipponmotorola", "motorola"],
        ["motorolamalaysiasdnbhd", "motorola"],
        ["motorola, motorolamobility", "motorola"],
        ["motorola, motorolasolutions", "motorola"],
        ["motorolalighting", "motorola"],
        ["motorolaenergysystems", "motorola"],
        ["motorolasemiconducteurs", "motorola"],
        ["motorolaimc", "motorola"],
        ["motorolacomputerx", "motorola"],
        ["motorolacomputersystems", "motorola"],
        
        ["nokiatechnologies, nokia", "nokia"],
        ["nokiacoporation ", "nokia"],
        ["nokiacoporation", "nokia"],
        ["nokiasolutionsnetworks, nokia", "nokia"],
        ["nokiatelecommunications, nokia", "nokia"],
        ["nokia, nokiamultimediaterminals", "nokia"],
        ["nokiainternetcommunications, nokia", "nokia"],
        ["nokiadisplayproducts, nokia", "nokia"],
        ["nokiatechnology, nokia", "nokia"],
        ["nokia, nokiahighspeedaccessproducts", "nokia"],
        ["nokianetwlrks", "nokia"],
        ["nokiamovilephones", "nokia"],
        ["nokiatelecommunicationsoyc", "nokia"],
        ["nokia, nokiamultimedianetworkterminals", "nokia"],

        ["ulvac", "ulvactechnologies"],

        ["armgroup", "armcompany"],
        ["arm", "armcompany"],

        ["totalimmersion", "immersion"],
        ["totalimmersionsoftware, totalimmersion", "immersion"],

        ["turbodynesystems", "turbodynesys"],

        ["oracleamericaincformerlyknownassunmicrosystems", "oracle"],
        ["oracleinternationalcoproration", "oracle"],
        ["oracleotcsubsidiary", "oracle"],
        ["oracle, oracleinternational", "oracle"],
        ["oracletaleo", "oracle"],
        ["oracleamerca", "oracle"],
        ["oracleamerican", "oracle"],
        ["oracleinernational", "oracle"],
        ["oraclecable, oracle", "oracle"],
        ["oraclefinancialservicessoftware", "oracle"],

        ["intelcorporatino", "intelcorp"],
        ["intelcorporatiton", "intelcorp"],
        ["intelcorporaiton", "intelcorp"],
        ["intelcorporatoin", "intelcorp"],
        ["intelcorportation", "intelcorp"],
        ["intelcorporaqtion", "intelcorp"],

        ["genus", "genustechnologies"],

        ["adobesystemsincorporation", "adobesystems, adobe"],
        ["adobesystemsincorportaed", "adobesystems, adobe"],
        ["adobe, adobesystems", "adobesystems, adobe"],

        ["squareenixalsotradingassquareenix", "squareenix"],
        ["squareenixholdings", "squareenix"],

        ["qualcomm, qualcommmemstechnologies", "qualcomm"],
        ["qualcomm, qualcommtechnologies", "qualcomm"],
        ["qualcomm, qualcomminnovationcenter", "qualcomm"],
        ["qualcommconnectedexperiences, qualcomm", "qualcomm"],
        ["qualcomm, qualcommatheros", "qualcomm"],
        ["qualcomm, qualcommiskoot", "qualcomm"],

        ["texasinstrumentsincoporated", "texasinstruments"],
        ["texasinstrumentsincorporation", "texasinstruments"],
        ["texasinstrumentsincorpated", "texasinstruments"],
        ["texasinstrumentstucson", "texasinstruments"],
        ["texasinstrumentsdeutschlqand", "texasinstruments"],
        ["texasinstrumentscopenhagenaps", "texasinstruments"],
        ["texasinstrumentsincoprorated", "texasinstruments"],
        ["texasinstrumentsdeutchsland", "texasinstruments"],

        ["ageresystemsguardian", "ageresystems"],
        ["ageresystemsoptoelectronicsguardian", "ageresystems"],
        [" ageresystemsguartian", "ageresystems"],
        ["ageresystemsgaurdian", "ageresystems"],
        ["ageresystemsoptoelectronics", "ageresystems"],
        ["ageresystemsguradian", "ageresystems"],
        ["ageresystemsguardin", "ageresystems"],
        ["ageresystemscuardian", "ageresystems"],
        ["ageresystemsguartian", "ageresystems"],
        
        ["neophotonicssemiconductorgodokaisha", "neophotonics"],

        ["crytekipholding", "crytek"],

        ["crytekipholding", "delphi, delphitechnologies"],
        ["delphitechnologiesholdingsarl", "delphi, delphitechnologies"],
        ["delphitechnologiesholdingssarl", "delphi, delphitechnologies"],
        ["delphitechnologiesholdingsnrl", "delphi, delphitechnologies"],
        ["delphidelcoelect", "delphi, delphitechnologies"],
        ["delphitechnolopgies", "delphi, delphitechnologies"],
        ["delphi", "delphi, delphitechnologies"],

        ["microsoft, microsofttechnologylicensing", "microsoft"],
        ["microsoftorthopedicsholdings", "microsoft"],
        ["microsofttechnology", "microsoft"],
        ["microsofttechnologylicensing, microsoft", "microsoft"],
        ["microsoftlicensingtechnology", "microsoft"],
        ["mircosoft, microsoft", "microsoft"],
        ["microsoftholdingsinternational", "microsoft"],

        ["kobelcokobesteel", "kobesteel"],

        ["tesseratechnologies, tessera", "tessera"],
        ["tesseramemstechnologies, tessera", "tessera"],

        ["philips, philipselectronics", "philips"],
        ["koninklijkephilipselectronics, philips", "philips"],
        ["philipssemiconductorgratkorn", "philips"],
        ["philipssemiconductor, philips", "philips"],
        ["koninklijkephilips, philips", "philips"],
        ["nederlandsephilipsbedrijven", "philips"],
        ["attphilipstelecommunications", "philips"],
        ["philips, philipsgloeilampenfabrieken", "philips"],
        ["philips, northamericanphilipsconsumerelectronics", "philips"],
        ["philipsindcomponents", "philips"],
        ["philipsindustrialcomponents", "philips"],
        ["philipssemiconductorsofnorthamerica", "philips"],
        ["philipslumiledslighting, philips", "philips"],

        ["eastmankodakcompany, kodak", "kodak"],
        ["eastmankodakcompamn", "kodak"],
        ["kodakpolychromegraphic", "kodak"],
        ["kodakpolychromegraphics", "kodak"],
        ["eastmankodak, kodak", "kodak"],
        ["eastmankodakcomany", "kodak"],
        ["kodakpolcyhromegraphics", "kodak"],
        ["kodakpolychromegraphicsll", "kodak"],

        ["nokiamultimediaterminals, nokia", "nokia"],
        ["nokia, nokiamobilephones", "nokia"],
        ["nokia, nokianetworks", "nokia"],
        ["nokiacommunications", "nokia"],
        ["nokia, nokiatechnologies", "nokia"],
        ["nokia, nokiadisplayproducts", "nokia"],
        ["nokia, nokiainternetcommunications", "nokia"],
        ["nokia, nokianetwork", "nokia"],
        ["nokia, nokiatechnology", "nokia"],
        ["nokiasiemens, nokiasiemensnetworks", "nokia"],
        ["nokiaip", "nokia"],
        ["nokianetworksov", "nokia"],
        ["nokia, nokiaintelligentedgerouters", "nokia"],
        ["nokia, nokiawirelessrouters", "nokia"],
        ["nokiatelecommunicationsojy", "nokia"],
        ["nokiasiemensnetworks", "nokia"],
        ["nokiacorportation", "nokia"],
        ["nokiatelecommunicationsoyj", "nokia"],
        ["nokiamobile", "nokia"],
        ["nokia, nokiatelecommunications", "nokia"],
        ["nokiasolutionsnetworks, nokiatelecommunications", "nokia"],

        ["corningcablessystems", "uscorning"],
        ["corninglasertron", "uscorning"],
        ["corningcaldesystems", "uscorning"],
        ["corningprecisionlens", "uscorning"],
        ["corningincorporation", "uscorning"],
        ["corningincorporatedc", "uscorning"],
        ["corningcablesystemstechnology", "uscorning"],
        ["corningoti", "uscorning"],
        ["corningintellisense", "uscorning"],
        ["corningappliedtechnologies", "uscorning"],
        ["corninggilbert", "uscorning"],
        ["corningcablesystems, uscorning", "uscorning"],

        ["doncorning", "dowcorning"],
        ["corningoil", "dowcorning"],
        ["dowcorningenterprises", "dowcorning"],
        ["dowcorning, dow", "dowcorning"],
        ["dowcorningcorporationlowell", "dowcorning"],
        ["dowcorning, dowcorningasia", "dowcorning"],
        ["dow3corning", "dowcorning"],
        ["dowcorning, dowcorningtoraysilicone", "dowcorning"],
        ["dowcorningtoraysilicones", "dowcorning"],

        ["mitsuitoatsuchemicals", "mitsuichemicals"],

        ["nvidiausinvestment", "nvidia"],
        ["nvidiausinvestments", "nvidia"],
        ["nvidiacorporaton", "nvidia"],

        ["celesticainternational", "celestica"],

        ["yamaha, yamahahatsudoki", "yamaha"],
        ["yamaha, yamahamotor", "yamaha"],
        ["yamahahadsudokikabushikikai", "yamaha"],

        # ["fujitsu electronics", "fujitsu"],
        # ["fujitsuyamanashielectronic", "fujitsu"],
        # ["fujitsumiyagielectron", "fujitsu"],
        # ["fujitsuvlsi", "fujitsu"],
        # ["fujitsupersonalsystems", "fujitsu"],
        # ["fujitsuvisi", "fujitsu"],
        # ["fujitsutohokuelectronics", "fujitsu"],
        # ["fujitsumicrocomputersystems", "fujitsu"],
        # ["fujitsudevices", "fujitsu"],
        # ["fujitsudenso", "fujitsu"],
        # ["fujitsumicromputersystemsli", "fujitsu"],
        # ["fujitsuautomation", "fujitsu"],
        # ["fujitsuten", "fujitsu"],
        # ["fujitsuisotec", "fujitsu"],
        # ["fujitsukasei", "fujitsu"],
        # ["fujitsuadvancedengineering", "fujitsu"],
        # ["fujitsusocialsciencelaboratory", "fujitsu"],
        # ["fujitsucomponent, fujitsu", "fujitsu"],
        # ["fujitsufrontech, fujitsu", "fujitsu"],
        # ["fujitsutoshibamobilecommunications", "fujitsu"],
        # ["fujitsuopticalcomponents", "fujitsu"],
        # ["fujitsugeneral, fujitsu", "fujitsu"],
        # ["fujitsusemiconductor, fujitsu", "fujitsu"],
        # ["nantongfujitsumicroelectronics", "fujitsu"],
        # ["fujitsunetworkcommunications, fujitsu", "fujitsu"],
        # ["fujitsulimitedfujitsusemiconductor", "fujitsu"],
        # ["miefujitsusemiconductor", "fujitsu"],
        # ["fujitsubroadsolutionconsulting", "fujitsu"],
        # ["fujitsumobilecommunications, fujitsu", "fujitsu"],
        # ["fujitsufsas", "fujitsu"],
        # ["fujitsuconnectedtechnologies", "fujitsu"],
        # ["fujitsutechnologysolutionsintellectualproperty", "fujitsu"],
        # ["fujitsutelecomnetworks, fujitsu", "fujitsu"],
        # ["fujitsusemiconductor", "fujitsu"],
        # ["fujitsutechnologysolutionsintellectualproperty", "fujitsu"],
        # ["fujitsuamdsemiconductor", "fujitsu"],
        # ["fujitsuhitachiplasmadisplay", "fujitsu"],
        # ["fujitsutakamisawacomponent", "fujitsu"],
        # ["fujitsusiemenscomputers", "fujitsu"],
        # ["fujitsu, fujitsuquantumdevices", "fujitsu"],
        # ["fujitsu, fujitsumediadevices", "fujitsu"],
        # ["fujitsu, fujitsudisplaytechnologies", "fujitsu"],
        # ["naganofujitsucomponent ", "fujitsu"],
        # ["fujitsuservices", "fujitsu"],
        # ["fujitsu, fujitsucomponent ", "fujitsu"],
        # ["fujitsu, fujitsugeneral", "fujitsu"],
        # ["fujitsu, fujitsunetworkcommunications", "fujitsu"],
        # ["fujitsusiemanscomputers", "fujitsu"],
        # ["fujitsunaganosystemsengineering", "fujitsu"],
        # ["fujitsu, fujitsumicroelectronics", "fujitsu"],
        # ["fujitsunetworkscommunications", "fujitsu"],
        # ["kyushufujitsuelectronics", "fujitsu"],
        # ["fujitsuperipherals, fujitsu", "fujitsu"],
        # ["fujitsutowaelectron", "fujitsu"],
        # ["fujitsulimilted ", "fujitsu"],
        # ["fujitsu, fujitsusemiconductor ", "fujitsu"],
        # ["fujitsufip", "fujitsu"],
        # ["fujitsu, fujitsucomponent", "fujitsu"],
        # ["fujitsu, fujitsufrontech", "fujitsu"],
        # ["fujitsusiemenscomputers", "fujitsu"],
        # ["fujitsuhitachiplasmadisplay", "fujitsu"],
        # ["fujitsu, fujitsugeneral", "fujitsu"],
        # ["fujitsu, fujitsuquantumdevices", "fujitsu"],
        # ["fujitsu, fujitsumediadevices", "fujitsu"],
        # ["fujitsu, fujitsudisplaytechnologies", "fujitsu"],
        # ["fujitsu, fujitsumobilecommunications", "fujitsu"],
        # ["fujitsu, fujitsusemiconductor", "fujitsu"],
        # ["fujitsu, fujitsumicroelectronics", "fujitsu"],
        # ["fujitsuamdsemiconductor", "fujitsu"],
        # ["naganofujitsucomponent", "fujitsu"],
        # ["fujitsuamdsemiconductorlimitedfasl", "fujitsu"],
        # ["fujitsuamdsemiconductorlimi", "fujitsu"],
        # ["fujitsukiden", "fujitsu"],
        # ["fujitsupersonalcomputersyst", "fujitsu"],
        # ["fujitsulimilted", "fujitsu"],
        # ["fujitsunet", "fujitsu"],
        # ["fujitsutakamizawacomponentl", "fujitsu"],
        # ["fujitsulimitedfujitsuis", "fujitsu"],
        # ["fujitsulimitedfujitsuvlsi", "fujitsu"],

        ["dspacedigitalsignalprocessingcontrolengineering", "dspace"],

        ["echelon", "echeloncorp"],

        ["amdocssoftwaresystems", "amdocs"],

        ["dassaultsystemsofamerica", "dassaultsystems"],

        ["tencenttecnology", "tencenttechnology, tencent"],
        ["tencentbvi", "tencenttechnology, tencent"],

        ["broadcomcorporatin", "broadcom"],
        ["broadcomhomenetworking", "broadcom"],
        ["broadcominnovision", "broadcom"],
        ["broadcomisraelresearch", "broadcom"],
        ["broadcomeireannresearch", "broadcom"],
        ["broadcomcorporaton", "broadcom"],
        ["broadcomsemiconductors", "broadcom"],

        ["macronixinternationalcol", "macronixinternational"],
        ["macronixint", "macronixinternational"],
        ["macronixintl", "macronixinternational"],        
        ["macronixinternationalco", "macronixinternational"],
        ["macronix", "macronixinternational"],

        ["delcoelectronicsoverseas", "delcoelectronics"],

        ["prolinxlabs", "prolinx"],

        ["nvlphotronics", "photronics"],
        ["drsphotronics", "photronics"],
        
        ["auoptronicscorpauo", "auoptronics"],
        ["auoptronicssuzhou, auoptronics", "auoptronics"],
        ["auoptronicsxiamen, auoptronics", "auoptronics"],

        ["airliquidesanteinternational", "airliquide"],
        ["airliquide, lairliquidepourletudelexploitation", "airliquide"],
        ["americanairliquide", "airliquide"],
        ["airliquidelargeindustries", "airliquide"],
        ["airliquideindustrial", "airliquide"],
        ["lairliquide", "airliquide"],
        ["lairliquidepourletudelexploitationdesprocedesgeorgesclaude", "airliquide"],
        ["lairliquideadirectoireconseildesurveillancepourletudelexploitationdesprocedesgeorgesclaude", "airliquide"],
        ["airliquideelectronics", "airliquide"],
        ["airliquidemedicalsystems", "airliquide"],
        ["airliquideelectronicssystems", "airliquide"],
        ["airliquideadvancedtechnologies", "airliquide"],
        ["airliquideprocessconstruction", "airliquide"],
        ["airliquide, lairliquidepourletudelexploitationdesprocedesgeorgesclaude", "airliquide"],
        ["airliquideprocessconstruction", "airliquide"],        

        ["sharp", "sharpcorp"],
        ["sharplaboratoriesofamerica, sharp", "sharpcorp"],
        ["sharpkabuhsikikaisha", "sharpcorp"],
        ["sharprodneywarwick", "sharpcorp"],
        ["sharplinda", "sharpcorp"],
        ["sharpjeffreyj", "sharpcorp"],
        ["sharpkabushikaisha", "sharpcorp"],
        ["sharpdavidr", "sharpcorp"],
        ["sharpcolinc", "sharpcorp"],
        ["sharplaboratoriesofamerican", "sharpcorp"],
        ["sharpallan", "sharpcorp"],
        ["sharpmichellee", "sharpcorp"],
        ["sharpbettylynette", "sharpcorp"],
        ["sharpdavid", "sharpcorp"],
        ["sharprobertl", "sharpcorp"],
        ["sharpjudithj", "sharpcorp"],
        ["sharpscottm", "sharpcorp"],
        ["sharpronniel", "sharpcorp"],
        ["ishiwawajimaharimaheavyindustriessharp", "sharpcorp"],
        ["hudsonsharpmachine", "sharpcorp"],
        ["sharppackagingsystems", "sharpcorp"],
        ["sharplaboratoriesofeurope", "sharpcorp"],
        ["sharpgaryl", "sharpcorp"],
        ["sharpkabsuhikikaisha", "sharpcorp"],

        ["qimondaflash", "qimonda"],
        ["qimondanorthamerican", "qimonda"],

        ["sonyericsson, sonyericssonmobilecommunications", "sonycoporation"],
        ["sonyericssonmobilecommunicatios", "sonycoporation"],
        ["sony", "sonycoporation"],
        ["sony, sonycomputerentertainment", "sonycoporation"],
        ["sonymobilecommunications, sony", "sonycoporation"],
        ["sony, sonyelectronics", "sonycoporation"],
        ["sonypicturesentertainment", "sonycoporation"],
        ["sony, sonychemicalinformationdevice", "sonycoporation"],
        ["sonydadc", "sonycoporation"],
        ["sonyunitedkimgdom", "sonycoporation"],
        ["sony, sonyinternational", "sonycoporation"],
        ["sonydiscdigitalsolutions", "sonycoporation"],
        ["sonycorporationofamerica", "sonycoporation"],
        ["sonyemcsmalaysiasdnbhd", "sonycoporation"],
        ["sonycorporationentertainment", "sonycoporation"],
        ["sonyericcsonmobilecommunications", "sonycoporation"],
        ["sonymanufacturingsystems", "sonycoporation"],
        ["sonyprecisiontechnology", "sonycoporation"],
        ["sony, sonychemical", "sonycoporation"],
        ["sonymusicentertainment", "sonycoporation"],
        ["sonyprecisionengineeringcenter", "sonycoporation"],
        ["sonydisctechnology", "sonycoporation"],

        ["delphiautomotivesystemssungwoo", "delphi, delphitechnologies"],
        ["delphiautomotivesyssungwoo", "delphi, delphitechnologies"],
        ["delphioracle", "delphi, delphitechnologies"],
        ["delphiautomotivesystems", "delphi, delphitechnologies"],
        ["delphi2creativetechnologies", "delphi, delphitechnologies"],
        ["delphitechnology", "delphi, delphitechnologies"],
        ["delphihealthsystems", "delphi, delphitechnologies"],
        ["delphisystemsimulation", "delphi, delphitechnologies"],
        ["delphitechnologiesincx", "delphi, delphitechnologies"],
        ["delphitech", "delphi, delphitechnologies"],
        ["delphicomponents", "delphi, delphitechnologies"],
        ["delphi2creativetech", "delphi, delphitechnologies"],
        ["delphifranceautomotivesys", "delphi, delphitechnologies"],
        ["delphiautomotivesysdeutschl", "delphi, delphitechnologies"],
        ["delphifranceautomotivesystems", "delphi, delphitechnologies"],
        ["delphiautomotivesystemsdeu", "delphi, delphitechnologies"],

        ["boc, bocedwardstechnologies", "boc, bocedwards"],

        ["sunmicrosoft", "microsoft"],

        ["sigmadesignsisraelsdi", "sigmadesigns"],

        ["analogdevicestechnology", "analogdevices"],
        ["analogdevicesimi", "analogdevices"],
        ["analogdevicesglobal", "analogdevices"],

        ["infineontechnologiesasiapacific", "infineon"],
        ["infineontechnologiessc300", "infineon"],
        ["infineontechnologics", "infineon"],
        ["infineontechnologiesna", "infineon"],
        ["infineontechnoplogies", "infineon"],
        ["infineontechnologiesrichmond", "infineon"],
        ["infineontechnologiesdelta", "infineon"],
        ["infineontechologies", "infineon"],
        ["infineontechnologiesflash", "infineon"],
        ["infineontechnologieswirelesssolutions", "infineon"],
        ["infineontechnologiessensonor", "infineon"],
        ["infineontechnologies, infineon", "infineon"],        
        ["infineon, infineontechnologies", "infineon"],
        ["infineontechnologies", "infineon"],
        ["infineontecnologies", "infineon"],        
        ["infineontechnologiesac", "infineon"],
        ["infineontechnologiesofinfineontechnologies", "infineon"],
        ["infineontechnologiesdevelopmentcentertelaviv", "infineon"],
        ["infineontechnologiessc", "infineon"],
        ["infineontechnologoies", "infineon"],
        ["infineontech", "infineon"],
        ["infineontechnologiesaglgr", "infineon"],
        ["infineontechnology", "infineon"],
        ["infineontechnologie", "infineon"],
        ["infineontechnologiesnorthamerican", "infineon"],
        ["infineontechnologiesagigr", "infineon"],
        ["infineontechnologoes", "infineon"],
        ["infineontechnologiesnorht", "infineon"],
        ["infineontechnologiesamericas", "infineon"],
        ["infineontechnologiesbipolar", "infineon"],

        ["okielectricindusrty", "okielectricindustry, oki"],
        ["okielectric, oki", "okielectricindustry, oki"],
        ["okielectriccable, oki", "okielectricindustry, oki"],
        ["oki, okielectriccable", "okielectricindustry, oki"],

        ["ibmcorporation, ibm", "internationalbusinessmachines"],
        ["internationalbusinessmachines, ibm", "internationalbusinessmachines"],
        ["ibm", "internationalbusinessmachines"],
        ["ibm, ibmcorporation", "internationalbusinessmachines"],
        ["ibm, ibminternationalbusinessmachines", "internationalbusinessmachines"],

        ["kyushufujitsuelectronic", "fujitsu electronics"],

        ["texasinstrumentsholland", "texasinstruments"],
        ["texasinstrumentsacer", "texasinstruments"],
        ["texasinstrumentssensorscontrols", "texasinstruments"],
        ["texasinstrumentsisreal", "texasinstruments"],
        ["texasinstrumentsincorproated", "texasinstruments"],
        ["texasinstrumentscork", "texasinstruments"],
        ["texasinstrumentsnorthern", "texasinstruments"],
        ["texasinstrumentsinformation", "texasinstruments"],

        ["sunplustechnologycol", "sunplustechnology"],

        ["kodakpolychromegrpahics", "kodak"],
        ["eastmaskodak", "kodak"],
        ["kodakplychromegraphics", "kodak"],

        ["simtekhardcoatings", "simtek"],

        ["towersemiconductors", "towersemiconductor"],

        ["intersilamericas", "intersil"],

        ["radisyscanadaulc", "radisys"],

        ["ztecorporation, zte", "ztecorp"],

        ["faroudjalaboratories", "faroudja"],
        ["faroudjalab", "faroudja"],
        ["faroudjayvesc", "faroudja"],
        ["faroudjayc", "faroudja"],

        ["sandisk3d, sandisk", "sandisk"],
        ["sandisktechnologies, sandisk", "sandisk"],
        ["sandisksemiconductor, sandisk", "sandisk"],
        ["sandiskenterpriseip, sandisk", "sandisk"],

        ["oraclecable", "oracle"],

        ["atmelgrenoble", "atmel"],
        ["atmelnantes", "atmel"],
        ["atmelresearch", "atmel"],
        ["atmelrousset", "atmel"],
        ["atmelautomotive", "atmel"],

        ["digitalequipmentcorppatent", "digitalequipmentcorp"],
        ["digitalequipmentcorppatlaw", "digitalequipmentcorp"],
        ["digitalequipmentcorpptylim", "digitalequipmentcorp"],

        ["digitalequipmentcorpptylim", "digitalequipmentcorp"],

        ["gemplussca", "gemplus"],
        ["gempluscardinternational, gemplus", "gemplus"],
        ["gempluscardint, gemplus", "gemplus"],
        ["gempluscardinternat", "gemplus"],

        ["ciscotechnologies", "cisco, ciscotechnology"],
        ["ciscosystems", "cisco, ciscotechnology"],
        ["ciscotechology", "cisco, ciscotechnology"],
        ["ciscosystemsinternational", "cisco, ciscotechnology"],
        ["ciscotecnology", "cisco, ciscotechnology"],
        ["cisco, ciscotech", "cisco, ciscotechnology"],        

        ["networkassociatestechnology", "networkassociates"],

        ["qualcommtechnologiesinternational", "qualcomm"],
        ["qualcommswitch", "qualcomm"],

        ["rambusinternational", "rambus"],

        ["facebooktechnologies", "facebook"],

        ["osramoptosemiconductorsgbmh", "optosemiconductor"],
        ["osranooptosemiconductors", "optosemiconductor"],

        ["northropgrummancoporation", "northropgrumman"],
        ["northropgrummancropration", "northropgrumman"],

        ["omron, omronhealthcare", "omron"],
        ["omron, omronautomotiveelectronics", "omron"],
        ["omronscientifictechnologies, omron", "omron"],
        ["omronlaserfront", "omron"],

        ["oberthurtechnologiesofamerica", "oberthurtechnologies"],

        ["tatung", "tatungcompany"],

        ["immersion, immersionmedical", "immersion"],

        ["nextlevelcommunications, lawfirm", "nextlevelcommunications"],

        ["soitecsilicononinsulatortechnologies", "soitec"],

        ["actel", "actelcorporaton"],

        ["thomsoncsf, thomsonmultimedia", "thomsonmultimedia"],
        ["thomsonmultimedialicensing", "thomsonmultimedia"],

        ["atmelresearch", "atmel"],

        ["thomsoncsf, sgsthomsonmicroelectronics", "sgsthomsonmicroelectronics"],
        ["sgsthomsonmicroelectronicssr1", "sgsthomsonmicroelectronics"],
        
        ["nationalsemiconductor", "usnationalsemiconductor"]
        
        ]), columns = ["before", "after"])

    institute = data.copy()    
    institute_matched = [""]*len(institute)
    for i, _ in enumerate(institute): # if for function not used, empty results...don't know why
        for name, institute_ in zip(lookup_table["before"], lookup_table["after"]):
            if _ == name:
                institute_matched[i] = institute_
        if institute_matched[i] == "":             
            institute_matched[i] = "".join(institute[i])
    if type_ == 0:
        institute_matched2 = list(set(institute_matched))
    else:
        institute_matched2 = institute_matched
    return institute_matched2 # in list type

def unify_firm_name2(data):
    """unify firms' names if it contains the names"""
    data2 = data.copy()
    df = pd.DataFrame(data2, columns = ["firm"])
    # change firms' names
    df.loc[df["firm"].str.contains("mitsubishielectric"), "firm"] = "mitsubishielectric"
    df.loc[df["firm"].str.contains("kyocera"), "firm"] = "kyocera"
    df.loc[df["firm"].str.contains("lucenttechnologies"), "firm"] = "lucenttechnologies"
    df.loc[df["firm"].str.contains("mitsui"), "firm"] = "mitsui"
    df.loc[df["firm"].str.contains("hitachi"), "firm"] = "hitachi"
    df.loc[df["firm"].str.contains("asml"), "firm"] = "asml"
    df.loc[df["firm"].str.contains("nanyatechnology"), "firm"] = "nanyatechnology"
    df.loc[df["firm"].str.contains("sony"), "firm"] = "sony"
    df.loc[df["firm"].str.contains("imec"), "firm"] = "imec"
    df.loc[df["firm"].str.contains("toyota"), "firm"] = "toyota"
    df.loc[df["firm"].str.contains("arthurdlittle"), "firm"] = "arthurdlittle"
    df.loc[df["firm"].str.contains("ericsson"), "firm"] = "ericsson"
    df.loc[df["firm"].str.contains("siemens"), "firm"] = "siemens"
    df.loc[df["firm"].str.contains("panasonic"), "firm"] = "panasonic"
    df.loc[df["firm"].str.contains("hyundaimotor"), "firm"] = "hyundaimotor"
    df.loc[df["firm"].str.contains("toshiba"), "firm"] = "toshiba"
    df.loc[df["firm"].str.contains("fujielectric"), "firm"] = "fujielectric"
    df.loc[df["firm"].str.contains("airliquide"), "firm"] = "airliquide"
    df.loc[df["firm"].str.contains("matsushita"), "firm"] = "matsushita"
    df.loc[df["firm"].str.contains("alcatel"), "firm"] = "alcatel"
    df.loc[df["firm"].str.contains("samsungelectronics"), "firm"] = "samsungelectronics"
    df.loc[df["firm"].str.contains("nipponsteel"), "firm"] = "nipponsteel"
    df.loc[df["firm"].str.contains("fujitsu"), "firm"] = "fujitsu"
    df.loc[df["firm"].str.contains("huawei"), "firm"] = "huawei"

    tolist = df["firm"].values.tolist()

    return tolist

def change_from_alliance(data):
    df = data.copy()
    df2 = df[["focal", "partner"]]
    df2["focal"] = df2["focal"].str.lower()
    df2["partner"] = df2["partner"].str.lower()
    df2.loc[(df2["focal"] == "arm" )] = "armcompany"
    df2.loc[(df2["partner"] == "arm")] = "armcompany"
    df2.loc[(df2["focal"] == "corning" )] = "uscorning"
    df2.loc[(df2["partner"] == "corning")] = "uscorning"
    df2.loc[(df2["focal"] == "cree" )] = "creecorp"
    df2.loc[(df2["partner"] == "cree")] = "creecorp"
    df2.loc[(df2["focal"] == "sharp" )] = "sharpcorp"
    df2.loc[(df2["partner"] == "sharp")] = "sharpcorp"
    df2.loc[(df2["focal"] == "nationalsemiconductor" )] = "usnationalsemiconductor"
    df2.loc[(df2["partner"] == "nationalsemiconductor")] = "usnationalsemiconductor"
    df2.loc[(df2["focal"] == "orange" )] = "orangebusiness"
    df2.loc[(df2["partner"] == "orange")] = "orangebusiness"
    df2.loc[(df2["focal"] == "rovi" )] = "rovisolutions"
    df2.loc[(df2["partner"] == "rovi")] = "rovisolutions"
    df2.loc[(df2["focal"] == "zte" )] = "ztecorp"
    df2.loc[(df2["partner"] == "zte")] = "ztecorp"
    df2.loc[(df2["focal"] == "asyst" )] = "asysttechnologies"
    df2.loc[(df2["partner"] == "asyst")] = "asysttechnologies"
    df2.loc[(df2["focal"] == "tatung" )] = "tatungcompany"
    df2.loc[(df2["partner"] == "tatung")] = "tatungcompany"
    df2.loc[(df2["focal"] == "onsemiconductor" )] = "onsemiconductortrading"
    df2.loc[(df2["partner"] == "onsemiconductor")] = "onsemiconductortrading"
    df2.loc[(df2["focal"] == "harman" )] = "harmaninternational"
    df2.loc[(df2["focal"] == "harman" )] = "harmaninternational"
    df2.loc[(df2["focal"] == "echelon" )] = "echeloncorp"
    df2.loc[(df2["partner"] == "echelon")] = "echeloncorp"
    df2.loc[(df2["focal"] == "bts")] = "btsholding"
    df2.loc[(df2["partner"] == "bts")] = "btsholding"
    df2.loc[(df2["focal"] == "ulvac" )] = "ulvactechnologies"
    df2.loc[(df2["partner"] == "ulvac")] = "ulvactechnologies"
    df2.loc[(df2["focal"] == "actel" )] = "actelcorporaton"
    df2.loc[(df2["partner"] == "actel")] = "actelcorporaton"
    df2.loc[(df2["focal"] == "nera")] = "neraconsulting"
    df2.loc[(df2["partner"] == "nera")] = "neraconsulting"
    df["focal"] = df2["focal"]
    df["partner"] = df2["partner"]
    return df


    