import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import functions

#df_DWD_historical = import_DWD_weather_2_pd_DataFrame.measurement("00433", "solar", False, True, False)


#solarRadiation_actuals_05_06 = "./Solcast/SolarRadiation/EstimatedActuals/GetWeatherSiteEstimatedActuals_05_06.csv"
#solcast_historical_10m = "./Solcast/Historical/52.458235_13.287083_Solcast_PT10M.csv"


result = functions.compare_solcast_DWD_historical()

#Umrechnung von [J/cm**2] auf [W/m**2]
faktor = 10000/(60*10)


plt.plot(result.index, result["Global_sky_radiation"]* faktor, label= "DWD", color= "blue")
plt.plot(result.index, result["Ghi"], label= "Solcast", color= "red")
plt.title("Vergleich historical Data Solcast und DWD")
plt.xlabel("Zeit in 10 Min Auflösung")
plt.ylabel("Ghi in [W/m**2]")
plt.legend()
plt.show()

list_solcast = []
list_DWD = []
for i in range(len(result["Ghi"])):
    list_solcast.append(result["Ghi"][i])
    list_DWD.append((result["Global_sky_radiation"][i]))


standard_deviation = functions.calc_SD(list_DWD,list_solcast)
mean_biaes_deviation = functions.calc_MBD(list_DWD, list_solcast)
root_mean_square_deviation = functions.calc_RMSD(list_DWD, list_solcast)
print("Standard deviation = " , standard_deviation)
print("Mean bias deviation = ", mean_biaes_deviation)
print("Root mean square deviation = ", root_mean_square_deviation)
