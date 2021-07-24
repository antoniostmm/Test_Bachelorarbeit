import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import functions as fn
import errors as er

'''
Vergleich zwischen den Vorhersagen und den Messwerten von DWD und Solcast für Juni 2021.
Dwd Vorhersagen mit 24h-Auflösung

Plottet Messwerte und Vorhersagen von beiden Datensätze für den Monat Juni 2021. (Auf compare_DWD_historical_month setzen),
sonst werden alle Vorhersagen verglichen.
Fehleranalyse für:
 - Ganz Juni mit und ohne Nachtwerte 
 - Um beide Datensätze vergleichen zu können: Zeitperiode 09.06 -30.06
 - Temperatur 

Für den Juni 2021 sind ein paar Dinge zu beachten.

1) Die Solcast Daten sind nur ungefähr 24h-Stunden Vorhersagen. Die Vorhersagen werden jeweils morgens einmal manuell
   gespeichert. Die Uhrzeit für die unterschiedlichen Vorhersagen ändert sich von Tag zu Tag.

2) Die Solcast Vorhersagen sind erst ab den 04.06 vorhanden, wobei am 08.06 keine Vorhersage am Morgen gespeichert wurde.
   D.h., dass erst ab den 09.06 komplette 24h-Vorhersagen vorhanden sind.

3) Die Messwerten sind zwar für den gleichen Zeitbereich, stammen aber nicht von der gleichen Station bzw. von den
   gleichen Koordinaten. D.h. dass die Messwerten nicht unbedingt vergleichbar sind.

4) Sowohl die Solcast-Messdaten als auch die Solcast-Vorhersagen sind in 30-minutiger Auflösung gegeben. Hingegen sind
   die DWD-Vorhersagen in stündlicher Auflösung gegeben und die Messdaten von 10-minutiger in stündlicher Auflösung
   umgerechnet. 

5) Für den Temperaturvergleich: Die Solcast-Vorhersagen schätzen die Temperatur nur in ganzen Zahlen während die DWD-Daten
   und die Solcast-Messdaten mit einer Nachkommastelle angegeben wird.
   
Erkenntnisse:
1) Ergebnisse sind knaper als erwartet: Für den ganzen Monat und ohne berücksichtigung der Defizite von Solcast-Vorhersagen, 
   scheint die DWD-Vorhersage besser zu sein.
   
2) Solcast-Vorhersagen unterschätzen die Einstrahlung (negativer MBE) (kann an der fehlenden Vorhersagen vom 08.06 liegen)

3) Für die Zeitperiode 09.06-30.06 übertrifft die Solcast-Vorhersage die vom DWD, woraus sich erschliessen lässt, dass bei
   gleichen Randbedingungen die Solcast_Vorhersage besser ist.
   
4) Wie üblich: Bei Auslassung der Nachtwerte werden die absoluten Fehler größer,da die triviale Vorhersage von
   Nachtwerten den absoluten Fehler positiv beeinflusst. Ganz im Gegenteil werden die relative Fehler kleiner,
   da der durchschittliche Normalisierungswert größer wird.
'''

dir_a = "./Solcast/SolarRadiation/EstimatedActuals/GetWeatherSiteEstimatedActuals_"
dir_f = "./Solcast/SolarRadiation/Forecasts/GetWeatherSiteForecast_"

error_list_names = ["RMSE", "MBE","MAE", "SD"]
error_list_names_relative = ["rRMSE", "rMBE","rMAE", "rSD", "R_2"]

list_df_actuals = []
for i in range(1,29):
    try:
        list_df_actuals.append(fn.tuning_df_solcast(pd.read_csv(dir_a + str(i).zfill(2) + "_06.csv")))
    except: continue

list_df_forecast = []
for i in range(9,30):
    try:
        list_df_forecast.append(fn.tuning_df_solcast(pd.read_csv(dir_f + str(i).zfill(2) + "_06.csv")))
    except: continue

list_df_actuals.reverse()

result_actuals = pd.concat(list_df_actuals, axis=0, join="inner")
result_actuals = result_actuals.drop_duplicates()



historical = pd.read_csv("Solcast/Historical/Solcast_Juni_actuals_30M.csv")
historical = fn.tuning_df_solcast(historical)


