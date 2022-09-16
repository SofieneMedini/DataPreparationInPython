import matplotlib
import matplotlib.pyplot as plt
from matplotlib.pyplot import text
import matplotlib.transforms as transforms
import pandas as pd
import numpy as np
import pickle as pk
from pandas import Series
#import seaborn as sns
from tkinter import Tk
import re
import os 


#Procedure Convert to float
def parse_float(x):
    try:
        return float(x)
    except ValueError:
        return np.nan 

rdt = '0'
def parseTime(x):
    global rdt
    try:
        rdt = pd.datetime.strptime(x,'%Y-%m-%d %H:%M:%S')
    except Exception as e:
        if type(x) != str:
            rdt = x
    return rdt

# Importing data as a DataFrame
def load_data(path, file_name, sep_caracter, date_index, col_index, show_shape):
    try:
        df = pk.load(open(file_name+".pk",'rb'))
    except Exception as e:
        print("File path: "+path+"\\"+file_name+'.csv')
        df = pd.read_csv(path+"\\"+file_name+'.csv', sep= sep_caracter,low_memory=False, parse_dates=[date_index],index_col=col_index)
       # pk.dump(df, open(file_name+".pk",'wb'))
    df.sort_index()
    if(show_shape):
        print('CSV Loaded Successfully- Shape of Data', df.shape)
        print('Head', df.head())
    
    for column in df[df.columns[~df.columns.isin(['Tag_Friendly_Name','Tag'])]]:
        df[column] = df[column].apply(parse_float)
        

    print("Done parsing columns to type float")
    return df

#Gets data Thresholds limits for every tag - tolerance is expresses the number of sigmas for threshold tolerance
def get_thresholds(df, path, tolerance, NbDigits):
    print("Inside get thresholds")
    save_to_path=path+'/DataThresholds Initial Screenshots'
    if not os.path.exists(save_to_path): os.makedirs(save_to_path)

    dfoutputs = pd.DataFrame(columns = ['Tag','Tag_Friendly_Name', 'Mean', 'STD','Lower_Limit', 'Upper_Limit','Tuned_Lower_Limit', 'Tuned_Upper_Limit']) 
    try:
        for column in df.columns:
            try:
                std = round(np.std(df[column]) ,NbDigits)
                mean = round(np.mean(df[column]), NbDigits) 
                upper_limit =round(mean + tolerance*std, NbDigits)
                lower_limit =round(mean - tolerance*std, NbDigits)
                y = column
                ax = df.plot(None, y, 'line', title  = str(column))
                ax.axhline(y = upper_limit, color = 'r')
                ax.axhline(y = lower_limit, color = 'r')   
                trans = transforms.blended_transform_factory( ax.transAxes, ax.transData)
                text(1,lower_limit, ' '+str(lower_limit) ,transform=trans, color = 'r', bbox=dict(facecolor='none', edgecolor='r', pad=1.0))
                text(1,upper_limit, ' '+str(upper_limit) ,transform=trans, color = 'r', bbox=dict(facecolor='none', edgecolor='r', pad=1.0))
                plt.savefig( save_to_path+'/'+ re.sub('[^A-Za-z0-9]+', '', str(column))+'_TH.png', dpi = 500)
                print("Tag = "+ str(column)+", std = " + str(std) + ", mean = "+str(mean))
                dfoutputs = dfoutputs.append({'Tag':str(column), 'Tag_Friendly_Name':str(column),'Mean':mean, 'STD':std,'Lower_Limit':lower_limit,'Upper_Limit':upper_limit,'Tuned_Lower_Limit':lower_limit,'Tuned_Upper_Limit':upper_limit}, ignore_index= True)
            except Exception as e:
                print("Exception: "+str(e))
        print(dfoutputs.head())
        dfoutputs.to_csv(path+'/Datathresholds.csv', ",")
    except Exception as e:
        print("Exception: "+str(e))

