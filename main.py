import pandas as pd
import numpy as np
import os
import datetime as dt
import matplotlib.pyplot as plt
import functions
import plotFunctions as pf


#Defining the actual data
df_solarradiation_actuals_14_06 = pd.read_csv("./Solcast/SolarRadiation/EstimatedActuals/GetWeatherSiteEstimatedActuals_14_06.csv")
df_solarradiation_actuals_14_06["period_end"] = pd.to_datetime(df_solarradiation_actuals_14_06["period_end"])
df_solarradiation_actuals_14_06.set_index("period_end", drop=False, inplace=True)


#Create a list of dataframes
list_df_result = []


#Concatinating the different forecasts to the actual data and adding them to a list: list_df_result[]
for i in range(9,14):
    df = pd.read_csv("./Solcast/SolarRadiation/Forecasts/GetWeatherSiteForecast_" + str(i) + "_06.csv")
    df["period_end"] = pd.to_datetime(df["period_end"])

    df.set_index("period_end", drop=False, inplace=True)
    df.rename(columns={"Ghi": "Ghi_forecast_" + str(i) + "_06"}, inplace=True)
    result = pd.concat([df, df_solarradiation_actuals_14_06], axis=1, join="inner")
    result["delta_" + str(i) + "_06"] = result["Ghi"] - result["Ghi_forecast_" + str(i) + "_06"]
    list_df_result.append(result)


time = list_df_result[0].index

plt.plot(time, list_df_result[0]["Ghi"], label= "Ghi_actual", color= "black")
for f in range(0,5):
    plt.plot(list_df_result[f].index, list_df_result[f]["Ghi_forecast_" + str(f+9) + "_06"], label= "Ghi_forecast_" + str(f+9) + "_06")
plt.title("Global horizontal Irradiance for different forecasting times")
plt.xlabel("Time")
plt.ylabel("Ghi")
plt.legend()
plt.show()

for f in range(0,5):
    plt.plot(list_df_result[f].index, list_df_result[f]["delta_" + str(f+9) + "_06"], label= "delta_Ghi_" + str(f+9) + "_06")
plt.xlabel("Time")
plt.ylabel("Delta Ghi für jeden forecast")
plt.legend()
plt.show()






#plot_mean_Ghi_in_day(df_solarRadiation_actuals)




