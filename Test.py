import pandas as pd
import functions as fn
from Mosmix import import_MOSMIX

pd.options.mode.chained_assignment = None

for day in range(1,32):
    for h in range (0,24):
        try:
            dict = import_MOSMIX.get_forecast_for_Station("Wetter/201812_berlin/MOSMIX_S_201812" + str(day).zfill(2) + str(h).zfill(2) + "_240_berlin.kml", "X105")
            df = pd.DataFrame(dict)
            dataframe = fn.tuning_DWD_historical_forecast(df)
            dataframe.to_csv("./DWD/Berlin/2018_12/2018_12_X105/dwd_forecast" + str(day).zfill(2) + "_" + str(h).zfill(2) + ".csv", encoding='utf-8')
        except:
            continue



# base_dir_rec = "./DWD/Recent/dwd_recent_"
#
# faktor_Ghi_10min = 10000/600
# faktor_Ghi_hourly = 1000/3600
#
#
# #df =
# df_DWD_recent = pd.read_csv(base_dir_rec + "2021-06-22_10.csv")
# df_DWD_recent_gefiltert = fn.filter_dataframe_GHI(df_DWD_recent)
# df_DWD_tuned = fn.tuning_DWD(df_DWD_recent_gefiltert)
#
# df_DWD_tuned["Ghi"] = df_DWD_tuned["Global_sky_radiation"]*faktor_Ghi_10min
# df_DWD_tuned["E"] = df_DWD_tuned["Global_sky_radiation"]*10
#
# df_DWD_tuned["Ghi_hourly"] = 0
# df_DWD_tuned["E_hourly"] = 0
# for i in range(len(df_DWD_tuned["Ghi"])):
#     if i > 4:
#         df_DWD_tuned["E_hourly"][i] = df_DWD_tuned["E"][i] + df_DWD_tuned["E"][i-1] + df_DWD_tuned["E"][i-2] + df_DWD_tuned["E"][i-3] + df_DWD_tuned["E"][i-4] + df_DWD_tuned["E"][i-5]
#         df_DWD_tuned["Ghi_hourly"][i] = (df_DWD_tuned["Ghi"][i] + df_DWD_tuned["Ghi"][i-1] + df_DWD_tuned["Ghi"][i-2] + df_DWD_tuned["Ghi"][i-3] + df_DWD_tuned["Ghi"][i-4] + df_DWD_tuned["Ghi"][i-5])/6
#     else:
#         df_DWD_tuned["Ghi_hourly"][i] = 0
#
#
# df_actual_recent = df_DWD_tuned.drop(df_DWD_tuned[df_DWD_tuned.index.minute != 0].index)
#
# #print(fn.compare_DWD_historical_month("2021_01", 1, df_actual_recent).columns)
# result = fn.compare_DWD_historical_month("2021_05", 1, df_actual_recent)
# result_day = result.drop(result[result.Ghi_hourly == 0].index)
#
# #result["delta"] = result["Ghi_hf"] - result["Ghi_hourly"]
#
# error_list_names = ["RMSE", "MBE","MAE", "SD"]
# error_list_names_relative = ["rRMSE", "rMBE","rMAE", "rSD", "R_2"]
# error_list = er.get_errors(result, "Ghi_hf", "Ghi_hourly")
# error_list_day = er.get_errors(result_day, "Ghi_hf", "Ghi_hourly")
#
# # plt.plot(result.index, result["Ghi_hf"], label= "Ghi historical forecast", c= "red")
# # plt.plot(result.index, result["Ghi_hourly"], label = "Ghi actual (hourly mean)", c="blue")
# # plt.title("Vergleich DWD historical forecast mit Messwerten (1h Auflösung)")
# # plt.xlabel("Time")
# # plt.ylabel("Ghi in W/m**2")
# # plt.legend()
# # plt.show()
#
# plt.style.use("seaborn-whitegrid")
# xpos= np.arange(len(error_list_names))
#
# plt.bar(xpos-0.2, error_list,width=0.4, label="all data", color="red")
# plt.bar(xpos+0.2, error_list_day, width=0.4, label="only day", color="green")
# for i in range(len(error_list_names)):
#     plt.text(i - 0.2, error_list[i], int(round(error_list[i], 0)), ha="center", va="bottom")
#     plt.text(i + 0.2, error_list_day[i], int(round(error_list_day[i], 0)), ha="center", va="bottom")
#
# plt.title("Fehler der Vorhersagen mit und ohne nighttime für Mai")
# plt.xticks(xpos, error_list_names)
# plt.ylabel("Ghi")
# plt.legend()
# plt.show()

