import numpy as np




def calc_MBE(fore, act):
    """
    Berechnet die mittlere systematische Abweichung
    :param p: prognostizierter Datenpunkt
    :param a: actual estimated Datenpunkt
    :return:
    """
    N = len(fore)
    mbe = (sum(fore[i]-act[i] for i in range(N))) / N
    return mbe

def calc_MBE_rel(fore, act):
    """
    Berechnet die mittlere systematische Abweichung
    :param p: prognostizierter Datenpunkt
    :param a: actual estimated Datenpunkt
    :return:
    """
    N = len(fore)
    mbe = (sum((fore[i]-act[i])/ fore[i] for i in range(N))) / N
    return mbe

def calc_SD(fore, act):

    N = len(fore)
    er = sum(N*(fore[i]-act[i])**2 for i in range(N))
    zw = (sum(fore[i]-act[i] for i in range(N)))**2
    sd = ((er-zw)**0.5)/N
    return sd


def calc_RMSE(fore,act):
    N = len(fore)
    rmse = ((sum((fore[i]-act[i])**2 for i in range(N)))/N)**0.5
    return rmse

def calc_RMSE_rel(fore,act):
    N = len(fore)
    rmse = ((sum((fore[i]-act[i])**2 / (act[i])**2 for i in range(N))))**0.5
    return rmse

def calc_R_2(fore, act):
    N = len(act)
    mean = np.mean(act)
    zaehler = sum((fore[i]-mean)**2 for i in range(N))
    nenner = sum((act[i]-mean)**2 for i in range(N))
    R_2 = zaehler/nenner
    return R_2

def calc_R_2_alt(fore, act):
    N = len(act)
    mean = np.mean(act)
    zaehler = sum((act[i] - fore[i])**2 for i in range(N))
    nenner = sum((act[i] - mean)**2 for i in range(N))
    R_2 = 1 - (zaehler/nenner)
    return R_2



def calc_MAE(fore, act):
    N = len(fore)
    mae = (sum(abs(fore[i]-act[i]) for i in range(N))) / N
    return mae


#def get_errors(df_forecast, df_actual):
    #result = pd.merge(df_forecast, df_actual, suffixes=["_for", "_act"], left_index=True, right_index=True)

def get_errors(dataframe, stat_for = "Ghi_for", stat_act= "Ghi"):
    list_for = []
    list_act = []
    for i in range(len(dataframe[stat_for])):
        list_for.append(dataframe[stat_for][i])
        list_act.append(dataframe[stat_act][i])

    standard_deviation = calc_SD(list_for, list_act)
    mean_bias_error = calc_MBE(list_for, list_act)
    mean_absolute_error = calc_MAE(list_for,list_act)
    root_mean_squared_error = calc_RMSE(list_for, list_act)
    error_list = [root_mean_squared_error, mean_bias_error, mean_absolute_error, standard_deviation]
    return error_list

def get_errors_relative(dataframe, stat_for = "Ghi_for", stat_act= "Ghi"):
    list_for = []
    list_act = []
    for i in range(len(dataframe[stat_for])):
        list_for.append(dataframe[stat_for][i])

    for n in range(len(dataframe[stat_act])):
        list_act.append(dataframe[stat_act][n])

    average_Ghi = np.mean(list_act)


    standard_deviation = calc_SD(list_for, list_act) / average_Ghi
    mean_biaes_error = calc_MBE(list_for, list_act) / average_Ghi
    mean_absolute_error = calc_MAE(list_for, list_act) / average_Ghi
    root_mean_squared_error = calc_RMSE(list_for, list_act) / average_Ghi
    r_2 = calc_R_2(list_for, list_act)
    #rmse_rel = calc_RMSE_rel(list_for,list_act)

    error_list_relative = [root_mean_squared_error, mean_biaes_error,mean_absolute_error, standard_deviation, r_2]
    return error_list_relative

fore = [1,2,3,4,5,7,8]
act= [2,2,3,4,5,9,6]


R_2 = calc_R_2(fore, act)

R_2_alt = calc_R_2_alt(fore, act)

print(R_2)
print(R_2_alt)