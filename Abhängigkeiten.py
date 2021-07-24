import pandas as pd
import functions as fn
import matplotlib.pyplot as plt
import numpy as np
import errors as er

dir_a = "./Solcast/SolarRadiation/EstimatedActuals/GetWeatherSiteEstimatedActuals_"
dir_f = "./Solcast/SolarRadiation/Forecasts/GetWeatherSiteForecast_"

diagon = [0,900]

list_df_actuals = []
for i in range(1,32):
    try:
        list_df_actuals.append(fn.tuning_df_solcast(pd.read_csv(dir_a + str(i).zfill(2) + "_06.csv")))
    except: continue

list_df_forecast = []
for i in range(1,32):
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

#Plot Vergleich Globale Einstrahlung forecast mit Messwerten aus den ganzen Juni ohne Nachtwerte
plt.plot(result.index, result["Ghi_for"], color= "red", label = "rolling_forecast")
plt.plot(result.index, result["Ghi"], c = "black", label="Messwerte")
#plt.plot(result.index, result["clear_sky_index_for"]*100, color= "green", label = "k*_forecast")
#plt.plot(result.index, result["clear_sky_index"]*100, c = "blue", label="k*_actual")
plt.title("Vergleich Ghi forecast und Messwerte für Juni")
plt.xlabel("Zeit")
plt.ylabel("Ghi in W/m**2")
plt.legend()
plt.show()

plt.scatter(result["Ghi"], result["Ghi_for"], c= result["cos_theta"], cmap="viridis", alpha=0.75 )
plt.plot(diagon,diagon, c = "red")
plt.title("Messwerte und Forecast globale Einstrahlung abhängig von cos(Theta) Juni 2021")
plt.ylabel("Forecast Ghi in W/m**2")
plt.xlabel("Messwerte Ghi in W/m**2")
cbar = plt.colorbar()
cbar.set_label("cos(Theta)")
plt.legend()
plt.show()

#Plot Abhängigkeit zwischen Ghi-foreast und k*-forecast
#Plot Abhängigkeit zwischen Ghi_Messwerte und k*-Werte
plt.subplot(1,2,1)
plt.scatter(result["clear_sky_index_for"], result["Ghi_for"], label="forecast", c="red")
plt.title("Abhängigkeit zwischen Ghi-foreast und k*-forecast")
plt.xlabel("clear sky index forecast")
plt.ylabel("Forecast Ghi in W/m**2")
plt.legend()

plt.subplot(1,2,2)
plt.scatter(result["clear_sky_index"], result["Ghi"], label="Messwerte", c="blue")
plt.title("Abhängigkeit zwischen Ghi-Messwerte und k*-Werte")
plt.xlabel("clear sky index")
plt.ylabel("Messwerte Ghi in W/m**2")
plt.legend()

plt.tight_layout()
plt.show()

#Plot Abhängigkeit zwischen Ghi-foreast und k*-forecast mit Berücksichtigung der Position der Sonne
#Plot Abhängigkeit zwischen Ghi_Messwerte und k*-Werte mit Berücksichtigung der Position der Sonne
plt.subplot(1,2,1)
plt.scatter(result["clear_sky_index_for"], result["Ghi_for"], label="forecast", c=result["cos_theta"], cmap="viridis")
plt.title("Abhängigkeit zwischen Ghi-foreast und k*-forecast")
plt.xlabel("clear sky index forecast")
plt.ylabel("Forecast Ghi in W/m**2")
cbar = plt.colorbar()
cbar.set_label("cos(Theta)")
plt.legend()

plt.subplot(1,2,2)
plt.scatter(result["clear_sky_index"], result["Ghi"], label="Messwerte", c=result["cos_theta"], cmap="viridis")
plt.title("Abhängigkeit zwischen Ghi-Messwerte und k*-Werte")
plt.xlabel("clear sky index")
plt.ylabel("Messwerte Ghi in W/m**2")
cbar = plt.colorbar()
cbar.set_label("cos(Theta)")
plt.legend()

plt.show()


#Plot Abhängigkeit zwischen Ghi-foreast und k*-forecast mit Berücksichtigung der Position der Sonne
#Plot Abhängigkeit zwischen Ghi_Messwerte und k*-Werte mit Berücksichtigung der Position der Sonne
plt.subplot(1,2,1)
plt.scatter(result["clear_sky_index_for"], result["Ghi"], label="forecast", c=result["cos_theta"], cmap="viridis")
plt.title("Abhängigkeit zwischen Ghi und k*-forecast")
plt.xlabel("clear sky index forecast")
plt.ylabel("Ghi in W/m**2")
cbar = plt.colorbar()
cbar.set_label("cos(Theta)")
plt.legend()

