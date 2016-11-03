from CAL3QHCR_CreateInputFile_function import CreateInputFile

inttext_list = ["2","56"]
intnum_list = [[2],[5,6]]
year_list = [10,11,12,13,14]
scenario_listupper = ['BD','NB']
scenario_listlower = ['bd','nb']
receptor_shp = "C:/Users/thasegawa/Documents/28 Gun Hill Square Air Quality Modeling/02 GIS/02 GIS FIles/Links_Receptors_Project.shp"
traffictable_path = "C:/Users/thasegawa/Documents/28 Gun Hill Square Air Quality Modeling/11 CAL3QHCR PM Dispersion/Input"
traffictable_suffix = "_pm_links.csv"
emissionstable_path = "C:/Users/thasegawa/Documents/28 Gun Hill Square Air Quality Modeling/11 CAL3QHCR PM Dispersion/Input/Road Dust"
emissionstable_suffix = "_pm_results_roaddust.csv"
outputfile_path = "C:/Users/thasegawa/Documents/28 Gun Hill Square Air Quality Modeling/11 CAL3QHCR PM Dispersion/Rev1/newmet"
surfacestation_num = 14732
upperstation_num = 94703

for int_index in range(len(intnum_list)):
    intnum = intnum_list[int_index]
    inttext = inttext_list[int_index]
    traffictable_prefix = "ghs_int" + inttext + "bd_2018"
    emissionstable_prefix = "ghs_int" + inttext + "bd_2018"
    outputfile_prefix = "Int" + inttext + "_"
    for scenario_num in [0,1]:
        scenario_upper = scenario_listupper[scenario_num]
        scenario_lower = scenario_listlower[scenario_num]
        linkvertex_shp = "C:/Users/thasegawa/Documents/28 Gun Hill Square Air Quality Modeling/02 GIS/02 GIS FIles/Links_" + scenario_upper + "_verticesAll2_Project_Width.shp"
        traffictable_prefix = "ghs_int" + inttext + scenario_lower + "_2018"
        emissionstable_prefix = "ghs_int" + inttext + scenario_lower + "_2018"
        
        for year_num in year_list:
            for month_num in [0,1,2,3]:
                CreateInputFile(intnum, scenario_num, month_num, year_num,
                                receptor_shp, linkvertex_shp,
                                traffictable_path, traffictable_prefix, traffictable_suffix,
                                emissionstable_path, emissionstable_prefix, emissionstable_suffix,
                                surfacestation_num, upperstation_num,
                                outputfile_path, outputfile_prefix)

