import datetime as dt
import functions as fn


today = dt.date.today()
now = dt.datetime.now()
hour = now.hour


#fn.save_solcast_forecast_16h()
#fn.save_solcast_forecast_48h()
fn.save_DWD_forecast_16h()