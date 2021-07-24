import pandas as pd
import json
import requests
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import solcast
import import_DWD_weather_2_pd_DataFrame
import errors
import os

def filter_dataframe_GHI(dataframe):
    counter = len(dataframe["Global_sky_radiation"])
    droper = []
    for i in range(0, counter):
        if dataframe["Global_sky_radiation"][i] < 0:
            droper.append(i)


    droper_reverse = droper[::-1]

    for n in droper_reverse:
        #a =1
        dataframe = dataframe.drop(index=dataframe.index[n])
        # test_df = test_df.drop(index = test_df.index[54199])
    return dataframe


def tuning_df_solcast(dataframe):
    try:
        dataframe["PeriodEnd"] = pd.to_datetime(dataframe["PeriodEnd"])
        dataframe.set_index("PeriodEnd", drop=False, inplace=True)
    except:
        dataframe["period_end"] = pd.to_datetime(dataframe["period_end"])
        dataframe.set_index("period_end", drop=False, inplace=True)
    return dataframe


def tuning_DWD_Forecast(dataframe):
    #result = dataframe[["timestamp", "Global_sky_radiation_Forecast"]]
    dataframe["timestamp"] = pd.to_datetime(dataframe["timestamp"])
    dataframe["timestamp"] = dataframe["timestamp"].dt.strftime("%Y-%m-%d %H:%M:%S")
    dataframe["timestamp"] = pd.to_datetime(dataframe["timestamp"])
    dataframe.set_index("timestamp", drop=True, inplace=True)

    return dataframe

def tuning_DWD_historical_forecast(dataframe, horizont=None):
    dataframe["Timesteps"] = pd.to_datetime(dataframe["Timesteps"])
    dataframe["Timesteps"] = dataframe["Timesteps"].dt.strftime("%Y-%m-%d %H:%M:%S")
    dataframe["Timesteps"] = pd.to_datetime(dataframe["Timesteps"])
    dataframe.set_index("Timesteps", drop=True, inplace=True)

    result = dataframe[["N", "Neff", "Rad1h", "TTT"]]
    if horizont != None:
        return result.head(horizont)
    else:
        return result


def compare_DWD_historical_month(month, horizont, dataframe_actual_recent):
    """

    :param month: format: Year_Month. example: 2020_01
    :param dataframe_actual_recent:
    :return:
    """
    path = "DWD/Berlin/" + month + "/" + month + "_X105"
    faktor_hourly = 1000/3600  #Von kJ/m**2 auf W/mm*2 für 1_Stunde Werte

    files = os.listdir(path)
    list_df = []
    for file in files:
        file = os.path.join(path, file)
        df = pd.read_csv(file)
        result = tuning_DWD_historical_forecast(df, horizont)
        list_df.append(result)

    #list_df ist eine Liste mit allen Forecasts mit dem in der Funktion gegebenen horizont

    df_forecast = pd.concat(list_df, axis=0)

    #df_forecast = df_forecast.drop_duplicates()
    df_forecast = df_forecast[~df_forecast.index.duplicated(keep='first')]

    df_forecast["Ghi_hf"] = df_forecast["Rad1h"] * faktor_hourly
    df_forecast["Temp_hf"] = df_forecast["TTT"] -273.15

    result = pd.concat([dataframe_actual_recent, df_forecast], axis=1, join="inner")

    return result

def compare_every_historical_forecast(month, horizont, actual_dataframe):
    path = "DWD/Berlin/" + month + "/" + month + "_X105"
    faktor_hourly = 1000 / 3600

    files = os.listdir(path)
    list_hf = []
    for file in files:
        file = os.path.join(path, file)
        df = pd.read_csv(file)
        result = tuning_DWD_historical_forecast(df, horizont)
        result["Ghi_hf"] = result["Rad1h"] * faktor_hourly
        result["Temp_hf"] = result["TTT"] -273.15
        list_hf.append(result)

    result = []
    for i in range(len(list_hf)):
        result.append(pd.concat([list_hf[i], actual_dataframe], axis= 1, join="inner"))
    dataframe = pd.concat(result, axis=0)
    dataframe["delta"] = dataframe["Ghi_hf"] - dataframe["Ghi_hourly"]

    return dataframe

def tuning_DWD(dataframe):
    dataframe["timestamp"] = pd.to_datetime(dataframe["timestamp"])
    dataframe.set_index("timestamp", drop=True, inplace=True)

    return dataframe


def tuning_24h_df_solcast(dataframe):
    try:
        dataframe["PeriodEnd"] = pd.to_datetime(dataframe["PeriodEnd"])
        dataframe.set_index("PeriodEnd", drop=False, inplace=True)
    except:
        dataframe["period_end"] = pd.to_datetime(dataframe["period_end"])
        dataframe.set_index("period_end", drop=False, inplace=True)
        dataframe_24h = dataframe.head(48)
    return dataframe_24h


