import MyProcedures

path =r'C:\Users\E100026\Desktop\V1'
Data_file_name = "Data"
Data_sep_caracter = ','


df = MyProcedures.load_data(path = path, file_name = Data_file_name, sep_caracter = Data_sep_caracter, date_index = 0,col_index = 0, show_shape = False)
    
    #1- Get the original Limits by tolerance_perc and Nbdigits 
MyProcedures.get_data_validation_limits(df, path, tolerance_perc = 25, NbDigits=2)
#MyProcedures.get_thresholds(df, path, tolerance = 3, NbDigits=2)

    #2.1- In dfTunedThresholds="DataValidation.csv" , Change the'Tuned_Lower_Limit' &'Tuned_Upper_Limit' as desired 
# dfDataValidationTuned = MyProcedures.load_data(path = path, file_name = "DataValidation", sep_caracter = ',', date_index = 0,col_index = 0, show_shape = False)
# MyProcedures.get_TunedScreenshots(df, dfDataValidationTuned, path, file_name="DataValidation")
# MyProcedures.get_TunedVsInitialScreenshots(df, dfDataValidationTuned, path,file_name= "DataValidation")

    #2.2- In dfThresholdsTuned="DataThresholds.csv" , Change the'Tuned_Lower_Limit' &'Tuned_Upper_Limit' as desired 
#dfThresholdsTuned = MyProcedures.load_data(path = path, file_name = "DataThresholds", sep_caracter = ',', date_index = 0,col_index = 0, show_shape = False)
#MyProcedures.get_TunedScreenshots(df, dfThresholdsTuned, path ,file_name="DataThresholds")
# MyProcedures.get_TunedVsInitialScreenshots(df, dfThresholdsTuned, path,file_name="DataThresholds" )