#Gets data validation limits for every tag - tolerance is a scalar expressing percentage of tolerance
def get_data_validation_limits(df, path, tolerance_perc, NbDigits):
    print("get data validation limits")
    dfoutputs = pd.DataFrame(columns = ['Tag','Tag_Friendly_Name','Lower_Limit', 'Upper_Limit','Tuned_Lower_Limit', 'Tuned_Upper_Limit']) 
    save_to_path=path+'/DataValidation Initial Screenshots'
    if not os.path.exists(save_to_path): os.makedirs(save_to_path)
    try:
        for column in df.columns:
            try:
                lower_limit = round(np.min(df[column]) -  (tolerance_perc/100)*(np.max(df[column]) - np.min(df[column])), NbDigits)
                upper_limit = round(np.max(df[column]) +  (tolerance_perc/100)*(np.max(df[column]) - np.min(df[column])), NbDigits)
                y = column
                ax = df.plot(None, y, 'line', title  = str(column))
                ax.axhline(y = upper_limit, color = 'g', label  = upper_limit)
                ax.axhline(y = lower_limit, color = 'g', label  = upper_limit)
                trans = transforms.blended_transform_factory( ax.transAxes, ax.transData)
                text(1,lower_limit, ' '+str(lower_limit) ,transform=trans, color = 'g', bbox=dict(facecolor='none', edgecolor='g', pad=1.0))
                text(1,upper_limit, ' '+str(upper_limit) ,transform=trans, color = 'g', bbox=dict(facecolor='none', edgecolor='g', pad=1.0))
                plt.savefig( save_to_path +'/'+ re.sub('[^A-Za-z0-9]+', '', str(column)) +'_DV.png',  dpi = 500)
                print("Tag = "+ str(column)+", lower_limit = " + str(lower_limit) + ", upper_limit = "+str(upper_limit))
                dfoutputs = dfoutputs.append({'Tag':str(column),'Tag_Friendly_Name':str(column),'Lower_Limit':lower_limit,'Upper_Limit':upper_limit,'Tuned_Lower_Limit':lower_limit,'Tuned_Upper_Limit':upper_limit}, ignore_index= True)
            except Exception as e:
                print("Exception: "+str(e)) 
        print(dfoutputs.head())
        dfoutputs.to_csv(path+'\DataValidation.csv', ",")
    except Exception as e:
        print("Exception: "+str(e))

#Gets data validation limits for every tag - tolerance is a scalar expressing percentage of tolerance
def moving_aggregation(df, column, sample_size, aggregation_type):
    print('inside moving average')
    if(str(aggregation_type) == 'avg'):
        moving_averages = pd.Series(df[column]).rolling(sample_size).mean()
        df[column+'_moavg'] = moving_averages
    elif(str(aggregation_type) == 'std'):
        moving_averages = pd.Series(df[column]).rolling(sample_size).std()
        df[column+'_movstdev'] = moving_averages
    print(moving_averages)
    
    return df


