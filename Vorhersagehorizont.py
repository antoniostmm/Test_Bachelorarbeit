import pandas as pd
import matplotlib.pyplot as plt
import functions as fn
import errors as er
import numpy as np
import seaborn as sns

"""
Plottet für einen Monat (frei wählbar) die Messwerte und die Vorhersagen mit unterschiedlichen VoHo (1h, 16h, 48h)

Fehleranalyse für einen Monat (frei wählbar) mit unterschiedlichen VoHo (1h, 16h, 48h):
 - Rolling mit Nachtwerte
 - Rolling ohne Nachwerte
 - Alle Daten mit Nachtwerte
 - Alle Daten ohne Nachtwerte

1) Es muss darauf geachtet werden, dass für einige Monate wie 03.2021 oder 04.2021 nicht alle Daten vorhanden sind.

Erkenntisse:
1) Für unterschiedliche Monate sind sehr unterschiedliche Erkenntnisse ersichtlich:
    - Mai 2021 ist sehr auffällig, da der Unterschied zwischen 1h und 16h VoHo sehr klein ist.
    - Juni 2021 weisst den grössten Unterschied zwischen den VoHo
    - Tendenz (ausser Juni 2021) für kältere Monate sind die Abweichungen zwischen den Voho grösser
    
2) Kaum Unterschied zwischen rolling und All Data

3) übliche Erkenntnisse für die Berücksichtigung der Nachtwerte

Offene Fragen:
- Wovon hängen die Fehler wirklich ab ?
- Warum plötzlich überschätzung für Juni 2021 ? (Näher analysieren)

"""
base_dir_rec = "./DWD/Recent/"

df_DWD_actual_recent_2018_2019 = pd.read_csv(base_dir_rec + "2018_2019/dwd_actual_recent_2018_2019.csv")
df_DWD_actual_recent_2021 = pd.read_csv(base_dir_rec + "2021/dwd_actual_recent_2021.csv")
df_DWD_actual_recent_2020 = pd.read_csv(base_dir_rec + "2020/dwd_actual_recent_2020.csv")


df_DWD_recent_gefiltert_2021 = fn.filter_dataframe_GHI(df_DWD_actual_recent_2021)
df_actual_recent_2021 = fn.tuning_DWD(df_DWD_recent_gefiltert_2021)

df_DWD_recent_gefiltert_2020 = fn.filter_dataframe_GHI(df_DWD_actual_recent_2020)
df_actual_recent_2020 = fn.tuning_DWD(df_DWD_recent_gefiltert_2020)

df_DWD_recent_gefiltert_2018_2019 = fn.filter_dataframe_GHI(df_DWD_actual_recent_2018_2019)
df_actual_recent_2018_2019= fn.tuning_DWD(df_DWD_recent_gefiltert_2018_2019)


result_16h = fn.compare_DWD_historical_month("2021_06", 16, df_actual_recent_2021)
#result_16h = result_16h.drop(result_16h[result_16h.Ghi_hourly == 0].index)
#result_16h = fn.compare_every_historical_forecast("2021_05", 16, df_actual_recent_2021)

result_1h = fn.compare_DWD_historical_month("2021_06", 1, df_actual_recent_2021)
#result_1h = result_1h.drop(result_1h[result_1h.Ghi_hourly == 0].index)
#result_1h = fn.compare_every_historical_forecast("2021_05", 1, df_actual_recent_2021)

result_48h = fn.compare_DWD_historical_month("2021_06", 48, df_actual_recent_2021)
#result_48h = result_48h.drop(result_48h[result_48h.Ghi_hourly == 0].index)
#result_48h = fn.compare_every_historical_forecast("2021_05", 48, df_actual_recent_2021)



result_1h["delta_Ghi"] = result_1h["Ghi_hf"] - result_1h["Ghi_hourly"]
result_1h["delta_Temp"] = result_1h["Temp_hf"] - result_1h["Temperature_Ambient"]



plt.plot(result_16h.index, result_16h["Ghi_hourly"], label="Ghi actual (hourly mean)", c="black")
plt.plot(result_48h.index, result_48h["Ghi_hf"], label="historical forecast 48h", c="yellow")
plt.plot(result_16h.index, result_16h["Ghi_hf"], label="historical forecast 16h", c="red")
plt.plot(result_1h.index, result_1h["Ghi_hf"], label="historical forecast 1h", c="blue")

plt.title("Vergleich Messdaten mit Vorhersagen mit unterschiedlichen VoHo")
plt.ylabel("Ghi in W/m**2")

plt.legend()
plt.show()

error_list_names = ["RMSE", "MBE","MAE", "SD"]
error_list_names_relative = ["rRMSE", "rMBE","rMAE", "rSD", "R_2"]

error_list_1h = er.get_errors(result_1h, "Ghi_hf", "Ghi_hourly")
error_list_16h = er.get_errors(result_16h, "Ghi_hf", "Ghi_hourly")
error_list_48h = er.get_errors(result_48h, "Ghi_hf", "Ghi_hourly")

error_list_relative_1h = er.get_errors_relative(result_1h, "Ghi_hf", "Ghi_hourly")
error_list_relative_16h = er.get_errors_relative(result_16h, "Ghi_hf", "Ghi_hourly")
error_list_relative_48h = er.get_errors_relative(result_48h, "Ghi_hf", "Ghi_hourly")

plt.style.use("seaborn-whitegrid")
plt.subplot(2,1,1)
xpos= np.arange(len(error_list_names))

