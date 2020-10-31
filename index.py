import os
import datetime
from swembassy import getAvailability
from twilio_sms import sendSms

to=os.getenv('twilio_to_no')

officeCodes = {
    'new_york': 'U0766'
    #'washington_dc': 'U1075'
}

dt_now = datetime.datetime.now()
utc_time_now = dt_now.replace(tzinfo = datetime.timezone.utc)
utc_time_future = utc_time_now + datetime.timedelta(weeks=+15)

start = utc_time_now.strftime("%Y-%m-%dT00:00:00+00:00")
end = utc_time_future.strftime("%Y-%m-%dT00:00:00+00:00")

available = []

for o in officeCodes:
    result = getAvailability(officeCodes[o], start, end)
    if result:
        available.append(o)

if available:
    msg = ""
    for a in available:
        msg = msg + a + " "

    msg = "Available: " + msg
    sendSms(to, msg)