def get_solcast_dataframe(period, hours, resource_id ="e7c8-8b3c-1b79-dc11" ):
    api_key = "3MxXoCUlvlQqEMh7vcFlXa3yUPWx6R71"
    url ="https://api.solcast.com.au/weather_sites/%s/forecasts?period=PT%sM&hours=%s&format=json&api_key=%s" % (
        str(resource_id), str(period), str(hours), api_key
    )
    response = requests.get(url)
    solcast_forecast = json.loads(response.text)
    df_solcast_forecast = pd.DataFrame(solcast_forecast)
    print(df_solcast_forecast)
    try:
        df_solcast_forecast["PeriodEnd"] = pd.to_datetime(df_solcast_forecast["PeriodEnd"])
        df_solcast_forecast.set_index("PeriodEnd", drop=False, inplace=True)
    except:
        df_solcast_forecast["period_end"] = pd.to_datetime(df_solcast_forecast["period_end"])
        df_solcast_forecast.set_index("period_end", drop=False, inplace=True)

    return df_solcast_forecast


def plot_temperature(dataframe):
    plt.plot(dataframe.index, dataframe["Temperature_Ambient"], label = "temperature", color = "blue")
    plt.xlabel("Zeit")
    plt.ylabel("Temperatur in ºC")
    plt.legend()
    plt.title("Air temperature für den gesuchten Zeitraum")
    plt.show()


def solcast_forecast_dataframe(forecast_end, lat =52.4582, lon = 13.287 ):
    """
    :param forecast_end: the amount of hours the forecast must predict
    :param lat: latitude (Berlin-Dahlem : 52.4582)
    :param lon: longitude (Berlin_Dahlem : 13.287)
    :return: weather_data is a list with the different stats
             df_solcast_forecast is a datframe with the period end as index with the given data
    """
    # Use solcast API
    api_key_solcast = "3MxXoCUlvlQqEMh7vcFlXa3yUPWx6R71"
    solcast_forecast = solcast.get_radiation_forecasts(lat, lon, api_key_solcast).content['forecasts'][0:forecast_end]


    # %% Extract Temperature and Irradiance Data
    weather_data = {'q_direct': None, 'q_diffuse': None, 'air_temp': None, "q_global" : None}

    q_global = np.zeros(forecast_end)  # Global horizontal irradiance in W/m²
    q_direct = np.zeros(forecast_end)  # Direct horizontal irradance in W/m²
    q_diffuse = np.zeros(forecast_end)  # Diffuse Horizontal Irradiance in W/m²
    air_temp_forecast_sc = np.zeros(forecast_end)

    for i in range(forecast_end):
        q_global[i] = solcast_forecast[i]['ghi']
        q_direct[i] = solcast_forecast[i]['ghi'] - solcast_forecast[i]['dhi']
        q_diffuse[i] = solcast_forecast[i]['dhi']
        air_temp_forecast_sc[i] = solcast_forecast[i]['air_temp']


    df_solcast_forecast = pd.DataFrame(solcast_forecast)

    df_solcast_forecast["period_end"] = pd.to_datetime(df_solcast_forecast["period_end"])
    df_solcast_forecast = df_solcast_forecast.set_index("period_end")


    weather_data['q_direct'] = q_direct
    weather_data['q_diffuse'] = q_diffuse
    weather_data['air_temp_sc'] = air_temp_forecast_sc
    weather_data["q_global"] = q_global

    # get the time horizon of this forecasting
    # Daylight Saving Time is not counted in the solcast and openweathermap
    # forecast_start = solcast_forecast[0]['period_end']- dt.timedelta(minutes = 30)
    # forecast_end = solcast_forecast[47]['period_end']

    #forecast_start = dt.datetime.fromtimestamp(openweather_forecast['hourly'][0]['dt'])
    #forecast_end = dt.datetime.fromtimestamp(openweather_forecast['hourly'][23]['dt']) + dt.timedelta(hours=1)
    #current_time = dt.datetime.fromtimestamp(openweather_forecast['current']['dt'])

    #forecast_time_horziont = [forecast_start, forecast_end]
    #weather_data['forecast_time_horziont'] = forecast_time_horziont
    #weather_data['loaded_at'] = current_time

    return weather_data, df_solcast_forecast


