from datetime import datetime

from twilio.rest import Client
import keys

client = Client(keys.account_sid, keys.auth_token)
sms = client.messages.create(
    body="test1",
    from_=keys.twilio_number,
    to='+84773346306')

print(sms.body)