#Change the Tuned_Lower_Limit and the Tuned_Upper_Limit columns - By Emna 8 Jan 2021
def get_TunedScreenshots(df, dfTunedThresholds,path,file_name):
    print("Inside get TunedScreenshots")
    try:
        save_to_path=path+'/'+file_name+' Tuned Screenshots'
        print(save_to_path)
        if not os.path.exists(save_to_path): os.makedirs(save_to_path)
        for column in df.columns:
            try: 
                index=int(df.columns.get_loc(column))
                lower_limit = dfTunedThresholds.Tuned_Lower_Limit[index]
                upper_limit = dfTunedThresholds.Tuned_Upper_Limit[index]
                y = column
                ax = df.plot(None, y, 'line', title  =  str(dfTunedThresholds.Tag_Friendly_Name[index]))
                ax.axhline(y = upper_limit, color = 'g')
                ax.axhline(y = lower_limit, color = 'g')
                trans = transforms.blended_transform_factory( ax.transAxes, ax.transData)
                ax.text(1,upper_limit, ' '+str(upper_limit) ,transform=trans, color = 'g', bbox=dict(facecolor='none', edgecolor='g', pad=1.0))
                ax.text(1,lower_limit, ' '+str(lower_limit) ,transform=trans, color = 'g', bbox=dict(facecolor='none', edgecolor='g', pad=1.0))                           
                plt.savefig( save_to_path +'/'+ re.sub('[^A-Za-z0-9]+', '', str(column)) +'.png',  dpi = 500)
                print("Tag = "+str(column)+", tuned_lower_limit = " + str(dfTunedThresholds.Tuned_Lower_Limit[index]) + ", tuned_upper_limit = "+str(dfTunedThresholds.Tuned_Upper_Limit[index]))            
            except Exception as e:
                print("Exception: "+str(e)) 
      
    except Exception as e:
        print("Exception: "+str(e))


#Check the Tuned_Lower_Limit and the Tuned_Upper_Limit Vs the Initial Ones- By Emna 8 Jan 2021
def get_TunedVsInitialScreenshots(df, dfTunedThresholds,path,file_name):
    print("Inside get Tuned Vs InitialScreenshots")

    save_to_path=path+'/'+file_name+' InitialVsTuned Screenshots'
    if not os.path.exists(save_to_path): os.makedirs(save_to_path)

    try:
        for column in df.columns:
            try: 
                index=int(df.columns.get_loc(column))
                Initial_Lower_Limit = dfTunedThresholds.Lower_Limit[index]
                Initial_Upper_Limit = dfTunedThresholds.Upper_Limit[index]
                Tuned_Lower_Limit = dfTunedThresholds.Tuned_Lower_Limit[index]
                Tuned_Upper_Limit = dfTunedThresholds.Tuned_Upper_Limit[index]
                y = column
                ax = df.plot(None, y, 'line', title  = str(dfTunedThresholds.Tag_Friendly_Name[index]))
                
                ax.axhline(y = Tuned_Lower_Limit, color = 'g')
                ax.axhline(y = Tuned_Upper_Limit, color = 'g')
                trans = transforms.blended_transform_factory( ax.transAxes, ax.transData)
                ax.text(1,Tuned_Lower_Limit, ' '+str(Tuned_Lower_Limit) ,transform=trans, color = 'g', bbox=dict(facecolor='none', edgecolor='g', pad=1.0))
                ax.text(1,Tuned_Upper_Limit, ' '+str(Tuned_Upper_Limit) ,transform=trans, color = 'g', bbox=dict(facecolor='none', edgecolor='g', pad=1.0))
                   
                if Initial_Lower_Limit != Tuned_Lower_Limit :
                   ax.axhline(y = Initial_Lower_Limit, color = 'g',linestyle='--')                
                   ax.text(0 ,Initial_Lower_Limit, ' '+str(Initial_Lower_Limit) ,transform=trans, color = 'g',va='bottom' ) 
                if Initial_Upper_Limit != Tuned_Upper_Limit :
                   ax.axhline(y = Initial_Upper_Limit, color = 'g',linestyle='--')
                   ax.text(0,Initial_Upper_Limit, ' '+str(Initial_Upper_Limit) ,transform=trans, color = 'g',va='bottom')
                plt.savefig( save_to_path +'/'+ re.sub('[^A-Za-z0-9]+', '', str(column)) +'.png',  dpi = 500)
                print("Tag = "+str(column)+", tuned_lower_limit = " + str(dfTunedThresholds.Tuned_Lower_Limit[index]) + ", tuned_upper_limit = "+str(dfTunedThresholds.Tuned_Upper_Limit[index]))
            
            except Exception as e:
                print("Exception: "+str(e)) 
      
    except Exception as e:
        print("Exception: "+str(e))