plt.bar(xpos-0.3, error_list_1h,width=0.3, label="1h Auflösung", color="green")
plt.bar(xpos, error_list_16h, width=0.3, label="16h Auflösung", color="blue")
plt.bar(xpos+0.3, error_list_48h, width=0.3, label="48h Auflösung", color="red")
for i in range(len(error_list_names)):
    plt.text(i - 0.3, error_list_1h[i], int(round(error_list_1h[i], 0)), ha="center", va="bottom")
    plt.text(i , error_list_16h[i], int(round(error_list_16h[i], 0)), ha="center", va="bottom")
    plt.text(i + 0.3 , error_list_48h[i], int(round(error_list_48h[i], 0)), ha="center", va="bottom")

plt.title("Fehler der Vorhersagen mit unteschiedlichen Vorhersagehorizonts für Juni 2021 mit nighttime")
plt.xticks(xpos, error_list_names)
plt.ylabel("Ghi")
plt.legend()

plt.subplot(2,1,2)
xpos= np.arange(len(error_list_names_relative))
plt.bar(xpos-0.3, error_list_relative_1h, width=0.3, label="1h Auflösung", color="green")
plt.bar(xpos, error_list_relative_16h, width=0.3, label="16h Auflösung", color="blue")
plt.bar(xpos+0.3, error_list_relative_48h, width=0.3, label="48h Auflösung", color="red")
for i in range(len(error_list_names_relative)):
    plt.text(i - 0.3, error_list_relative_1h[i], round(error_list_relative_1h[i], 2), ha="center", va="bottom")
    plt.text(i , error_list_relative_16h[i], round(error_list_relative_16h[i], 2), ha="center", va="bottom")
    plt.text(i + 0.3, error_list_relative_48h[i], round(error_list_relative_48h[i], 2), ha="center", va="bottom")

plt.title("Relative Fehler der Vorhersagen mit unteschiedlichen Vorhersagehorizonts für Juni 2021 mit nighttime")
plt.xticks(xpos, error_list_names_relative)
plt.ylabel("-")

plt.legend()
plt.show()




result_16h_allData = fn.compare_every_historical_forecast("2021_06", 16, df_actual_recent_2021)
#result_16h_allData = result_16h_allData.drop(result_16h_allData[result_16h_allData.Ghi_hourly == 0].index)

result_1h_allData = fn.compare_every_historical_forecast("2021_06", 1, df_actual_recent_2021)
#result_1h_allData = result_1h_allData.drop(result_1h_allData[result_1h_allData.Ghi_hourly == 0].index)

result_48h_allData = fn.compare_every_historical_forecast("2021_06", 48, df_actual_recent_2021)
#result_48h_allData = result_48h_allData.drop(result_48h_allData[result_48h_allData.Ghi_hourly == 0].index)

error_list_1h_allData = er.get_errors(result_1h_allData, "Ghi_hf", "Ghi_hourly")
error_list_16h_allData = er.get_errors(result_16h_allData, "Ghi_hf", "Ghi_hourly")
error_list_48h_allData = er.get_errors(result_48h_allData, "Ghi_hf", "Ghi_hourly")

error_list_relative_1h_allData = er.get_errors_relative(result_1h_allData, "Ghi_hf", "Ghi_hourly")
error_list_relative_16h_allData = er.get_errors_relative(result_16h_allData, "Ghi_hf", "Ghi_hourly")
error_list_relative_48h_allData = er.get_errors_relative(result_48h_allData, "Ghi_hf", "Ghi_hourly")



plt.style.use("seaborn-whitegrid")
plt.subplot(2,1,1)
xpos= np.arange(len(error_list_names))

plt.bar(xpos-0.3, error_list_1h_allData,width=0.3, label="1h Auflösung", color="green")
plt.bar(xpos, error_list_16h_allData, width=0.3, label="16h Auflösung", color="blue")
plt.bar(xpos+0.3, error_list_48h_allData, width=0.3, label="48h Auflösung", color="red")
for i in range(len(error_list_names)):
    plt.text(i - 0.3, error_list_1h_allData[i], int(round(error_list_1h_allData[i], 0)), ha="center", va="bottom")
    plt.text(i , error_list_16h_allData[i], int(round(error_list_16h_allData[i], 0)), ha="center", va="bottom")
    plt.text(i + 0.3 , error_list_48h_allData[i], int(round(error_list_48h_allData[i], 0)), ha="center", va="bottom")

plt.title("Fehler der Vorhersagen mit unteschiedlichen Vorhersagehorizonts für Juni 2021 mit nighttime (all Data)")
plt.xticks(xpos, error_list_names)
plt.ylabel("Ghi")
plt.legend()

plt.subplot(2,1,2)
xpos= np.arange(len(error_list_names_relative))
plt.bar(xpos-0.3, error_list_relative_1h_allData, width=0.3, label="1h Auflösung", color="green")
plt.bar(xpos, error_list_relative_16h_allData, width=0.3, label="16h Auflösung", color="blue")
plt.bar(xpos+0.3, error_list_relative_48h_allData, width=0.3, label="48h Auflösung", color="red")
for i in range(len(error_list_names_relative)):
    plt.text(i - 0.3, error_list_relative_1h_allData[i], round(error_list_relative_1h_allData[i], 2), ha="center", va="bottom")
    plt.text(i , error_list_relative_16h_allData[i], round(error_list_relative_16h_allData[i], 2), ha="center", va="bottom")
    plt.text(i + 0.3, error_list_relative_48h_allData[i], round(error_list_relative_48h_allData[i], 2), ha="center", va="bottom")

plt.title("Relative Fehler der Vorhersagen mit unteschiedlichen Vorhersagehorizonts für Juni 2021 mit nighttime (all Data)")
plt.xticks(xpos, error_list_names_relative)
plt.ylabel("-")

plt.legend()
plt.show()