result_forecast = pd.concat(list_df_forecast, axis= 0 , join ="inner")
result_forecast = result_forecast.drop_duplicates(subset= "period_end", keep= "last")

result_solcast = fn.concat_2_dataframes(result_forecast, result_actuals)

error_list_solcast = er.get_errors(result_solcast)
error_list_solcast_relative = er.get_errors_relative(result_solcast)

result_solcast_days = result_solcast.drop(result_solcast[result_solcast.Ghi < 1].index)

error_list_solcast_days = er.get_errors(result_solcast_days)
error_list_solcast_days_relative = er.get_errors_relative(result_solcast_days)






base_dir_rec = "./DWD/Recent/"

df_DWD_actual_recent_2021 = pd.read_csv(base_dir_rec + "2021/dwd_actual_recent_2021.csv")

df_DWD_recent_gefiltert_2021 = fn.filter_dataframe_GHI(df_DWD_actual_recent_2021)
df_actual_recent_2021 = fn.tuning_DWD(df_DWD_recent_gefiltert_2021)

result_dwd = fn.compare_DWD_historical_month("2021_06", 24, df_actual_recent_2021 )


error_list_dwd = er.get_errors(result_dwd, "Ghi_hf", "Ghi_hourly")
error_list_dwd_relative = er.get_errors_relative(result_dwd, "Ghi_hf", "Ghi_hourly")

result_dwd_days = result_dwd.drop(result_dwd[result_dwd.Ghi_hourly == 0].index)

error_list_dwd_days = er.get_errors(result_dwd_days, "Ghi_hf", "Ghi_hourly")
error_list_dwd_days_relative = er.get_errors_relative(result_dwd_days, "Ghi_hf", "Ghi_hourly")





plt.style.use("seaborn-whitegrid")
#plt.plot(result_dwd.index, result_dwd["Ghi_hourly"], label="DWD Messdaten", c="blue")
#plt.plot(result_solcast.index, result_solcast["Ghi"], label="Solcast Messdaten", c="red")
plt.plot(result_dwd.index, result_dwd["Ghi_hf"], label="DWD Vorhersage", c="lightblue")
#plt.plot(result_solcast.index, result_solcast["Ghi_for"], label="Solcast Vorhersage", c="lightsalmon")
plt.legend(prop = {"size":15})
plt.ylabel("Ghi [W/m**2]", size=25)
plt.xticks(fontsize = 19)
plt.yticks(fontsize = 19)
plt.title("Vergleich Globalstrahlung Solcast und DWD für Juni ", size=30)
plt.show()








plt.style.use("seaborn-whitegrid")
plt.subplot(2,1,1)
xpos= np.arange(len(error_list_names))

plt.bar(xpos-0.2, error_list_dwd_days,width=0.4, label="dwd", color="blue")
plt.bar(xpos+0.2, error_list_solcast_days, width=0.4, label="solcast", color="orange")
for i in range(len(error_list_names)):
    plt.text(i-0.2, error_list_dwd_days[i], int(round(error_list_dwd_days[i], 0)), ha="center", va="bottom" )
    plt.text(i + 0.2, error_list_solcast_days[i], int(round(error_list_solcast_days[i], 0)), ha="center", va="bottom")

plt.title("Fehler der Vorhersagen von Solcast und DWD für Juni 2021 (only days)")
plt.xticks(xpos, error_list_names)
plt.ylabel("Ghi")
plt.legend()

plt.subplot(2,1,2)
xpos= np.arange(len(error_list_names_relative))

plt.bar(xpos-0.2, error_list_dwd_days_relative, width=0.4, label="dwd", color="blue")
plt.bar(xpos+0.2, error_list_solcast_days_relative, width=0.4, label="solcast", color="orange")
for i in range(len(error_list_names_relative)):
    plt.text(i-0.2, error_list_dwd_days_relative[i], round(error_list_dwd_days_relative[i], 2), ha="center", va="bottom" )
    plt.text(i + 0.2, error_list_solcast_days_relative[i], round(error_list_solcast_days_relative[i], 2), ha="center", va="bottom")
plt.title("Relative Fehler der Vorhersagen von Solcast und DWD für Juni 2021 (only days)")
plt.xticks(xpos, error_list_names_relative)
plt.ylabel("")
plt.legend()

plt.tight_layout()
plt.show()


