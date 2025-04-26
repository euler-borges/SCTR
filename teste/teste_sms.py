# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client
from my_secrets import account_sid, auth_token, twilio_number, my_number

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = account_sid
auth_token = auth_token
client = Client(account_sid, auth_token)

message = client.messages.create(
    body="This is the ship that made the Kessel Run in fourteen parsecs?",
    from_=twilio_number,
    to=my_number,
)

print(message.body)