import datetime
import pytz

def get_est_now():
  utc_now = datetime.datetime.utcnow()
  eastern_tz = pytz.timezone('US/Eastern')
  return utc_now.astimezone(eastern_tz)
