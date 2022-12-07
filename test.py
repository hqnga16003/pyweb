from datetime import datetime

from twilio.rest import Client
import keys

client = Client(keys.account_sid, keys.auth_token)
sms = client.messages.create(
    body="alo",
    from_=keys.twilio_number,
    to='+84773346306')

print(sms.body)



today = datetime(2022,1,30).date().today()

print(today)
