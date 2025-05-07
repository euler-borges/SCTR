# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client
from my_secrets import account_sid, auth_token, twilio_number, my_number
import requests.exceptions
import time

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = account_sid
auth_token = auth_token
client = Client(account_sid, auth_token)
print("Twilio client initialized")
time.sleep(5)

try:
    message = client.messages.create(
        body="This is the ship that made the Kessel Run in fourteen parsecs?",
        from_=twilio_number,
        to=my_number,
    )
    print(message.body) 
except requests.exceptions.ConnectionError as e:
    print("Erro de conexão:", e)
except requests.exceptions.RequestException as e:
    print("Erro ao fazer a requisição:", e)
except Exception as e:
    print(f"Esse é o erro: {e}")
