
from email_alert import send_alert_email
from utils import get_exchange_rates , send_twilio_mssg 
from twilio.rest import Client
import keys

# Define the base and foreign currencies to monitor
# base_currency = "USD"
# foreign_currency = "INR"

base_currency = input("Enter the base Currency Eg : 'INR' , 'USD', etc ")

final_alert_message = get_exchange_rates(base_currency)

client = Client(keys.account_sid ,keys.auth_token)  
message = client.messages.create(
    body=final_alert_message,
    from_=keys.twilio_number, to = keys.target_number)

print(message.body)
    
# message = send_twilio_mssg(final_alert_message)
# print(message.body)



# Sample inputs :

# INR
# Y
# 3
# USD
# EUR
# AFN
# 82.60
# 82.55
# 89.0
# 88.9
# 10
# 10

 # Sample Inputs :
# INR
# n
# USD
# 82.60
# 82.55