def compare_stat(df_forecast, df_actual, stat):
    """
    Compare one stat (PV-Power, Cloud Opacity, Global Horizontal Irradiance...) of two dataframes. The function checks
    the time of each "PeriodEnd" in both dataframes and compares the given stat for the same time.
    Returns a new dataframe with the stat for both Dataframes with a new column delta wich shows the difference between
    the actual data and the forecast
    """
    df_actual["time"] = df_actual["period_end"]

    # Seting the index of both dataframes to the time
    try:
        df_forecast["PeriodEnd"] = pd.to_datetime(df_forecast["PeriodEnd"])
        df_forecast.set_index("PeriodEnd", drop= False, inplace=True)
    except:
        df_forecast["period_end"] = pd.to_datetime(df_forecast["period_end"])
        df_forecast.set_index("period_end", drop=False, inplace=True)

    try:
        df_actual["PeriodEnd"] = pd.to_datetime(df_actual["PeriodEnd"])
        df_actual.set_index("PeriodEnd", drop=False, inplace=True)
    except:
        df_actual["period_end"] = pd.to_datetime(df_actual["period_end"])
        df_actual.set_index("period_end", drop= False, inplace=True)

    # Changing the name of the columns in the forecast-dataframe.
    # Other columns names can be changed an added to the result dataframe bellow
    df_forecast.rename(
        columns={stat: stat + '_for'}, inplace=True)

    # Concatinating both dataframes and adding a delta-column
    result = pd.concat([df_actual, df_forecast], axis=1, join="inner")
    result["delta_" + stat] = result[stat] - result[stat + "_for"]
    return result[[stat, stat + "_for", "delta_" + stat, "time"]]


def compare_solcast_DWD_historical():
    """
    Comparing the historical Data from Solcast and DWD for a common Period of time
    :return: Dataframe with both columns
    """
    df_DWD_historical = import_DWD_weather_2_pd_DataFrame.measurement("00433", "solar", False, True, False)
    df_DWD_historical_gefiltert = filter_dataframe_GHI(df_DWD_historical)
    df_solcast_historical = pd.read_csv("./Solcast/Historical/52.458235_13.287083_Solcast_PT10M.csv")

    df_solcast_historical["timestamp"] = pd.to_datetime(df_solcast_historical["PeriodEnd"])

    df_solcast_historical["timestamp"] = df_solcast_historical["timestamp"].dt.strftime("%Y-%m-%d %H:%M:%S")

    df_solcast_historical["timestamp"] = pd.to_datetime(df_solcast_historical["timestamp"])

    df_solcast_historical.set_index("timestamp", drop=True, inplace=True)


    result = pd.concat([ df_DWD_historical_gefiltert, df_solcast_historical ], axis=1, join="inner")
    return result


def plot_mean_CloudOpacity_in_day(dataframe):
    dataframe["Date"] = dataframe["PeriodEnd"].str[0:10]
    dataframe["Date"] = pd.to_datetime(dataframe["Date"])
    dataframe["day"] = dataframe["Date"].dt.day

    dataframe_days = dataframe.groupby("day").mean()

    days = []
    for day in dataframe_days.index:
        days.append(day)

    plt.bar(days, dataframe_days["CloudOpacity"])
    plt.ylabel("CloudOpacity")
    plt.xlabel("Days")
    print(dataframe_days)
    plt.show()


def plot_mean_Ghi_in_day(datadframe):
    datadframe["Date"] = datadframe["PeriodEnd"].str[0:10]
    datadframe["Date"] = pd.to_datetime(datadframe["Date"])
    datadframe["Day"] = datadframe["Date"].dt.day

    datadframe_days = datadframe.groupby("Day").mean()

    days = []
    for day in datadframe_days.index:
        days.append(day)

    plt.bar(days, datadframe_days["Ghi"])
    plt.ylabel("Global Horizontal Irradiance (W/m**2)")
    plt.xlabel("Days")
    plt.title("Durchschnittliches GHI für jeden Tag")
    print(datadframe_days)
    plt.show()


def plot_mean_Dni_in_day(datadframe):
    datadframe["Time"] = datadframe["PeriodEnd"].str[0:10]
    datadframe["Time"] = pd.to_datetime(datadframe["Time"])
    datadframe["Day"] = datadframe["Time"].dt.day

    datadframe_days = datadframe.groupby("Day").mean()

    days = []
    for day in datadframe_days.index:
        days.append(day)

    plt.bar(days, datadframe_days["Dni"])
    plt.ylabel("Direct Normal Irradiance (W/m**2)")
    plt.xlabel("Days")
    print(datadframe_days)
    plt.show()


