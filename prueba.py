import pandas as pd
import matplotlib.pyplot as plt
import functions as fn
import errors as er
import numpy as np
from scipy import optimize
pd.options.mode.chained_assignment = None

base_dir_rec = "./DWD/Recent/"
df_DWD_actual_recent_2021 = pd.read_csv(base_dir_rec + "2021/dwd_actual_recent_2021.csv")

df_DWD_recent_gefiltert_2021 = fn.filter_dataframe_GHI(df_DWD_actual_recent_2021)
df_actual_recent_2021 = fn.tuning_DWD(df_DWD_recent_gefiltert_2021)

result = fn.compare_every_historical_forecast("2021_06", 16, df_actual_recent_2021 )
result = fn.adding_zenith_angle(result)
result["delta_rounded"] = round((result["delta"]/5)) *5
result["relative_delta"] = result["delta"] / result["Ghi_hourly"]
result_day = result.drop(result[result.Ghi_hourly == 0].index)


result_delta = result_day.groupby(["delta_rounded"]).count()
number_of_datapairs_unequal_to_0 = result["relative_delta"].count()
result_delta["percent"] = result_delta["relative_delta"]/number_of_datapairs_unequal_to_0

def gaussian_f(x, a, b, c):
    y = a * np.exp(-0.5 * ((x-b)/c)**2)
    return y

x_values = result_delta.index
y_values = result_delta["percent"]
#
init_guess = [100,50,-100]
popt, cov = optimize.curve_fit(gaussian_f, x_values, y_values)
a,b,c = popt


plt.bar(result_delta.index, result_delta["percent"],width=4, color= "blue")
plt.plot(x_values, gaussian_f(x_values, a,b,c), color="red")


plt.title("Häufigkeitsverteilung der Abweichung für Juni 2021 mit 16h-Vorhersagehorizont")
plt.xlabel("Abweichung in 5 W/m**2 -Schrite")
plt.ylabel("Häufigkeit")
plt.show()