plt.subplot(1,2,2)
plt.scatter(result["clear_sky_index_for"], result["delta"], label="Abweichung", c=result["cos_theta"], cmap="viridis")
plt.title("Abhängigkeit zwischen Ghi-Abweichung und k*-forecast")
plt.xlabel("clear sky index forecast")
plt.ylabel("Abweichung Ghi in W/m**2")
cbar = plt.colorbar()
cbar.set_label("cos(Theta)")
plt.legend()

plt.show()


#Plot Abhängigkeit zwischen cos(Theta) und Ghi
plt.subplot(1,2,1)
plt.scatter(result["cos_theta"], result["Ghi"], label="Messwerte", c="blue")
plt.title("Abhängigkeit zwischen Ghi-Messwerte und cos(Theta)")
plt.xlabel("cos(Theta)")
plt.ylabel("Ghi in W/m**2")
plt.legend()

plt.subplot(1,2,2)
plt.scatter(result["cos_theta"], result["Ghi_for"], label="forecast", c="red")
plt.title("Abhängigkeit zwischen Ghi-foreast und cos(Theta)")
plt.xlabel("cos(Theta)")
plt.ylabel("Forecast Ghi in W/m**2")
plt.legend()

plt.tight_layout()
plt.show()

#Plot Abhängigkeit zwischen cos(theta) und delta_Ghi
plt.subplot(1,2,1)
plt.scatter(result["cos_theta"], result["delta"], label="Delta Ghi", c="red")
plt.title("Abhängigkeit zwischen cos(Theta) und Ghi_delta")
plt.xlabel("cos(Theta)")
plt.ylabel("Delta Ghi in W/m**2")
plt.legend()

plt.subplot(1,2,2)
plt.scatter(result["cos_theta"], result["delta_absolute"], label="Absolute Delta", c="blue")
plt.title("Abhängigkeit zwischen Ghi-foreast und cos(Theta)")
plt.xlabel("cos(Theta)")
plt.ylabel("Delta Ghi in W/m**2")
plt.legend()

plt.tight_layout()
plt.show()

#Plot Abhängigkeit zwischen k*-forecast und delta_Ghi
plt.subplot(1,2,1)
plt.scatter(result["clear_sky_index_for"], result["delta"], label="delta", c="blue")
plt.title("Abhängigkeit zwischen k*-index_forecast und Abweichung")
plt.xlabel("k*-index_forecast")
plt.ylabel("Delta_GHI in W/m**2")
plt.legend()

plt.subplot(1,2,2)
plt.scatter(result["clear_sky_index_for"], result["delta_absolute"], label="absolute delta", c="red")
plt.title("Abhängigkeit zwischen k*-index_forecast und  absolute Abweichung")
plt.xlabel("k*-index_forecast")
plt.ylabel("Absolute Delta_GHI in W/m**2")
plt.legend()

plt.tight_layout()
plt.show()

#Plot Abhängigkeit zwischen k*-messwerte und delta
plt.subplot(1,2,1)
plt.scatter(result["clear_sky_index"], result["delta"], label="delta", c="blue")
plt.title("Abhängigkeit zwischen k*-index und Abweichung")
plt.xlabel("k*-index_gemessen")
plt.ylabel("Delta_GHI in W/m**2")
plt.legend()

plt.subplot(1,2,2)
plt.scatter(result["clear_sky_index"], result["delta_absolute"], label="absolute delta", c="red")
plt.title("Abhängigkeit zwischen k*-index und  absolute Abweichung")
plt.xlabel("k*-index_gemessen")
plt.ylabel("Absolute Delta_GHI in W/m**2")
plt.legend()

plt.tight_layout()
plt.show()

#Plot Abhängigkeit zwischen delta-k*_index und delta_Ghi
plt.subplot(1,2,1)
plt.scatter(result["clear_sky_index_delta"], result["delta"], label="delta", c="blue")
plt.title("Abhängigkeit zwischen delta_k*-index und Ghi_Abweichung")
plt.xlabel("delta_k*-index")
plt.ylabel("Delta_GHI in W/m**2")
plt.legend()

plt.subplot(1,2,2)
plt.scatter(result["clear_sky_index_delta"], result["delta_absolute"], label="absolute delta", c="red")
plt.title("Abhängigkeit zwischen delta_k*-index und absolute Ghi_Abweichung")
plt.xlabel("delta_k*-index")
plt.ylabel("Absolute Delta_GHI in W/m**2")
plt.legend()

plt.tight_layout()
plt.show()