def get_errors(df_forecast, df_actual):
    result = pd.merge(df_forecast, df_actual, suffixes=["_for", "_act"], left_index=True, right_index=True)
    list_for = []
    list_act = []
    for i in range(len(result["Ghi_for"])):
        list_for.append(result["Ghi_for"][i])

    for n in range(len(result["Ghi_act"])):
        list_act.append(result["Ghi_act"][n])

    standard_deviation = errors.calc_SD(list_for, list_act)
    mean_biaes_error = errors.calc_MBE(list_for, list_act)
    root_mean_squared_error = errors.calc_RMSE(list_for, list_act)
    r_2 = errors.calc_R_2(list_for, list_act)
    error_list = [root_mean_squared_error, mean_biaes_error, standard_deviation, r_2]
    return error_list


def concat_2_dataframes_Ghi(df_forecast, df_actual, stat ="Ghi"):
    df_forecast.rename(
        columns={stat: stat + '_for'}, inplace=True)

    # Concatinating both dataframes and adding a delta-column
    result = pd.concat([df_actual, df_forecast], axis=1, join="inner")
    return result[[stat, stat + "_for", "Ghi90", "Ghi10"]]


def concat_2_dataframes(df_forecast, df_actual, stat ="Ghi", stat2 = "cloud_opacity"):
    df_forecast.rename(
        columns={stat: stat + '_for', stat2: stat2+"_for", "air_temp": "AirTemp_for"}, inplace=True)

    # Concatinating both dataframes and adding a delta-column
    result = pd.concat([df_actual, df_forecast], axis=1, join="inner")
    return result

def save_solcast_forecast_16h():
    weather_data, df_solcast_forecast = solcast_forecast_dataframe(32)
    today = dt.date.today()
    now = dt.datetime.now()
    hour = now.hour

    df_solcast_forecast.to_csv("./Solcast/SolarRadiation/16h_Forecasts/solcast_forecast_16h_" + str(today) + "_" + str(hour) + ".csv", encoding='utf-8')


def save_solcast_forecast_48h():
    weather_data, df_solcast_forecast = solcast_forecast_dataframe(96)
    today = dt.date.today()
    now = dt.datetime.now()
    hour = now.hour

    df_solcast_forecast.to_csv("./Solcast/SolarRadiation/48h_Forecasts/solcast_forecast_48h_" + str(today) +"_" + str(hour) + ".csv", encoding='utf-8')


def save_DWD_forecast_16h():
    today = dt.date.today()
    now = dt.datetime.now()
    hour = now.hour

    df_DWD_forecast = import_DWD_weather_2_pd_DataFrame.forecast("10381")

    df_DWD_forecast.to_csv("./DWD/live_forecasts/dwd_forecast_"+ str(today) + "_" + str(hour) + ".csv", encoding='utf-8')


def calc_zenith_angle(day, hour, year):
    lat = 52.47
    lon = 13.4
    LT = hour
    solar_declination = -23.45*np.cos(np.deg2rad(360/365*(day+10)))
    B = 360/365 *(day-81)
    EOT = 9.87*np.sin(np.deg2rad(2*B))- 7.53 * np.cos(np.deg2rad(B)) - 1.5 * np.sin(np.deg2rad(B))

    #LSTM = 30 für Sommerzeit in Berlin. Hängt jeweils vom Jahr ab:
    if year == 2018:
        if day > 83 and day <301:
            LSTM = 30
        else: LSTM= 15

    if year == 2019:
        if day > 89 and day <300:
            LSTM = 30
        else: LSTM = 15

    if year == 2020:
        if day > 88 and day <299:
            LSTM = 30
        else: LSTM = 15

    if year == 2021:
        if day > 86 and day <304:
            LSTM = 30
        else: LSTM = 15

    TC = 4*(lon) + EOT
    LST = LT + (TC/60)
    h_angle = 15*(LST-12)

    zenith_angle = np.arccos(
        np.sin(np.deg2rad(lat)) * np.sin(np.deg2rad(solar_declination)) + np.cos(np.deg2rad(lat)) * np.cos(
            np.deg2rad(solar_declination)) * np.cos(np.deg2rad(h_angle)))
    return  np.rad2deg(zenith_angle)


def adding_zenith_angle(dataframe):
    previous_days = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]
    dataframe["year"] = int(dataframe.index.year[0])
    dataframe["month"] = dataframe.index.month
    dataframe["day"] = dataframe.index.day
    dataframe["hour"] = dataframe.index.hour
    dataframe["zenith_angle"] = 0
    for i in range(len(dataframe)):
        dataframe["day"][i] += previous_days[int(dataframe["month"][i]) - 1]
        if dataframe["year"][i] == 2020 and int(dataframe["month"][i]) > 2:
            dataframe["day"][i] += 1

        dataframe["zenith_angle"][i] += calc_zenith_angle(dataframe["day"][i], dataframe["hour"][i], dataframe["year"][i])

    dataframe = dataframe.drop(["year","month","day","hour"], axis=1)

    return dataframe

