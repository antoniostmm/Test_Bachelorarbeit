import pandas as pd
import numpy as np
import os

path_file = os.path.dirname(os.path.abspath(__file__))
dir_Daten = path_file + "/Daten/"
print(dir_Daten)
if not os.path.exists(dir_Daten):
    os.makedirs(dir_Daten)

def get_Data(Data_csv):
    df_Data = pd.DataFrame()
    df_Data = pd.read_csv(Data_csv)
    #df_Data = df_Data.drop(columns= [" "," "," "," "," "," "," "," "," "," "," "])
    df_Data_ges = df_Data[["AirTemp","CloudOpacity"]]

    return df_Data_ges
Data_csv = "Forecasting/2007-2020_Historical_Weather_Aachen_5min_Solcast.csv"
print(get_Data(Data_csv))

