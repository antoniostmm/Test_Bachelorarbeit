import pandas as pd
import matplotlib.pyplot as plt
import functions as fn
import errors as er
import numpy as np
from scipy import optimize
pd.options.mode.chained_assignment = None


base_dir_rec = "./DWD/Recent/"
df_DWD_actual_recent_2021 = pd.read_csv(base_dir_rec + "2021/dwd_actual_recent_2021.csv")
df_DWD_actual_recent_2020 = pd.read_csv(base_dir_rec + "2020/dwd_actual_recent_2020.csv")

df_DWD_recent_gefiltert_2021 = fn.filter_dataframe_GHI(df_DWD_actual_recent_2021)
df_actual_recent_2021 = fn.tuning_DWD(df_DWD_recent_gefiltert_2021)

df_DWD_recent_gefiltert_2020 = fn.filter_dataframe_GHI(df_DWD_actual_recent_2020)
df_actual_recent_2020 = fn.tuning_DWD(df_DWD_recent_gefiltert_2020)


# result_day = fn.compare_DWD_historical_month("2021_05",1,df_actual_recent_2021)
#
# result = result_day.drop(result_day[result_day.Ghi_hourly == 0].index)
#
# result["delta"] = result["Ghi_hf"] - result["Ghi_hourly"]
# result["delta_rounded"] = round((result["delta"]/5)) *5
# result_delta = result.groupby(["delta_rounded"]).count()
#
# print(result_delta)
#
# plt.bar(result_delta.index, result_delta["delta"], width=4, color= "blue")
# plt.title("Verteilungsfunktion der Abweichung für einen Monat")
# plt.xlabel("Abweicbhung in 5 W/m**2 -Schrtitte")
# plt.ylabel("Prozent %")
# plt.show()



result = fn.compare_every_historical_forecast("2021_05", 16, df_actual_recent_2021 )
result = fn.adding_zenith_angle(result)
print(result)
result["delta_rounded"] = round((result["delta"]/5)) *5
result_day = result.drop(result[result.Ghi_hourly == 0].index)


result_delta = result_day.groupby(["delta_rounded"]).count()

plt.scatter(result_delta.index, result_delta["delta"], color= "blue")
plt.title("Verteilungsfunktion der Abweichung für Mai mit 16h-Vorhersagehorizont")
plt.xlabel("Abweicbhung in 5 W/m**2 -Schrite")
plt.ylabel("Anzahl")
plt.show()


def gaussian_f(X, a, b, c):
    y = a * np.exp(-0.5 * ((X-b)/c)**2)
    return y

popt, pcov = optimize.curve_fit(objective, x, y)

plt.bar(result_delta.index, result_delta["delta"], width=4, color= "blue")
plt.title("Verteilungsfunktion der Abweichung für Januar mit 16h-Vorhersagehorizont")
plt.xlabel("Abweicbhung in 5 W/m**2 -Schrite")
plt.ylabel("Anzahl")
plt.show()

plt.subplot(2,1,1)
plt.scatter(result["Ghi_hourly"], result["delta"], c= result["zenith_angle"],cmap="viridis_r", alpha=0.5)
plt.title("Verteilungsfunktion der Abweichung für Mai mit 16h-Vorhersagehorizont")
plt.xlabel("Ghi_gemessen")
plt.ylabel("Abweichung")
cbar = plt.colorbar()
cbar.set_label("Zenith angle")
plt.clim(30, 90)


plt.subplot(2,1,2)
plt.scatter(result["Ghi_hf"], result["delta"], c= result["zenith_angle"],cmap="viridis_r", alpha=0.5)
plt.title("Verteilungsfunktion der Abweichung für Mai mit 16h-Vorhersagehorizont")
plt.xlabel("Ghi_forecast")
plt.ylabel("Abweichung")
cbar = plt.colorbar()
cbar.set_label("Zenith angle")
plt.clim(30, 90)

plt.tight_layout()
plt.show()

plt.scatter(result["zenith_angle"], result["delta"], c= result["zenith_angle"],cmap="viridis_r", alpha=0.7)
plt.title("Verteilungsfunktion der Abweichung in Abhängigkeit vom Zenith_angle für Mai mit 16h-Vorhersagehorizont")
plt.xlabel("Zenith angle")
plt.ylabel("Abweichung")
plt.clim(30, 90)
plt.show()

# error_list_names = ["RMSE", "MBE","MAE", "SD"]
# error_list_names_relative = ["rRMSE", "rMBE","rMAE", "rSD", "R_2"]
#
# error_list = er.get_errors(result, "Ghi_hf", "Ghi_hourly")
# error_list_day = er.get_errors(result_day, "Ghi_hf", "Ghi_hourly")
#
# error_list_relative = er.get_errors_relative(result, "Ghi_hf", "Ghi_hourly")
# error_list_day_relative = er.get_errors_relative(result_day, "Ghi_hf", "Ghi_hourly")
#
# plt.style.use("seaborn-whitegrid")
# plt.subplot(2,1,1)
# xpos= np.arange(len(error_list_names))
#
# plt.bar(xpos-0.2, error_list,width=0.4, label="all data", color="red")
# plt.bar(xpos+0.2, error_list_day, width=0.4, label="only day", color="green")
# for i in range(len(error_list_names)):
#     plt.text(i - 0.2, error_list[i], int(round(error_list[i], 0)), ha="center", va="bottom")
#     plt.text(i + 0.2, error_list_day[i], int(round(error_list_day[i], 0)), ha="center", va="bottom")
#
# plt.title("Fehler der Vorhersagen mit und ohne nighttime für Januar mit 16h-Vorhersagehorizont")
# plt.xticks(xpos, error_list_names)
# plt.ylabel("Ghi")
# plt.legend()
#
# plt.subplot(2,1,2)
# xpos= np.arange(len(error_list_names_relative))
# plt.bar(xpos-0.2, error_list_relative, width=0.4, label="all data", color="red")
# plt.bar(xpos+0.2, error_list_day_relative, width=0.4, label="only day", color="green")
# for i in range(len(error_list_names_relative)):
#     plt.text(i - 0.2, error_list_relative[i], round(error_list_relative[i], 2), ha="center", va="bottom")
#     plt.text(i + 0.2, error_list_day_relative[i], round(error_list_day_relative[i], 2), ha="center", va="bottom")
#
# plt.title("Relative Fehler der Vorhersagen mit und ohne nighttime für Januar mit 16h-Vorhersagehorizont")
# plt.xticks(xpos, error_list_names_relative)
# plt.ylabel("-")
#
# plt.legend()
# plt.show()





