import pandas as pd
import matplotlib.pyplot as plt
import functions as fn
import numpy as np
import seaborn as sns

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

result = fn.concat_2_dataframes(result_forecast, result_actuals)

result["delta"] = result["Ghi"] - result["Ghi_for"]
result["delta_absolute"] = abs(result["Ghi"] - result["Ghi_for"])
result["clear_sky_index_for"] = 1 - (result["cloud_opacity_for"]/100)
result["clear_sky_index"] = 1 - (result["cloud_opacity"]/100)
result["delta_relative"] = result["delta"] / result["Ghi"]
number_of_datapairs_unequal_to_0 = result["delta_relative"].count()
result["cos_theta"] = np.cos(np.deg2rad(result["Zenith"]))
result["k*-grouped"] = round(result["clear_sky_index_for"]/10, 2) *10
result["cos_theta_grouped"] = round(result["cos_theta"]/10, 2) *10

result = result.drop(result[result.cos_theta < 0].index)

prueba = result.groupby(["k*-grouped","cos_theta_grouped"], as_index=False).mean()
prob = result.groupby("k*-grouped").cos_theta_grouped.value_counts().unstack()
print(prueba)
print(prob)
sns.heatmap(prob)
plt.show()

plt.scatter(result["cos_theta"], result["clear_sky_index_for"], s=300, c = result["delta"], cmap="RdYlGn", edgecolors="black", linewidths=0.5, alpha=0.75)
cbar = plt.colorbar()
cbar.set_label("Bias in W/m**2")
plt.clim(-100, 100)
plt.title("Delta in Abhängigkeit von clear sky index forecast un Position der Sonne")
plt.xlabel("cos(Theta)")
plt.ylabel("Clear sky index forecast")
plt.show()

plt.scatter(result["cos_theta"], result["clear_sky_index"], s=200,c = result["delta"], cmap="RdYlGn", edgecolors="black", linewidths=0.5, alpha=0.75)
cbar = plt.colorbar()
cbar.set_label("Absolute delta")
plt.clim(-100, 100)
plt.title("Delta in Abhängigkeit von Clear sky index un Position der Sonne")
plt.xlabel("cos(Theta)")
plt.ylabel("Clear sky index")
plt.show()