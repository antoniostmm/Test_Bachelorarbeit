import functions as fn
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

dir_f = "./Solcast/SolarRadiation/Forecasts/GetWeatherSiteForecast_"
df_forecast_10 = fn.tuning_df_solcast(pd.read_csv(dir_f + "10_06" + ".csv"))
df_forecast_11 = fn.tuning_df_solcast(pd.read_csv(dir_f + "11_06" + ".csv"))
df_forecast_12 = fn.tuning_df_solcast(pd.read_csv(dir_f + "12_06" + ".csv"))
df_forecast_13 = fn.tuning_df_solcast(pd.read_csv(dir_f + "13_06" + ".csv"))
df_forecast_14 = fn.tuning_df_solcast(pd.read_csv(dir_f + "14_06" + ".csv"))
df_forecast_15 = fn.tuning_df_solcast(pd.read_csv(dir_f + "15_06" + ".csv"))
df_forecast_16 = fn.tuning_df_solcast(pd.read_csv(dir_f + "16_06" + ".csv"))

df_actuals_17 = pd.read_csv("./Solcast/SolarRadiation/EstimatedActuals/GetWeatherSiteEstimatedActuals_17_06.csv")
df_actuals_17 = fn.tuning_df_solcast(df_actuals_17)

df_forecast_10.update(df_forecast_11)
df_forecast_10.update(df_forecast_12)
df_forecast_10.update(df_forecast_13)
df_forecast_10.update(df_forecast_14)
df_forecast_10.update(df_forecast_15)
df_forecast_10.update(df_forecast_16)

result = fn.concat_2_dataframes(df_forecast_10,df_actuals_17)
result["counter"] = 1
result["delta"] = result["Ghi"] - result["Ghi_for"]
result["absolut_delta"] = abs(result["Ghi"] - result["Ghi_for"])
result["delta_rounded"] = round((result["delta"]/5)) *5
result["Ghi_rounded"] = round(result["Ghi"], -1)
result["relative_delta"] = result["delta"] / result["Ghi"]
#result_min = result.groupby(['Ghi_rounded']).min()
#result_max = result.groupby(['Ghi_rounded']).max()
result_mean = result.groupby(['Ghi_rounded']).mean()
number_of_datapairs_unequal_to_0 = result["relative_delta"].count()


result_delta = result.groupby(["delta_rounded"]).count()

result_delta["percent"] = result_delta["relative_delta"]/number_of_datapairs_unequal_to_0



#plt.bar(result_delta.index, result_delta["relative_delta"], width=4, color= "blue")
plt.bar(result_delta.index, result_delta["percent"], width=4, color= "blue")
plt.title("Verteilungsfunktion für eine Woche")
plt.xlabel("Delta in 5 W/m**2 -steps")
plt.ylabel("Percentage amount")
plt.show()

diagon = [0,900]

plt.scatter(result["Ghi"], result["Ghi_for"], c = result["delta"], cmap="RdYlGn", edgecolors="black", linewidths=0.5, alpha=0.75)
plt.plot(diagon,diagon)
cbar = plt.colorbar()
cbar.set_label("Absolute delta")
plt.clim(-100, 100)
plt.title("Vergleich Vorhersage mit Messdaten")
plt.xlabel("Gemessene Ghi in W/m**2")
plt.ylabel("Forecast Ghi in W/m**2")
plt.show()

plt.subplot(2,1,1)
plt.scatter(result_mean.index, result_mean["delta"], edgecolors="black", linewidths=0.5, alpha=0.75)
plt.title("Verteilungsfunktion für die Abweichung für die Woche 10-17.06")
plt.xlabel("Ghi")
plt.ylabel("Durc Abw")

plt.subplot(2,1,2)
#plt.scatter(result_min.index, result_min["delta"], edgecolors="black", linewidths=0.5, alpha=0.75)
plt.title("Maximale/Minimale Abweichung für die Woche 10-17.06")
plt.xlabel("Ghi")
plt.ylabel("Ab")

plt.tight_layout()
plt.show()

plt.subplot(2,1,1)
#plt.scatter(result_max.index, result_max["absolut_delta"], edgecolors="black", linewidths=0.5, alpha=0.75)
plt.title("Durchscnittliche absolute Abweichung für die Woche 10-17.06")
plt.xlabel("Ghi")
plt.ylabel("A max Abwe")

plt.subplot(2,1,2)
plt.scatter(result_mean.index, result_mean["absolut_delta"], edgecolors="black", linewidths=0.5, alpha=0.75)
plt.title("Maximale absolute Abweichung für die Woche 10-17.06")
plt.xlabel("Ghi")
plt.ylabel("A du Abwe")

plt.tight_layout()
plt.show()

