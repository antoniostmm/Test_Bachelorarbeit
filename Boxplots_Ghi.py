import pandas as pd
import matplotlib.pyplot as plt
import functions as fn
import errors as er
import numpy as np
import seaborn as sns

base_dir_rec = "./DWD/Recent/"

df_DWD_actual_recent_2021 = pd.read_csv(base_dir_rec + "2021/dwd_actual_recent_2021.csv")
df_DWD_actual_recent_2020 = pd.read_csv(base_dir_rec + "2020/dwd_actual_recent_2020.csv")

df_DWD_recent_gefiltert_2021 = fn.filter_dataframe_GHI(df_DWD_actual_recent_2021)
df_actual_recent_2021 = fn.tuning_DWD(df_DWD_recent_gefiltert_2021)

df_DWD_recent_gefiltert_2020 = fn.filter_dataframe_GHI(df_DWD_actual_recent_2020)
df_actual_recent_2020 = fn.tuning_DWD(df_DWD_recent_gefiltert_2020)

print("Actuals finished")

result_06_1h = fn.compare_every_historical_forecast("2021_06", 1, df_actual_recent_2021)
result_05_1h = fn.compare_every_historical_forecast("2021_05", 1, df_actual_recent_2021 )
result_04_1h = fn.compare_every_historical_forecast("2021_04", 1, df_actual_recent_2021 )
result_03_1h = fn.compare_every_historical_forecast("2021_03", 1, df_actual_recent_2021 )
result_02_1h = fn.compare_every_historical_forecast("2021_02", 1, df_actual_recent_2021 )
result_01_1h = fn.compare_every_historical_forecast("2021_01", 1, df_actual_recent_2021 )
result_12_1h = fn.compare_every_historical_forecast("2020_12", 1, df_actual_recent_2020 )
result_11_1h = fn.compare_every_historical_forecast("2020_11", 1, df_actual_recent_2020 )
result_10_1h = fn.compare_every_historical_forecast("2020_10", 1, df_actual_recent_2020 )

result_1h = pd.concat([result_01_1h,result_02_1h,result_03_1h,result_04_1h,result_05_1h,result_06_1h, result_10_1h, result_11_1h, result_12_1h], axis=0)

print("result_1h finished")

result_06_2h = fn.compare_every_historical_forecast("2021_06", 2, df_actual_recent_2021)
result_05_2h = fn.compare_every_historical_forecast("2021_05", 2, df_actual_recent_2021 )
result_04_2h = fn.compare_every_historical_forecast("2021_04", 2, df_actual_recent_2021 )
result_03_2h = fn.compare_every_historical_forecast("2021_03", 2, df_actual_recent_2021 )
result_02_2h = fn.compare_every_historical_forecast("2021_02", 2, df_actual_recent_2021 )
result_01_2h = fn.compare_every_historical_forecast("2021_01", 2, df_actual_recent_2021 )
result_12_2h = fn.compare_every_historical_forecast("2020_12", 2, df_actual_recent_2020 )
result_11_2h = fn.compare_every_historical_forecast("2020_11", 2, df_actual_recent_2020 )
result_10_2h = fn.compare_every_historical_forecast("2020_10", 2, df_actual_recent_2020 )

result_2h = pd.concat([result_01_2h,result_02_2h,result_03_2h,result_04_2h,result_05_2h,result_06_2h, result_10_2h, result_11_2h, result_12_2h], axis=0)

print("result_2h finished")

result_06_12h = fn.compare_every_historical_forecast("2021_06", 12, df_actual_recent_2021)
result_05_12h = fn.compare_every_historical_forecast("2021_05", 12, df_actual_recent_2021 )
result_04_12h = fn.compare_every_historical_forecast("2021_04", 12, df_actual_recent_2021 )
result_03_12h = fn.compare_every_historical_forecast("2021_03", 12, df_actual_recent_2021 )
result_02_12h = fn.compare_every_historical_forecast("2021_02", 12, df_actual_recent_2021 )
result_01_12h = fn.compare_every_historical_forecast("2021_01", 12, df_actual_recent_2021 )
result_12_12h = fn.compare_every_historical_forecast("2020_12", 12, df_actual_recent_2020 )
result_11_12h = fn.compare_every_historical_forecast("2020_11", 12, df_actual_recent_2020 )
result_10_12h = fn.compare_every_historical_forecast("2020_10", 12, df_actual_recent_2020 )

result_12h = pd.concat([result_01_12h,result_02_12h,result_03_12h,result_04_12h,result_05_12h,result_06_12h, result_10_12h, result_11_12h, result_12_12h], axis=0)


result_06_16h = fn.compare_every_historical_forecast("2021_06", 16, df_actual_recent_2021)
result_05_16h = fn.compare_every_historical_forecast("2021_05", 16, df_actual_recent_2021 )
result_04_16h = fn.compare_every_historical_forecast("2021_04", 16, df_actual_recent_2021 )
result_03_16h = fn.compare_every_historical_forecast("2021_03", 16, df_actual_recent_2021 )
result_02_16h = fn.compare_every_historical_forecast("2021_02", 16, df_actual_recent_2021 )
result_01_16h = fn.compare_every_historical_forecast("2021_01", 16, df_actual_recent_2021 )
result_12_16h = fn.compare_every_historical_forecast("2020_12", 16, df_actual_recent_2020 )
result_11_16h = fn.compare_every_historical_forecast("2020_11", 16, df_actual_recent_2020 )
result_10_16h = fn.compare_every_historical_forecast("2020_10", 16, df_actual_recent_2020 )

