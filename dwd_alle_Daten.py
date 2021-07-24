import pandas as pd
import functions as fn
import matplotlib.pyplot as plt
import numpy as np
import errors as er

pd.options.mode.chained_assignment = None

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

result_06 = fn.compare_every_historical_forecast("2021_06", 48, df_actual_recent_2021)
result_05 = fn.compare_every_historical_forecast("2021_05", 48, df_actual_recent_2021 )
result_04 = fn.compare_every_historical_forecast("2021_04", 48, df_actual_recent_2021 )
result_03 = fn.compare_every_historical_forecast("2021_03", 48, df_actual_recent_2021 )
result_02 = fn.compare_every_historical_forecast("2021_02", 48, df_actual_recent_2021 )
result_01 = fn.compare_every_historical_forecast("2021_01", 48, df_actual_recent_2021 )
result_12 = fn.compare_every_historical_forecast("2020_12", 48, df_actual_recent_2020 )
result_11 = fn.compare_every_historical_forecast("2020_11", 48, df_actual_recent_2020 )
result_10 = fn.compare_every_historical_forecast("2020_10", 48, df_actual_recent_2020 )

result = pd.concat([result_01,result_02,result_03,result_04,result_05,result_06, result_10, result_11, result_12], axis=0)
result_day = result.drop(result[result.Ghi_hourly == 0].index)


error_list_names = ["RMSE", "MBE","MAE", "SD"]
error_list_names_relative = ["rRMSE", "rMBE","rMAE", "rSD", "R_2"]

error_list = er.get_errors(result, "Ghi_hf", "Ghi_hourly")
error_list_day = er.get_errors(result_day, "Ghi_hf", "Ghi_hourly")

error_list_relative = er.get_errors_relative(result, "Ghi_hf", "Ghi_hourly")
error_list_day_relative = er.get_errors_relative(result_day, "Ghi_hf", "Ghi_hourly")

plt.style.use("seaborn-whitegrid")
plt.subplot(2,1,1)
xpos= np.arange(len(error_list_names))


plt.bar(xpos-0.2, error_list,width=0.4, label="all data", color="red")
plt.bar(xpos+0.2, error_list_day, width=0.4, label="only day", color="green")
for i in range(len(error_list_names)):
    plt.text(i - 0.2, error_list[i], int(round(error_list[i], 0)), ha="center", va="bottom")
    plt.text(i + 0.2, error_list_day[i], int(round(error_list_day[i], 0)), ha="center", va="bottom")

plt.title("Fehler der Vorhersagen mit und ohne nighttime für alle Daten mit 48h-Vorhersagehorizont")
plt.xticks(xpos, error_list_names)
plt.ylabel("Ghi")
plt.legend()

plt.subplot(2,1,2)
xpos= np.arange(len(error_list_names_relative))
plt.bar(xpos-0.2, error_list_relative, width=0.4, label="all data", color="red")
plt.bar(xpos+0.2, error_list_day_relative, width=0.4, label="only day", color="green")
for i in range(len(error_list_names_relative)):
    plt.text(i - 0.2, error_list_relative[i], round(error_list_relative[i], 2), ha="center", va="bottom")
    plt.text(i + 0.2, error_list_day_relative[i], round(error_list_day_relative[i], 2), ha="center", va="bottom")

plt.title("Relative Fehler der Vorhersagen mit und ohne nighttime für alle Daten mit 48h-Vorhersagehorizont")
plt.xticks(xpos, error_list_names_relative)
plt.ylabel("-")

plt.legend()
plt.show()


diagon = [0,900]
plt.scatter(result_day["Ghi_hf"], result_day["Ghi_hourly"],c = result_day["N"], cmap="viridis", edgecolors="black", linewidths=0.5, alpha=0.75)
plt.plot(diagon,diagon)
cbar = plt.colorbar()
cbar.set_label("Bedeckungsgrad N")
plt.clim(0, 100)

plt.title("Vergleich Vorhersage mit Messdaten")
plt.xlabel("Forecast Ghi in W/m**2")
plt.ylabel("Gemessene Ghi in W/m**2")
plt.show()

diagon = [0,900]
plt.scatter(result_day["Ghi_hf"], result_day["Ghi_hourly"],c = result_day["Neff"], cmap="viridis", edgecolors="black", linewidths=0.5, alpha=0.75)
plt.plot(diagon,diagon)
cbar = plt.colorbar()
cbar.set_label("effektiver Bedeckungsgrad N_eff")
plt.clim(0, 100)

plt.title("Vergleich Vorhersage mit Messdaten")
plt.xlabel("Forecast Ghi in W/m**2")
plt.ylabel("Gemessene Ghi in W/m**2")
plt.show()