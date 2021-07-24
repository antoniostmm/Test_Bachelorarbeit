import pandas as pd
import functions as fn
import matplotlib.pyplot as plt
import numpy as np
import errors as er

pd.options.mode.chained_assignment = None
"""
Fehleranalyse der Temperatur für alle Daten 2020/2021 mit unterschiedlichen VoHo

Erkenntnisse:
- Gröserwerdender Fehler mit steigendem VoHo

"""
base_dir_rec = "./DWD/Recent/"

df_DWD_actual_recent_2021 = pd.read_csv(base_dir_rec + "2021/dwd_actual_recent_2021.csv")
df_DWD_actual_recent_2020 = pd.read_csv(base_dir_rec + "2020/dwd_actual_recent_2020.csv")
df_DWD_actual_recent_2018_2019 = pd.read_csv(base_dir_rec + "2018_2019/dwd_actual_recent_2018_2019.csv")

df_DWD_recent_gefiltert_2021 = fn.filter_dataframe_GHI(df_DWD_actual_recent_2021)
df_actual_recent_2021 = fn.tuning_DWD(df_DWD_recent_gefiltert_2021)

df_DWD_recent_gefiltert_2020 = fn.filter_dataframe_GHI(df_DWD_actual_recent_2020)
df_actual_recent_2020 = fn.tuning_DWD(df_DWD_recent_gefiltert_2020)

df_DWD_recent_gefiltert_2018_2019 = fn.filter_dataframe_GHI(df_DWD_actual_recent_2018_2019)
df_actual_recent_2018_2019= fn.tuning_DWD(df_DWD_recent_gefiltert_2018_2019)

result_06_48 = fn.compare_every_historical_forecast("2021_06", 48, df_actual_recent_2021)
result_05_48 = fn.compare_every_historical_forecast("2021_05", 48, df_actual_recent_2021 )
result_04_48 = fn.compare_every_historical_forecast("2021_04", 48, df_actual_recent_2021 )
result_03_48 = fn.compare_every_historical_forecast("2021_03", 48, df_actual_recent_2021 )
result_02_48 = fn.compare_every_historical_forecast("2021_02", 48, df_actual_recent_2021 )
result_01_48 = fn.compare_every_historical_forecast("2021_01", 48, df_actual_recent_2021 )
result_12_48 = fn.compare_every_historical_forecast("2020_12", 48, df_actual_recent_2020 )
result_11_48 = fn.compare_every_historical_forecast("2020_11", 48, df_actual_recent_2020 )
result_10_48 = fn.compare_every_historical_forecast("2020_10", 48, df_actual_recent_2020 )

result_06_1 = fn.compare_every_historical_forecast("2021_06", 1, df_actual_recent_2021)
result_05_1 = fn.compare_every_historical_forecast("2021_05", 1, df_actual_recent_2021 )
result_04_1 = fn.compare_every_historical_forecast("2021_04", 1, df_actual_recent_2021 )
result_03_1 = fn.compare_every_historical_forecast("2021_03", 1, df_actual_recent_2021 )
result_02_1 = fn.compare_every_historical_forecast("2021_02", 1, df_actual_recent_2021 )
result_01_1 = fn.compare_every_historical_forecast("2021_01", 1, df_actual_recent_2021 )
result_12_1 = fn.compare_every_historical_forecast("2020_12", 1, df_actual_recent_2020 )
result_11_1 = fn.compare_every_historical_forecast("2020_11", 1, df_actual_recent_2020 )
result_10_1 = fn.compare_every_historical_forecast("2020_10", 1, df_actual_recent_2020 )

