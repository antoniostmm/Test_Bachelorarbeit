import matplotlib.pyplot as plt
import pandas as pd
import import_DWD_weather_2_pd_DataFrame
import functions as fn

# pd.options.mode.chained_assignment = None
#
#df_DWD = pd.read_csv("DWD/Recent/produkt_zehn_min_tu_20100101_20191231_00433.txt", sep=';')
#

#
# df_DWD = df_DWD.drop(["STATIONS_ID", "eor", "SD_10", "LS_10", "DS_10"], axis=1)
# #df["PeriodEnd"] = pd.to_datetime(df_DWD["MESS_DATUM"], format="%Y-%m-%d")
#
#
# df["PeriodEnd"] = 1
# for i in range(len(df)):
#     df["PeriodEnd"][i] = str(df["MESS_DATUM"])[0:5]
#
#
# print(df)

#Dataframe mit import_DWD speichern. Station_id 00433 =Berlin
#df_DWD = import_DWD_weather_2_pd_DataFrame.measurement(station_id= "00433", measurements="all", now= False, recent= True, historical = True)
# df_DWD.to_csv("./DWD/Recent/dwd_historical_2018_2019.csv", encoding='utf-8')

# df_DWD['timestamp'] = pd.to_datetime(df_DWD['MESS_DATUM'], format='%Y%m%d%H%M', errors='ignore')
# df_DWD.set_index("timestamp", drop=True, inplace=True)
# df_DWD= df_DWD.drop(["STATIONS_ID", "eor", "PP_10", "RF_10", "TM5_10", "MESS_DATUM"], axis=1)
# df_DWD.rename(columns={"TT_10": 'Temperature'}, inplace=True)
#
# print(df_DWD.tail(55000))
#
# df = df_DWD.tail(55000)
#
# plt.plot(df.index, df["Temperature"])
# plt.show()
#df_DWD_historical_gefiltert = fn.filter_dataframe_GHI(df)


# faktor_Ghi_10min = 10000/600
# faktor_Ghi_hourly = 1000/3600
#
#
#
#
#
# #
# df_DWD_historical_gefiltert["Ghi"] = round(df_DWD_historical_gefiltert["Global_sky_radiation"]*faktor_Ghi_10min,1)
# df_DWD_historical_gefiltert["E"] = df_DWD_historical_gefiltert["Global_sky_radiation"]*10
#
# df_DWD_historical_gefiltert["Ghi_hourly"] = 0
# df_DWD_historical_gefiltert["E_hourly"] = 0
# for i in range(len(df_DWD_historical_gefiltert["Ghi"])):
#     if i > 4:
#         df_DWD_historical_gefiltert["E_hourly"][i] = df_DWD_historical_gefiltert["E"][i] + df_DWD_historical_gefiltert["E"][i-1] + df_DWD_historical_gefiltert["E"][i-2] + df_DWD_historical_gefiltert["E"][i-3] + df_DWD_historical_gefiltert["E"][i-4] + df_DWD_historical_gefiltert["E"][i-5]
#         df_DWD_historical_gefiltert["Ghi_hourly"][i] = (df_DWD_historical_gefiltert["Ghi"][i] + df_DWD_historical_gefiltert["Ghi"][i-1] + df_DWD_historical_gefiltert["Ghi"][i-2] + df_DWD_historical_gefiltert["Ghi"][i-3] + df_DWD_historical_gefiltert["Ghi"][i-4] + df_DWD_historical_gefiltert["Ghi"][i-5])/6
#     else:
#         df_DWD_historical_gefiltert["Ghi_hourly"][i] = 0


df_actual_temperature = pd.read_csv("DWD/Recent/2018_2019/dwd_actual_temperature.csv")
df_actual_ghi = pd.read_csv("DWD/Recent/2018_2019/dwd_actual_recent_2018_2019.csv")

df_actual_temperature = fn.tuning_DWD(df_actual_temperature)
df_actual_ghi = fn.tuning_DWD(df_actual_ghi)

result = pd.concat([df_actual_ghi,df_actual_temperature], axis=1)
df_actual_historical = result[["Global_sky_radiation", "E_hourly", "Ghi_hourly", "Temperature"]]
print(df_actual_historical)
df_actual_historical.rename(columns= {"Temperature" : "Temperature_Ambient"} , inplace=True)
df_actual_historical.to_csv("./DWD/Recent/2018_2019/dwd_actual_recent_2018_2019.csv", encoding='utf-8')

#
# df_actual_recent_2020 = df_actual_recent.drop(df_actual_recent[df_actual_recent.index.year !=2020].index)
# df_actual_recent_2021 = df_actual_recent.drop(df_actual_recent[df_actual_recent.index.year !=2021].index)
#
# df_actual_recent_2020.to_csv("./DWD/Recent/2020/dwd_actual_recent_2020.csv", encoding='utf-8')
# df_actual_recent_2021.to_csv("./DWD/Recent/2021/dwd_actual_recent_2021.csv", encoding='utf-8')

#print(df_actual_recent)
#df_actual_temperature.to_csv("./DWD/Recent/2018_2019/dwd_actual_temperature.csv", encoding='utf-8')


# faktor_Ghi_10min = 10000/600
# faktor_Ghi_hourly = 1000/3600
#
#
# #df =
# df_DWD_recent = pd.read_csv(base_dir_rec + "2021-06-22_10.csv")
# df_DWD_recent_gefiltert = fn.filter_dataframe_GHI(df_DWD_recent)
# df_DWD_tuned = fn.tuning_DWD(df_DWD_recent_gefiltert)
#
# df_DWD_tuned["Ghi"] = round(df_DWD_tuned["Global_sky_radiation"]*faktor_Ghi_10min,1)
# df_DWD_tuned["E"] = df_DWD_tuned["Global_sky_radiation"]*10
#
# df_DWD_tuned["Ghi_hourly"] = 0
# df_DWD_tuned["E_hourly"] = 0
# for i in range(len(df_DWD_tuned["Ghi"])):
#     if i > 4:
#         df_DWD_tuned["E_hourly"][i] = df_DWD_tuned["E"][i] + df_DWD_tuned["E"][i-1] + df_DWD_tuned["E"][i-2] + df_DWD_tuned["E"][i-3] + df_DWD_tuned["E"][i-4] + df_DWD_tuned["E"][i-5]
#         df_DWD_tuned["Ghi_hourly"][i] = (df_DWD_tuned["Ghi"][i] + df_DWD_tuned["Ghi"][i-1] + df_DWD_tuned["Ghi"][i-2] + df_DWD_tuned["Ghi"][i-3] + df_DWD_tuned["Ghi"][i-4] + df_DWD_tuned["Ghi"][i-5])/6
#     else:
#         df_DWD_tuned["Ghi_hourly"][i] = 0
#
#
# df_actual_recent = df_DWD_tuned.drop(df_DWD_tuned[df_DWD_tuned.index.minute != 0].index)
#
# df_actual_recent_2020 = df_actual_recent.drop(df_actual_recent[df_actual_recent.index.year !=2020].index)
# df_actual_recent_2021 = df_actual_recent.drop(df_actual_recent[df_actual_recent.index.year !=2021].index)
#
# df_actual_recent_2020.to_csv("./DWD/Recent/2020/dwd_actual_recent_2020.csv", encoding='utf-8')
# df_actual_recent_2021.to_csv("./DWD/Recent/2021/dwd_actual_recent_2021.csv", encoding='utf-8')