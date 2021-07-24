import pandas as pd
import functions as fn
import matplotlib.pyplot as plt
import numpy as np
import errors as er

pd.options.mode.chained_assignment = None
"""
Vergleich von DWD-Daten für zwei gleiche Zeitperioden in 2019 und 2021 (Dezember-März).
2019: vor Corona. Die durchschittliche Temperatur für diese Periode in 2019: 4,86ºC
2021: mit Corona. Die durchshnittliche Temperatur für diese Periode in 2021: 2.21ºC


Plottet Fehler der Einstrahlung-Vorhersagen für beide Datensätze mit und ohne Nachtwerte mit wählbaren VoHo.
Plottet Fehler der Temperatur-Vorhersagen für beide Datensätze mit wählbaren VoHo.

Erkenntnisse:
1) Relative Fehler nur eingeschränkt vergleichbar, denn die durchschnittliche Werte (mit denen normalisiert wird),
   unterschiedlich sind. (Temperatur und Einstrahlung)

2) Für die Zeitperiode von 2021 wird konservativ prognostiziert, sodass die solare Einstrahlung unterschätzt wird:
   (negativer MBE)
   Für die Zeitperiode von 2019 hingegen, wird die solare Einstrahlung systematisch überschätzt (positiver MBE)
   
3) Die durchschnittliche Einstrahlung ist größer für 2019.Als Folge sind die Fehler generell für 2021 niedriger außer
   der Determinatioskoeffizient R^2

4) Wie üblich werden die Fehler mit steigendem VoHo schlechter, aber der Unteschied zwischen 1h und 16h ist immmernoch 
   kleiner als erwartet.

5) Auch wie üblich: Bei Auslassung der Nachtwerte werden die absoluten Fehler größer,da die triviale Vorhersage von
   Nachtwerten den absoluten Fehler positiv beeinflusst. Ganz im Gegenteil werden die relative Fehler kleiner,
   da der durchschittliche Normalisierungswert größer wird.
   
Temperatur:
6) Die Temperatur-Vorhersagen sind ziemlich gleich für beide Perioden, da die absolute Fehler fast identisch sind. Die 
   relative Fehler sind nur eingeschränkt vergleichbar, weil die durchschnittliche Temperatur von 2019 doppelt so hoch 
   ist wie die von 2021
   
Offene Fragen:
- Hat die Temperatur einen Einfluss auf die Einstrahling?
- Bewirkt der große Unteschied der durchschittlichen Temperatur die unterschiedlichen Fehler?
- Warum wurde die Tendez von Unterschätung/Überschätzung für den MBE geändert ?


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



result_03_2021 = fn.compare_every_historical_forecast("2021_03", 1, df_actual_recent_2021 )
result_02_2021 = fn.compare_every_historical_forecast("2021_02", 1, df_actual_recent_2021 )
result_01_2021 = fn.compare_every_historical_forecast("2021_01", 1, df_actual_recent_2021 )
result_12_2020 = fn.compare_every_historical_forecast("2020_12", 1, df_actual_recent_2020 )

result_03_2019 = fn.compare_every_historical_forecast("2019_03", 1, df_actual_recent_2018_2019 )
result_02_2019 = fn.compare_every_historical_forecast("2019_02", 1, df_actual_recent_2018_2019 )
result_01_2019 = fn.compare_every_historical_forecast("2019_01", 1, df_actual_recent_2018_2019 )
result_12_2018 = fn.compare_every_historical_forecast("2018_12", 1, df_actual_recent_2018_2019 )

result_2021 = pd.concat([result_01_2021,result_02_2021,result_03_2021,result_12_2020], axis=0)
result_2021_day = result_2021.drop(result_2021[result_2021.Ghi_hourly == 0].index)

result_2019 = pd.concat([result_01_2019,result_02_2019,result_03_2019,result_12_2018], axis=0)
result_2019_day = result_2019.drop(result_2019[result_2019.Ghi_hourly == 0].index)



error_list_names = ["RMSE", "MBE","MAE", "SD"]
error_list_names_relative = ["rRMSE", "rMBE","rMAE", "rSD", "R_2"]

error_list_2021 = er.get_errors(result_2021, "Ghi_hf", "Ghi_hourly")
error_list_2021_day = er.get_errors(result_2021_day, "Ghi_hf", "Ghi_hourly")

error_list_2019 = er.get_errors(result_2019, "Ghi_hf", "Ghi_hourly")
error_list_2019_day = er.get_errors(result_2019_day, "Ghi_hf", "Ghi_hourly")

error_list_2021_relative = er.get_errors_relative(result_2021, "Ghi_hf", "Ghi_hourly")
error_list_2021_day_relative = er.get_errors_relative(result_2021_day, "Ghi_hf", "Ghi_hourly")

error_list_2019_relative = er.get_errors_relative(result_2019, "Ghi_hf", "Ghi_hourly")
error_list_2019_day_relative = er.get_errors_relative(result_2019_day, "Ghi_hf", "Ghi_hourly")






plt.style.use("seaborn-whitegrid")
plt.subplot(2,1,1)
xpos= np.arange(len(error_list_names))


plt.bar(xpos-0.2, error_list_2019, width=0.4, label="2018/19", color="red")
plt.bar(xpos+0.2, error_list_2021, width=0.4, label="2020/21", color="green")
for i in range(len(error_list_names)):
    plt.text(i - 0.2, error_list_2019[i], int(round(error_list_2019[i], 0)), ha="center", va="bottom")
    plt.text(i + 0.2, error_list_2021[i], int(round(error_list_2021[i], 0)), ha="center", va="bottom")

plt.title("Fehler der Vorhersagen für beide Datensätze Dezember-März mit 1h-Vorhersagehorizont")
plt.xticks(xpos, error_list_names)
plt.ylabel("Ghi")
plt.legend()

plt.subplot(2,1,2)
xpos= np.arange(len(error_list_names_relative))
plt.bar(xpos-0.2, error_list_2019_relative, width=0.4, label="2018/19", color="red")
plt.bar(xpos+0.2, error_list_2021_relative, width=0.4, label="2020/21", color="green")
for i in range(len(error_list_names_relative)):
    plt.text(i - 0.2, error_list_2019_relative[i], round(error_list_2019_relative[i], 2), ha="center", va="bottom")
    plt.text(i + 0.2, error_list_2021_relative[i], round(error_list_2021_relative[i], 2), ha="center", va="bottom")

plt.title("Relative Fehler der Vorhersagen für beide Datensätze Dezember-März mit 1h-Vorhersagehorizont")
plt.xticks(xpos, error_list_names_relative)
plt.ylabel("-")

plt.legend()
plt.show()





plt.style.use("seaborn-whitegrid")
plt.subplot(2,1,1)
xpos= np.arange(len(error_list_names))


plt.bar(xpos-0.2, error_list_2019_day, width=0.4, label="2018/19", color="red")
plt.bar(xpos+0.2, error_list_2021_day, width=0.4, label="2020/21", color="green")
for i in range(len(error_list_names)):
    plt.text(i - 0.2, error_list_2019_day[i], int(round(error_list_2019_day[i], 0)), ha="center", va="bottom")
    plt.text(i + 0.2, error_list_2021_day[i], int(round(error_list_2021_day[i], 0)), ha="center", va="bottom")

plt.title("Fehler der Vorhersagen für beide Datensätze Dezember-März mit 1h-Vorhersagehorizont (day only)")
plt.xticks(xpos, error_list_names)
plt.ylabel("Ghi")
plt.legend()

plt.subplot(2,1,2)
xpos= np.arange(len(error_list_names_relative))
plt.bar(xpos-0.2, error_list_2019_day_relative, width=0.4, label="2018/19", color="red")
plt.bar(xpos+0.2, error_list_2021_day_relative, width=0.4, label="2020/21", color="green")
for i in range(len(error_list_names_relative)):
    plt.text(i - 0.2, error_list_2019_day_relative[i], round(error_list_2019_day_relative[i], 2), ha="center", va="bottom")
    plt.text(i + 0.2, error_list_2021_day_relative[i], round(error_list_2021_day_relative[i], 2), ha="center", va="bottom")

plt.title("Relative Fehler der Vorhersagen für beide Datensätze Dezember-März mit 1h-Vorhersagehorizont (day only)")
plt.xticks(xpos, error_list_names_relative)
plt.ylabel("-")

plt.legend()
plt.show()






error_list_2021_temp = er.get_errors(result_2021, "Temp_hf", "Temperature_Ambient")

error_list_2019_temp = er.get_errors(result_2019, "Temp_hf", "Temperature_Ambient")

error_list_2021_temp_relative = er.get_errors_relative(result_2021, "Temp_hf", "Temperature_Ambient")

error_list_2019_temp_relative = er.get_errors_relative(result_2019, "Temp_hf", "Temperature_Ambient")

plt.subplot(2,1,1)
xpos= np.arange(len(error_list_names))


plt.bar(xpos-0.2, error_list_2019_temp, width=0.4, label="2018/19", color="red")
plt.bar(xpos+0.2, error_list_2021_temp, width=0.4, label="2020/21", color="green")
for i in range(len(error_list_names)):
    plt.text(i - 0.2, error_list_2019_temp[i], round(error_list_2019_temp[i], 2), ha="center", va="bottom")
    plt.text(i + 0.2, error_list_2021_temp[i], round(error_list_2021_temp[i], 2), ha="center", va="bottom")

plt.title("Fehler der Temperatur-Vorhersagen für beide Datensätze Dezember-März mit 1h-Vorhersagehorizont")
plt.xticks(xpos, error_list_names)
plt.ylabel("Ghi")
plt.legend()

plt.subplot(2,1,2)
xpos= np.arange(len(error_list_names_relative))
plt.bar(xpos-0.2, error_list_2019_temp_relative, width=0.4, label="2018/19", color="red")
plt.bar(xpos+0.2, error_list_2021_temp_relative, width=0.4, label="2020/21", color="green")
for i in range(len(error_list_names_relative)):
    plt.text(i - 0.2, error_list_2019_temp_relative[i], round(error_list_2019_temp_relative[i], 2), ha="center", va="bottom")
    plt.text(i + 0.2, error_list_2021_temp_relative[i], round(error_list_2021_temp_relative[i], 2), ha="center", va="bottom")

plt.title("Relative Fehler der Temperatur-Vorhersagen für beide Datensätze Dezember-März mit 1h-Vorhersagehorizont")
plt.xticks(xpos, error_list_names_relative)
plt.ylabel("-")

plt.legend()
plt.show()

plt.plot(result_2021.index, result_2021["Temperature_Ambient"], label= "2021")
plt.plot(result_2019.index, result_2019["Temperature_Ambient"], label= "2019")
plt.legend()
plt.show()