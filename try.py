import pandas as pd
import functions as fn
import matplotlib.pyplot as plt
import numpy as np
import errors as er

dir_a = "./Solcast/SolarRadiation/EstimatedActuals/GetWeatherSiteEstimatedActuals_"
dir_f = "./Solcast/SolarRadiation/Forecasts/GetWeatherSiteForecast_"

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

result_forecast_not_rolling = pd.concat(list_df_forecast, axis= 0 , join ="inner")
result_forecast_not_rolling = result_forecast_not_rolling.drop_duplicates(subset= "period_end", keep= "first")

result = fn.concat_2_dataframes(result_forecast, result_actuals)

#Neue Spalten einfügen und Nachtwerte entfernen
result["delta"] = result["Ghi_for"] - result["Ghi"]
result["delta_absolute"] = abs(result["delta"])
result["clear_sky_index_for"] = 1 - (result["cloud_opacity_for"]/100)
result["clear_sky_index"] = 1 - (result["cloud_opacity"]/100)
result["clear_sky_index_for_rounded"] = round((result["clear_sky_index_for"]/5), 2) *5
result["clear_sky_index_delta"] = result["clear_sky_index_for"] - result["clear_sky_index"]
result["clear_sky_index_delta_abs"] = abs(result["clear_sky_index_delta"])
result["delta_squared"] = result["delta"]**2
result["counter"] = 1
result["cos_theta"] = np.cos(np.deg2rad(result["Zenith"]))

result = result.drop(result[result.cos_theta < 0].index)

#Dataframe bilden um RMSE in Abhängigkeit vom k*-index darzustellen
result_rmse = result.groupby(["clear_sky_index_for_rounded"]).sum()
result_rmse["rmse"] = (result_rmse["delta_squared"] / result_rmse["counter"])**0.5

result_rmse_not_rounded = result.groupby(["clear_sky_index_for"]).sum()
result_rmse_not_rounded["rmse"] = (result_rmse_not_rounded["delta_squared"] / result_rmse_not_rounded["counter"])**0.5

#Plot RMSE in Abhängigkeit vom k*-index für gruppierte und nicht gruppierte k*-indizes
plt.plot(result_rmse.index, result_rmse["rmse"], label="RMSE grouped in 0.05-steps", c="blue")
plt.plot(result_rmse_not_rounded.index, result_rmse_not_rounded["rmse"], label="RMSE not grouped", c="gray", alpha= 0.5)
plt.title("RMSE für unterschiedliche Bereiche des clear_sky_index_forecast im Juni")
plt.axvspan(0.8, 1, alpha=0.2, color='green', label="clear sky")
plt.axvspan(0.15, 0.35, alpha=0.2, color='red', label="overcast")
plt.xlabel("clear sky index forecast")
plt.ylabel("RMSE in W/m**2")
plt.legend()
plt.show()

#Definiere verschiedene Dataframes für unterschiedliche k*-index Bereiche
result_clear_sky = result.drop(result[result.clear_sky_index_for < 0.9].index)

result_overcast = result.drop(result[result.clear_sky_index > 0.3].index)

result_broken_cloud =  result.drop(result[result.clear_sky_index < 0.3].index)
result_broken_cloud = result_broken_cloud.drop(result_broken_cloud[result_broken_cloud.clear_sky_index > 0.9].index)

#Fehler für die unterschiedlichen k*-index Bereiche
error_list_names = ["RMSE", "MBE","MAE", "SD"]
error_list_names_relative = ["rRMSE", "rMBE","rMAE", "rSD", "R_2"]
error_list_clear = er.get_errors(result_clear_sky)
error_list_clear_relative = er.get_errors_relative(result_clear_sky)

error_list_overcast = er.get_errors(result_overcast)
error_list_overcast_relative = er.get_errors_relative(result_overcast)

error_list_broken = er.get_errors(result_broken_cloud)
error_list_broken_relative = er.get_errors_relative(result_broken_cloud)


plt.style.use("seaborn-whitegrid")
plt.subplot(2,1,1)
xpos= np.arange(len(error_list_names))

plt.bar(xpos, error_list_broken, width=0.3, label="broken", color="orange")
plt.bar(xpos+0.3, error_list_clear, width=0.3, label="clear", color="yellow")
plt.bar(xpos-0.3, error_list_overcast, width=0.3, label="overcast", color="red")

for i in range(len(error_list_names)):
    plt.text(i , error_list_broken[i], int(round(error_list_broken[i], 0)), ha="center", va="bottom" )
    plt.text(i - 0.3, error_list_overcast[i], int(round(error_list_overcast[i], 0)), ha="center", va="bottom")
    plt.text(i + 0.3, error_list_clear[i], int(round(error_list_clear[i], 0)), ha="center", va="bottom")
plt.title("Fehler der Vorhersagen")
plt.xticks(xpos, error_list_names)
plt.ylabel("Ghi")
plt.legend()


plt.subplot(2,1,2)
xpos= np.arange(len(error_list_names_relative))

plt.bar(xpos, error_list_broken_relative, width=0.3, label="broken", color="orange")
plt.bar(xpos+0.3, error_list_clear_relative, width=0.3, label="clear", color="yellow")
plt.bar(xpos-0.3, error_list_overcast_relative, width=0.3, label="overcast", color="red")
for i in range(len(error_list_names_relative)):
    plt.text(i , error_list_broken_relative[i], round(error_list_broken_relative[i], 2), ha="center", va="bottom" )
    plt.text(i - 0.3, error_list_overcast_relative[i], round(error_list_overcast_relative[i], 2), ha="center", va="bottom")
    plt.text(i + 0.3, error_list_clear_relative[i], round(error_list_clear_relative[i], 2), ha="center", va="bottom")
plt.title("Relative Fehler der Vorhersagen")
plt.xticks(xpos, error_list_names_relative)
plt.ylabel("%")
plt.legend()


plt.tight_layout()
plt.show()







