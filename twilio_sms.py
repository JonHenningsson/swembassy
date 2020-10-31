import os
from twilio.rest import Client

def sendSms(to, msg):
    # Your Account SID from twilio.com/console
    account_sid = os.getenv('twilio_account_sid')
    # Your Auth Token from twilio.com/console
    auth_token = os.getenv('twilio_auth_token')
    # From number
    from_no = os.getenv('twilio_from_no')

    client = Client(account_sid, auth_token)
    message = client.messages.create(
        to=to,
        from_=from_no,
        body=msg)

    return message.sid
