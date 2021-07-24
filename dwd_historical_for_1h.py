import pandas as pd
import numpy as np
import functions as fn
import errors as er
import matplotlib.pyplot as plt
pd.options.mode.chained_assignment = None

base_dir_rec = "./DWD/Recent/"

df_DWD_actual_recent_2021 = pd.read_csv(base_dir_rec + "2021/dwd_actual_recent_2021.csv")
df_DWD_actual_recent_2018_2019 = pd.read_csv(base_dir_rec + "2018_2019/dwd_actual_recent_2018_2019.csv")

df_DWD_recent_gefiltert_2021 = fn.filter_dataframe_GHI(df_DWD_actual_recent_2021)
df_actual_recent_2021 = fn.tuning_DWD(df_DWD_recent_gefiltert_2021)

df_DWD_recent_gefiltert_2018_2019 = fn.filter_dataframe_GHI(df_DWD_actual_recent_2018_2019)
df_actual_recent_2018_2019 = fn.tuning_DWD(df_DWD_recent_gefiltert_2018_2019)

result = fn.compare_DWD_historical_month("2021_06", 1, df_actual_recent_2021)

print(result.columns)

result = fn.adding_zenith_angle(result)
#print(result.head(40))

result_day = result.drop(result[result.Ghi_hourly == 0].index)

plt.subplot(1,2,1)
plt.scatter(result_day["zenith_angle"], result_day["Ghi_hf"], label="forecast", c=result_day["N"], cmap="binary")
plt.title("Abhängigkeit zwischen Ghi-forecast und Zenith_angle")
plt.xlabel("Zenith_angle")
plt.ylabel("Forecast-Ghi in W/m**2")
cbar = plt.colorbar()
cbar.set_label("Bedeckungsgrad")
plt.legend()

plt.subplot(1,2,2)
plt.scatter(result_day["zenith_angle"], result_day["Ghi_hourly"], label="actual", c=result_day["N"], cmap="viridis_r")
plt.title("Abhängigkeit zwischen Ghi und Zenith_angle")
plt.xlabel("Zenith_angle")
plt.ylabel("Ghi in W/m**2")
cbar = plt.colorbar()
cbar.set_label("Bedeckungsgrad")
plt.legend()

plt.show()




























plt.plot(result.index, result["Ghi_hf"], label= "Ghi historical forecast", c= "red")
plt.plot(result.index, result["N"], label = "Bedeckungsgrad", c="blue")
plt.plot(result.index, result["Neff"], label = "Effektiver Bedeckungsgrad", c="green")
plt.title("Vergleich DWD historical forecast mit Messwerten für Mai 2021 (1h Auflösung)")
plt.xlabel("Time")
plt.ylabel("Ghi in W/m**2")
plt.legend()
plt.show()



error_list_names = ["RMSE", "MBE","MAE", "SD"]
error_list_names_relative = ["rRMSE", "rMBE","rMAE", "rSD", "R_2"]

error_list = er.get_errors(result, "Ghi_hf", "Ghi_hourly")
error_list_day = er.get_errors(result_day, "Ghi_hf", "Ghi_hourly")

error_list_relative = er.get_errors_relative(result, "Ghi_hf", "Ghi_hourly")
error_list_day_relative = er.get_errors_relative(result_day, "Ghi_hf", "Ghi_hourly")


error_list_temp = er.get_errors(result, "Temp_hf", "Temperature_Ambient")
error_list_day_temp = er.get_errors(result_day, "Temp_hf", "Temperature_Ambient")

error_list_relative_temp = er.get_errors_relative(result, "Temp_hf", "Temperature_Ambient")
error_list_day_relative_temp = er.get_errors_relative(result_day, "Temp_hf", "Temperature_Ambient")

# error_list_E = er.get_errors(result, "Rad1h", "E_hourly")
# error_list_day_E = er.get_errors(result_day, "Rad1h", "E_hourly")
#
# error_list_relative_E = er.get_errors_relative(result, "Rad1h", "E_hourly")
# error_list_day_relative_E = er.get_errors_relative(result_day, "Rad1h", "E_hourly")