result_06_16 = fn.compare_every_historical_forecast("2021_06", 16, df_actual_recent_2021)
result_05_16 = fn.compare_every_historical_forecast("2021_05", 16, df_actual_recent_2021 )
result_04_16 = fn.compare_every_historical_forecast("2021_04", 16, df_actual_recent_2021 )
result_03_16 = fn.compare_every_historical_forecast("2021_03", 16, df_actual_recent_2021 )
result_02_16 = fn.compare_every_historical_forecast("2021_02", 16, df_actual_recent_2021 )
result_01_16 = fn.compare_every_historical_forecast("2021_01", 16, df_actual_recent_2021 )
result_12_16 = fn.compare_every_historical_forecast("2020_12", 16, df_actual_recent_2020 )
result_11_16 = fn.compare_every_historical_forecast("2020_11", 16, df_actual_recent_2020 )
result_10_16 = fn.compare_every_historical_forecast("2020_10", 16, df_actual_recent_2020 )

result_1 = pd.concat([result_01_1,result_02_1,result_03_1,result_04_1,result_05_1,result_06_1, result_10_1, result_11_1, result_12_1], axis=0)
result_16 = pd.concat([result_01_16,result_02_16,result_03_16,result_04_16,result_05_16,result_06_16, result_10_16, result_11_16, result_12_16], axis=0)
result_48 = pd.concat([result_01_48,result_02_48,result_03_48,result_04_48,result_05_48,result_06_48, result_10_48, result_11_48, result_12_48], axis=0)

error_list_names = ["RMSE", "MBE","MAE", "SD"]
error_list_names_relative = ["rRMSE", "rMBE","rMAE", "rSD", "R_2"]

error_list_1 = er.get_errors(result_1, "Temp_hf", "Temperature_Ambient")
error_list_16 = er.get_errors(result_16, "Temp_hf", "Temperature_Ambient")
error_list_48 = er.get_errors(result_48, "Temp_hf", "Temperature_Ambient")


error_list_relative_1 = er.get_errors_relative(result_1, "Temp_hf", "Temperature_Ambient")
error_list_relative_16 = er.get_errors_relative(result_16, "Temp_hf", "Temperature_Ambient")
error_list_relative_48 = er.get_errors_relative(result_48, "Temp_hf", "Temperature_Ambient")


plt.style.use("seaborn-whitegrid")
plt.subplot(2,1,1)
xpos= np.arange(len(error_list_names))


plt.bar(xpos-0.3, error_list_1,width=0.3, label="1h", color="green")
plt.bar(xpos, error_list_16,width=0.3, label="16", color="blue")
plt.bar(xpos+0.3, error_list_48,width=0.3, label="48h", color="red")

for i in range(len(error_list_names)):
    plt.text(i - 0.3, error_list_1[i], round(error_list_1[i], 2), ha="center", va="bottom")
    plt.text(i , error_list_16[i], round(error_list_16[i], 2), ha="center", va="bottom")
    plt.text(i + 0.3, error_list_48[i], round(error_list_48[i], 2), ha="center", va="bottom")

plt.title("Fehler der Temperatur-vorhersagen für alle Daten mit unterschiedlichen Vorhersagehorizont")
plt.xticks(xpos, error_list_names)
plt.ylabel("Temperatur in K")
plt.legend()

plt.subplot(2,1,2)
xpos= np.arange(len(error_list_names_relative))
plt.bar(xpos-0.3, error_list_relative_1,width=0.3, label="1h", color="green")
plt.bar(xpos, error_list_relative_16,width=0.3, label="16", color="blue")
plt.bar(xpos+0.3, error_list_relative_48,width=0.3, label="48h", color="red")

for i in range(len(error_list_names_relative)):
    plt.text(i - 0.3, error_list_relative_1[i], round(error_list_relative_1[i], 2), ha="center", va="bottom")
    plt.text(i , error_list_relative_16[i], round(error_list_relative_16[i], 2), ha="center", va="bottom")
    plt.text(i + 0.3, error_list_relative_48[i], round(error_list_relative_48[i], 2), ha="center", va="bottom")

plt.title("Relative Fehler der Temperatur-vorhersagen für alle Daten mit unterschiedlichen Vorhersagehorizont")
plt.xticks(xpos, error_list_names_relative)
plt.ylabel("Temperatur in K")
plt.legend()

plt.legend()
plt.show()