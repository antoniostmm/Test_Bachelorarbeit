import pandas as pd
import matplotlib.pyplot as plt
import functions as fn
import numpy as np

dir_f = "./Solcast/SolarRadiation/Forecasts/GetWeatherSiteForecast_"
dir_a = "./Solcast/SolarRadiation/EstimatedActuals/GetWeatherSiteEstimatedActuals_"

list_df_actuals = []
for i in range(1,30):
    try:
        list_df_actuals.append(fn.tuning_df_solcast(pd.read_csv(dir_a + str(i).zfill(2) + "_06.csv")))
    except: continue

list_df_forecast = []
for i in range(1,30):
    try:
        list_df_forecast.append(fn.tuning_df_solcast(pd.read_csv(dir_f + str(i).zfill(2) + "_06.csv")))
    except: continue

list_df_actuals.reverse()

result_actuals = pd.concat(list_df_actuals, axis=0, join="inner")
result_actuals = result_actuals.drop_duplicates()

result_forecast = pd.concat(list_df_forecast, axis= 0 , join ="inner")
result_forecast = result_forecast.drop_duplicates(subset= "period_end", keep= "last")

total_rounded = pd.DataFrame()
total_scatter = pd.DataFrame()

result = fn.concat_2_dataframes(result_forecast, result_actuals)

result["delta"] = result["Ghi"] - result["Ghi_for"]
result["delta_absolute"] = abs(result["Ghi"] - result["Ghi_for"])
result["Ghi_rounded"] = round(result["Ghi"], -1)
result["delta_relative"] = result["delta"] / result["Ghi"]
result["delta_rounded"] = round((result["delta"]/5)) *5
number_of_datapairs_unequal_to_0 = result["delta_relative"].count()
result["cos_theta"] = np.cos(np.deg2rad(result["Zenith"]))
#result_mean = result.groupby(['Ghi_rounded']).mean()
#total_rounded = total_rounded.append(result.groupby(['Ghi_rounded']).mean())

result_delta = result.groupby(["delta_rounded"]).count()
result_delta["percent"] = result_delta["delta_relative"]/number_of_datapairs_unequal_to_0


plt.bar(result_delta.index, result_delta["percent"], width=4, color= "blue")
plt.title("Verteilungsfunktion der Abweichung für einen Monat")
plt.xlabel("Abweicbhung in 5 W/m**2 -Schrtitte")
plt.ylabel("Prozent %")
plt.show()

diagon = [0,900]
plt.scatter(result["Ghi"], result["Ghi_for"], c = result["delta"], cmap="RdYlGn", edgecolors="black", linewidths=0.5, alpha=0.75)
plt.plot(diagon,diagon)
cbar = plt.colorbar()
cbar.set_label("Delta zwischen Forecast und Messdaten")
plt.clim(-100, 100)

plt.title("Vergleich Vorhersage mit Messdaten")
plt.xlabel("Gemessene Ghi in W/m**2")
plt.ylabel("Forecast Ghi in W/m**2")
plt.show()





result["delta_cloud"] = result["cloud_opacity"] - result["cloud_opacity_for"]
diagon2 = [0,100]
plt.scatter(result["cloud_opacity"], result["cloud_opacity_for"], c = result["delta_cloud"], cmap="RdYlGn", edgecolors="black", linewidths=0.5, alpha=0.75)
plt.plot(diagon2,diagon2)
cbar = plt.colorbar()
cbar.set_label("Delta zwischen Forecast und Messdaten")
plt.clim(-50, 50)

plt.title("Vergleich Vorhersage mit Messdaten für Cloud Opacity")
plt.xlabel("Gemessene Cloud Opacity")
plt.ylabel("Forecast Cloud Opacity")
plt.show()