plt.style.use("seaborn-whitegrid")
plt.plot(result.index, result["Ghi_hf"], label= "Stündliche Vorhersage", c= "red")
plt.plot(result.index, result["Ghi_hourly"], label = "Stündlich gemittelte Messwerte", c="blue")
plt.title("Vergleich historische Vorhersage mit Messwerten für Juni 2021 - Berlin", size=30)
plt.xticks(fontsize = 19)
plt.yticks(fontsize = 19)
plt.ylabel("Ghi  [W/m^2]", size=25)
plt.legend(prop = {"size":15})
plt.show()

plt.plot(result.index, result["Temperature_Ambient"], label= "Temperatur actual", c= "red")
plt.plot(result.index, result["Temp_hf"], label = "Temperatur historical forecast", c="blue")
plt.title("Temperaturvergleich DWD historical forecast mit Messwerten für Mai 2021 (1h Auflösung)")
plt.xlabel("Time")
plt.ylabel("Temp in ºC")
plt.legend()
plt.show()

# plt.plot(result.index, result["Rad1h"], label= "Rad1h historical forecast", c= "red")
# plt.plot(result.index, result["E_hourly"], label = "E actual (hourly mean)", c="blue")
# plt.title("Vergleich DWD historical forecast mit Messwerten für Februar 2019 (1h Auflösung)")
# plt.xlabel("Time")
# plt.ylabel("E in kJ/m**2")
# plt.legend()
# plt.show()

# plt.style.use("seaborn-whitegrid")
# plt.subplot(2,1,1)
# xpos= np.arange(len(error_list_names))
#
# plt.bar(xpos-0.2, error_list_E,width=0.4, label="all data", color="red")
# plt.bar(xpos+0.2, error_list_day_E, width=0.4, label="only day", color="green")
# for i in range(len(error_list_names)):
#     plt.text(i - 0.2, error_list_E[i], int(round(error_list_E[i], 0)), ha="center", va="bottom")
#     plt.text(i + 0.2, error_list_day_E[i], int(round(error_list_day_E[i], 0)), ha="center", va="bottom")
#
# plt.title("Fehler der Vorhersagen mit und ohne nighttime für Februar 2019")
# plt.xticks(xpos, error_list_names)
# plt.ylabel("E")
# plt.legend()
#
# plt.subplot(2,1,2)
# xpos= np.arange(len(error_list_names_relative))
# plt.bar(xpos-0.2, error_list_relative_E, width=0.4, label="all data", color="red")
# plt.bar(xpos+0.2, error_list_day_relative_E, width=0.4, label="only day", color="green")
# for i in range(len(error_list_names_relative)):
#     plt.text(i - 0.2, error_list_relative_E[i], round(error_list_relative_E[i], 2), ha="center", va="bottom")
#     plt.text(i + 0.2, error_list_day_relative_E[i], round(error_list_day_relative_E[i], 2), ha="center", va="bottom")
#
# plt.title("Relative Fehler der Vorhersagen mit und ohne nighttime für Februar 2019")
# plt.xticks(xpos, error_list_names_relative)
# plt.ylabel("-")
#
# plt.legend()
# plt.show()



# plt.style.use("seaborn-whitegrid")
# plt.subplot(2,1,1)
# xpos= np.arange(len(error_list_names))
#
# plt.bar(xpos-0.2, error_list_temp,width=0.4, label="all data", color="red")
# plt.bar(xpos+0.2, error_list_day_temp, width=0.4, label="only day", color="green")
# for i in range(len(error_list_names)):
#     plt.text(i - 0.2, error_list_temp[i], round(error_list_temp[i], 2), ha="center", va="bottom")
#     plt.text(i + 0.2, error_list_day_temp[i], round(error_list_day_temp[i], 2), ha="center", va="bottom")
#
# plt.title("Fehler der Temperaturvorhersagen mit und ohne nighttime für Juni 2021")
# plt.xticks(xpos, error_list_names)
# plt.ylabel("ºC")
# plt.legend()
#
# plt.subplot(2,1,2)
# xpos= np.arange(len(error_list_names_relative))
# plt.bar(xpos-0.2, error_list_relative_temp, width=0.4, label="all data", color="red")
# plt.bar(xpos+0.2, error_list_day_relative_temp, width=0.4, label="only day", color="green")
# for i in range(len(error_list_names_relative)):
#     plt.text(i - 0.2, error_list_relative_temp[i], round(error_list_relative_temp[i], 2), ha="center", va="bottom")
#     plt.text(i + 0.2, error_list_day_relative_temp[i], round(error_list_day_relative_temp[i], 2), ha="center", va="bottom")
#
# plt.title("Relative Fehler der Temperaturvorhersagen mit und ohne nighttime für Juni")
# plt.xticks(xpos, error_list_names_relative)
# plt.ylabel("-")
#
# plt.legend()
# plt.show()








