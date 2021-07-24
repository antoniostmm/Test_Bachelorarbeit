import pandas as pd
import functions as fn
import matplotlib.pyplot as plt
import numpy as np
import errors as er

dir_a = "./Solcast/SolarRadiation/EstimatedActuals/GetWeatherSiteEstimatedActuals_"
dir_f = "./Solcast/SolarRadiation/Forecasts/GetWeatherSiteForecast_"

list_df_actuals = []
for i in range(1,32):
    try:
        list_df_actuals.append(fn.tuning_df_solcast(pd.read_csv(dir_a + str(i).zfill(2) + "_06.csv")))
    except: continue

list_df_forecast = []
for i in range(1,31):
    try:
        list_df_forecast.append(fn.tuning_df_solcast(pd.read_csv(dir_f + str(i).zfill(2) + "_06.csv")))
    except: continue

list_df_actuals.reverse()

historical = pd.read_csv("Solcast/Historical/Solcast_Juni_actuals_30M.csv")
historical = fn.tuning_df_solcast(historical)

result_actuals = pd.concat(list_df_actuals, axis=0, join="inner")
result_actuals = result_actuals.drop_duplicates()

result_forecast = pd.concat(list_df_forecast, axis= 0 , join ="inner")
result_forecast = result_forecast.drop_duplicates(subset= "period_end", keep= "last")

result_forecast_not_rolling = pd.concat(list_df_forecast, axis= 0 , join ="inner")
result_forecast_not_rolling = result_forecast_not_rolling.drop_duplicates(subset= "period_end", keep= "first")

result_pre = fn.concat_2_dataframes(result_forecast_not_rolling, result_actuals)
error_list_pre = er.get_errors(result_pre)
error_list_pre_relative = er.get_errors_relative(result_pre)

result = fn.concat_2_dataframes(result_forecast, result_actuals)


result_solcast = fn.concat_2_dataframes(result_forecast, historical)


result["delta"] = result["Ghi_for"] - result["Ghi"]
result["delta_absolute"] = abs(result["delta"])
result["clear_sky_index_for"] = 1 - (result["cloud_opacity_for"]/100)
result["clear_sky_index"] = 1 - (result["cloud_opacity"]/100)
result["delta_clear_sky_index"] = result["clear_sky_index_for"] - result["clear_sky_index"]
result["delta_clear_sky_index_absolut"] = abs(result["delta_clear_sky_index"])

result["cos_theta"] = np.cos(np.deg2rad(result["Zenith"]))

error_list_names = ["RMSE", "MBE","MAE", "SD"]
error_list_names_relative = ["rRMSE", "rMBE","rMAE", "rSD", "R_2"]

error_list_def = er.get_errors(result)
error_list_def_relative = er.get_errors_relative(result)




plt.plot(result.index, result["Ghi"], label="estimated actuals", c="red")
plt.plot(result_solcast.index, result_solcast["Ghi"], label="historical", c= "blue")
plt.plot(result.index, result["Ghi_for"], label="forecast", color="green")
plt.legend()
plt.show()


plt.style.use("seaborn-whitegrid")
plt.subplot(2,1,1)
xpos= np.arange(len(error_list_names))

plt.bar(xpos-0.2, error_list_pre,width=0.4, label="stationary", color="red")
plt.bar(xpos+0.2, error_list_def, width=0.4, label="rolling_24h", color="green")
for i in range(len(error_list_names)):
    plt.text(i-0.2, error_list_pre[i], int(round(error_list_pre[i], 0)), ha="center", va="bottom" )
    plt.text(i + 0.2, error_list_def[i], int(round(error_list_def[i], 0)), ha="center", va="bottom")

plt.title("Fehler der Vorhersagen")
plt.xticks(xpos, error_list_names)
plt.ylabel("Ghi")
plt.legend()

plt.subplot(2,1,2)
xpos= np.arange(len(error_list_names_relative))

plt.bar(xpos-0.2, error_list_pre_relative,width=0.4, label="stationary", color="red")
plt.bar(xpos+0.2, error_list_def_relative, width=0.4, label="rolling_24h", color="green")
for i in range(len(error_list_names_relative)):
    plt.text(i-0.2, error_list_pre_relative[i], round(error_list_pre_relative[i], 2), ha="center", va="bottom" )
    plt.text(i + 0.2, error_list_def_relative[i], round(error_list_def_relative[i], 2), ha="center", va="bottom")
plt.title("Relative Fehler der Vorhersagen")
plt.xticks(xpos, error_list_names_relative)
plt.ylabel("")
plt.legend()

plt.tight_layout()
plt.show()

plt.plot(result.index, result["Ghi90"], color="lightgrey")
plt.plot(result.index, result["Ghi10"], color="lightgrey")
plt.fill_between(result.index, result["Ghi90"], result["Ghi10"], color="lightgrey", label="Ghi90-Ghi10")
plt.plot(result.index, result["Ghi_for"], label="forecast", color="red")
plt.plot(result.index, result["Ghi"], label="actual", color="blue")

plt.title("Global solar irradiance for June with rolling horizon of 24h")
plt.ylabel("Ghi")
plt.legend()
plt.show()



result_days = result.drop(result[result.cos_theta < 0].index)


error_list_days = er.get_errors(result_days)
error_list_days_relative = er.get_errors_relative(result_days)


plt.style.use("seaborn-whitegrid")
plt.subplot(2,1,1)
xpos= np.arange(len(error_list_names))

plt.bar(xpos-0.2, error_list_def,width=0.4, label="mit night time", color="red")
plt.bar(xpos+0.2, error_list_days, width=0.4, label="ohne night time", color="green")
for i in range(len(error_list_names)):
    plt.text(i-0.2, error_list_def[i], int(round(error_list_def[i], 0)), ha="center", va="bottom" )
    plt.text(i + 0.2, error_list_days[i], int(round(error_list_days[i], 0)), ha="center", va="bottom")

plt.title("Fehler der Vorhersagen")
plt.xticks(xpos, error_list_names)
plt.ylabel("Ghi")
plt.legend()

plt.subplot(2,1,2)
xpos= np.arange(len(error_list_names_relative))

plt.bar(xpos-0.2, error_list_def_relative,width=0.4, label="mit night time", color="red")
plt.bar(xpos+0.2, error_list_days_relative, width=0.4, label="ohne night time", color="green")
for i in range(len(error_list_names_relative)):
    plt.text(i-0.2, error_list_def_relative[i], round(error_list_def_relative[i], 2), ha="center", va="bottom" )
    plt.text(i + 0.2, error_list_days_relative[i], round(error_list_days_relative[i], 2), ha="center", va="bottom")
plt.title("Relative Fehler der Vorhersagen")
plt.xticks(xpos, error_list_names_relative)
plt.ylabel("")
plt.legend()


plt.tight_layout()
plt.show()
