import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import functions as fn
import errors as er

"""
Ähnliche Dokumentation wie vergleich_DWD_solcast

speziell für Temperatur:
- Keine Auswertung für Auslassung der Nachtwerte
- Die Solcast-Vorhersagen schätzen die Temperatur nur in ganzen Zahlen während die DWD-Daten
   und die Solcast-Messdaten mit einer Nachkommastelle angegeben wird.
- Absoluter Fehler grösser als für andere Monate, da die Temperatur höhere Werte annimmt
- Dafür geringere relative Fehler
"""
dir_a = "./Solcast/SolarRadiation/EstimatedActuals/GetWeatherSiteEstimatedActuals_"
dir_f = "./Solcast/SolarRadiation/Forecasts/GetWeatherSiteForecast_"

error_list_names = ["RMSE", "MBE","MAE", "SD"]
error_list_names_relative = ["rRMSE", "rMBE","rMAE", "rSD", "R_2"]


list_df_forecast = []
for i in range(1,31):
    try:
        list_df_forecast.append(fn.tuning_df_solcast(pd.read_csv(dir_f + str(i).zfill(2) + "_06.csv")))
    except: continue


historical = pd.read_csv("Solcast/Historical/Solcast_Juni_actuals_30M.csv")
historical = fn.tuning_df_solcast(historical)

result_forecast = pd.concat(list_df_forecast, axis= 0 , join ="inner")
result_forecast = result_forecast.drop_duplicates(subset= "period_end", keep= "last")

result_solcast = fn.concat_2_dataframes(result_forecast, historical)

error_list_solcast = er.get_errors(result_solcast, "AirTemp", "AirTemp_for")
error_list_solcast_relative = er.get_errors_relative(result_solcast, "AirTemp", "AirTemp_for")






base_dir_rec = "./DWD/Recent/"

df_DWD_actual_recent_2021 = pd.read_csv(base_dir_rec + "2021/dwd_actual_recent_2021.csv")

df_DWD_recent_gefiltert_2021 = fn.filter_dataframe_GHI(df_DWD_actual_recent_2021)
df_actual_recent_2021 = fn.tuning_DWD(df_DWD_recent_gefiltert_2021)

result_dwd = fn.compare_DWD_historical_month("2021_06", 24, df_actual_recent_2021 )


error_list_dwd = er.get_errors(result_dwd, "Temp_hf", "Temperature_Ambient")
error_list_dwd_relative = er.get_errors_relative(result_dwd, "Temp_hf", "Temperature_Ambient")




plt.plot(result_dwd.index, result_dwd["Temperature_Ambient"], label="dwd_actual", c="blue")
plt.plot(result_dwd.index, result_dwd["Temp_hf"], label="dwd_forecast", c="lightblue")
plt.plot(result_solcast.index, result_solcast["AirTemp"], label="solcast_actual", c="red")
plt.plot(result_solcast.index, result_solcast["AirTemp_for"], label="solcast_forecast", c="lightsalmon")
plt.legend()
plt.ylabel("Temperatur in ºC")
plt.title("Vergleich Temperatur Solcast und DWD für Juni")
plt.show()

# plt.plot(result_dwd.index, result_dwd["N"], label="N", c="blue")
# plt.plot(result_dwd.index, result_dwd["Neff"], label="Neff", c="lightblue")
# #plt.plot(result_solcast.index, result_solcast["cloud_opacity_for"], label="cloud_opacity_for", c="red")
# plt.plot(result_solcast.index, result_solcast["CloudOpacity"], label="cloud_opacity", c="lightsalmon")
# plt.legend()
# plt.ylabel("Temperatur in ºC")
# plt.title("Vergleich Temperatur Solcast und DWD für Juni")
# plt.show()
#






plt.style.use("seaborn-whitegrid")
plt.subplot(2,1,1)
xpos= np.arange(len(error_list_names))

plt.bar(xpos-0.2, error_list_dwd,width=0.4, label="dwd", color="blue")
plt.bar(xpos+0.2, error_list_solcast, width=0.4, label="solcast", color="orange")
for i in range(len(error_list_names)):
    plt.text(i-0.2, error_list_dwd[i], round(error_list_dwd[i], 1), ha="center", va="bottom" )
    plt.text(i + 0.2, error_list_solcast[i], round(error_list_solcast[i], 1), ha="center", va="bottom")

plt.title("Fehler der Temperatur-Vorhersagen von Solcast und DWD für Juni 2021 ")
plt.xticks(xpos, error_list_names)
plt.ylabel("Temperatur in ºC")
plt.legend()

plt.subplot(2,1,2)
xpos= np.arange(len(error_list_names_relative))

plt.bar(xpos-0.2, error_list_dwd_relative, width=0.4, label="dwd", color="blue")
plt.bar(xpos+0.2, error_list_solcast_relative, width=0.4, label="solcast", color="orange")
for i in range(len(error_list_names_relative)):
    plt.text(i-0.2, error_list_dwd_relative[i], round(error_list_dwd_relative[i], 2), ha="center", va="bottom" )
    plt.text(i + 0.2, error_list_solcast_relative[i], round(error_list_solcast_relative[i], 2), ha="center", va="bottom")
plt.title("Relative Fehler der Temperatur-Vorhersagen von Solcast und DWD für Juni 2021")
plt.xticks(xpos, error_list_names_relative)
plt.ylabel("")
plt.legend()

plt.tight_layout()
plt.show()