plt.style.use("seaborn-whitegrid")
plt.subplot(2,1,1)
xpos= np.arange(len(error_list_names))

plt.bar(xpos-0.2, error_list,width=0.4, label="all data", color="red")
plt.bar(xpos+0.2, error_list_day, width=0.4, label="only day", color="green")
for i in range(len(error_list_names)):
    plt.text(i - 0.2, error_list[i], int(round(error_list[i], 0)), ha="center", va="bottom")
    plt.text(i + 0.2, error_list_day[i], int(round(error_list_day[i], 0)), ha="center", va="bottom")

plt.title("Fehler der Vorhersagen mit und ohne nighttime für Mai 2021")
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

plt.title("Relative Fehler der Vorhersagen mit und ohne nighttime für Mai")
plt.xticks(xpos, error_list_names_relative)
plt.ylabel("-")

plt.legend()
plt.show()


diagon = [0,900]
plt.scatter(result_day["Ghi_hf"], result_day["Ghi_hourly"],c = result_day["zenith_angle"], cmap="viridis", edgecolors="black", linewidths=0.5, alpha=0.75)
plt.plot(diagon,diagon)
cbar = plt.colorbar()
cbar.set_label("Zenith angle")
plt.clim(30, 90)

plt.title("Vergleich Vorhersage mit Messdaten")
plt.xlabel("Forecast Ghi in W/m**2")
plt.ylabel("Gemessene Ghi in W/m**2")
plt.show()


#Plot Abhängigkeit zwischen Ghi-foreast und k*-forecast mit Berücksichtigung der Position der Sonne
#Plot Abhängigkeit zwischen Ghi_Messwerte und k*-Werte mit Berücksichtigung der Position der Sonne
plt.subplot(1,2,1)
plt.scatter(result_day["N"], result_day["Ghi_hf"], label="forecast", c=result_day["zenith_angle"], cmap="viridis")
plt.title("Abhängigkeit zwischen Ghi-forecast und Bedeckungsgrad")
plt.xlabel("Bedeckungsgrad")
plt.ylabel("Ghi in W/m**2")
cbar = plt.colorbar()
cbar.set_label("zenith_angle")
plt.legend()

plt.subplot(1,2,2)
plt.scatter(result_day["Neff"], result_day["Ghi_hf"], label="forecast", c=result_day["zenith_angle"], cmap="viridis")
plt.title("Abhängigkeit zwischen Ghi-forecast und effektiver Bedeckungsgrad")
plt.xlabel("Effektiver Bedeckungsgrad")
plt.ylabel("Ghi in W/m**2")
cbar = plt.colorbar()
cbar.set_label("zenith_angle")
plt.legend()

plt.show()






#Plot Abhängigkeit zwischen Ghi-foreast und k*-forecast mit Berücksichtigung der Position der Sonne
#Plot Abhängigkeit zwischen Ghi_Messwerte und k*-Werte mit Berücksichtigung der Position der Sonne
plt.subplot(1,2,1)
plt.scatter(result_day["zenith_angle"], result_day["Ghi_hf"], label="actual", c=result_day["N"], cmap="viridis")
plt.title("Abhängigkeit zwischen Ghi und Bedeckungsgrad")
plt.xlabel("Zenith_angle")
plt.ylabel("Ghi in W/m**2")
cbar = plt.colorbar()
cbar.set_label("zenith_angle")
plt.legend()

plt.subplot(1,2,2)
plt.scatter(result_day["zenith_angle"], result_day["Ghi_hourly"], label="actual", c=result_day["N"], cmap="viridis")
plt.title("Abhängigkeit zwischen Ghi und effektiver Bedeckungsgrad")
plt.xlabel("Zenith_angle")
plt.ylabel("Ghi in W/m**2")
cbar = plt.colorbar()
cbar.set_label("zenith_angle")
plt.legend()

plt.show()