result_16h = pd.concat([result_01_16h,result_02_16h,result_03_16h,result_04_16h,result_05_16h,result_06_16h, result_10_16h, result_11_16h, result_12_16h], axis=0)


result_06_24h = fn.compare_every_historical_forecast("2021_06", 24, df_actual_recent_2021)
result_05_24h = fn.compare_every_historical_forecast("2021_05", 24, df_actual_recent_2021 )
result_04_24h = fn.compare_every_historical_forecast("2021_04", 24, df_actual_recent_2021 )
result_03_24h = fn.compare_every_historical_forecast("2021_03", 24, df_actual_recent_2021 )
result_02_24h = fn.compare_every_historical_forecast("2021_02", 24, df_actual_recent_2021 )
result_01_24h = fn.compare_every_historical_forecast("2021_01", 24, df_actual_recent_2021 )
result_12_24h = fn.compare_every_historical_forecast("2020_12", 24, df_actual_recent_2020 )
result_11_24h = fn.compare_every_historical_forecast("2020_11", 24, df_actual_recent_2020 )
result_10_24h = fn.compare_every_historical_forecast("2020_10", 24, df_actual_recent_2020 )

result_24h = pd.concat([result_01_24h,result_02_24h,result_03_24h,result_04_24h,result_05_24h,result_06_24h, result_10_24h, result_11_24h, result_12_24h], axis=0)


result_06_48h = fn.compare_every_historical_forecast("2021_06", 48, df_actual_recent_2021)
result_05_48h = fn.compare_every_historical_forecast("2021_05", 48, df_actual_recent_2021 )
result_04_48h = fn.compare_every_historical_forecast("2021_04", 48, df_actual_recent_2021 )
result_03_48h = fn.compare_every_historical_forecast("2021_03", 48, df_actual_recent_2021 )
result_02_48h = fn.compare_every_historical_forecast("2021_02", 48, df_actual_recent_2021 )
result_01_48h = fn.compare_every_historical_forecast("2021_01", 48, df_actual_recent_2021 )
result_12_48h = fn.compare_every_historical_forecast("2020_12", 48, df_actual_recent_2020 )
result_11_48h = fn.compare_every_historical_forecast("2020_11", 48, df_actual_recent_2020 )
result_10_48h = fn.compare_every_historical_forecast("2020_10", 48, df_actual_recent_2020 )

result_48h = pd.concat([result_01_48h,result_02_48h,result_03_48h,result_04_48h,result_05_48h,result_06_48h, result_10_48h, result_11_48h, result_12_48h], axis=0)

print("Every result finished")

result_16h = result_16h.drop(result_16h[result_16h.Ghi_hourly == 0].index)
result_1h = result_1h.drop(result_1h[result_1h.Ghi_hourly == 0].index)
result_48h = result_48h.drop(result_48h[result_48h.Ghi_hourly == 0].index)
result_2h = result_2h.drop(result_2h[result_2h.Ghi_hourly == 0].index)
result_24h = result_24h.drop(result_24h[result_24h.Ghi_hourly == 0].index)
result_12h = result_12h.drop(result_12h[result_12h.Ghi_hourly == 0].index)


result_1h["delta_Ghi"] = result_1h["Ghi_hf"] - result_1h["Ghi_hourly"]
result_1h["delta_Temp"] = result_1h["Temp_hf"] - result_1h["Temperature_Ambient"]

result_16h["delta_Ghi"] = result_16h["Ghi_hf"] - result_16h["Ghi_hourly"]
result_16h["delta_Temp"] = result_16h["Temp_hf"] - result_16h["Temperature_Ambient"]

result_2h["delta_Ghi"] = result_2h["Ghi_hf"] - result_2h["Ghi_hourly"]
result_2h["delta_Temp"] = result_2h["Temp_hf"] - result_2h["Temperature_Ambient"]

result_48h["delta_Ghi"] = result_48h["Ghi_hf"] - result_48h["Ghi_hourly"]
result_48h["delta_Temp"] = result_48h["Temp_hf"] - result_48h["Temperature_Ambient"]

result_12h["delta_Ghi"] = result_12h["Ghi_hf"] - result_12h["Ghi_hourly"]
result_12h["delta_Temp"] = result_12h["Temp_hf"] - result_12h["Temperature_Ambient"]

result_24h["delta_Ghi"] = result_24h["Ghi_hf"] - result_24h["Ghi_hourly"]
result_24h["delta_Temp"] = result_24h["Temp_hf"] - result_24h["Temperature_Ambient"]


delta_1h_Ghi = result_1h["delta_Ghi"].values
delta_16h_Ghi = result_16h["delta_Ghi"].values
delta_2h_Ghi = result_2h["delta_Ghi"].values
delta_48h_Ghi = result_48h["delta_Ghi"].values
delta_12h_Ghi = result_12h["delta_Ghi"].values
delta_24h_Ghi = result_24h["delta_Ghi"].values

Ghi_array = [delta_1h_Ghi, delta_2h_Ghi, delta_12h_Ghi, delta_16h_Ghi, delta_24h_Ghi , delta_48h_Ghi]


VoHo = ["1h", "2h", "12h", "16h", "24h", "48h"]

xpos= np.arange(len(VoHo))




plt.style.use("seaborn-whitegrid")
sns.boxplot(data= Ghi_array, orient="v", whis=[0,100], color="blue")
plt.title("Boxplot der Einstrahlung-Abweichung für verschiedene Vorhersagehorizonte Alle Daten")
plt.xlabel("Vorhersagehorizonte")
plt.ylabel("Delta-Ghi [W/m**2]")
plt.xticks(xpos, VoHo)
plt.show()