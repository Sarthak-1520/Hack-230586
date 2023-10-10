
from utils import get_exchange_rates , send_sms_alert ,get_inputs
from uagents import Agent, Context



# Define the base currency to monitor
base_currency = input("Enter the base Currency Eg : 'INR' , 'USD', etc ")

num2 , foreign_curr_list , upper_threshold_list , lower_threshold_list = get_inputs()


# Defining an Agent
CurrencyAgent = Agent(name="Curry")

# To send messages in an interval of 3600 seconds
@CurrencyAgent.on_interval(period=3600)
async def check_exchange_rate(ctx: Context):
    final_alert_message = get_exchange_rates(num2 , foreign_curr_list , upper_threshold_list , lower_threshold_list,base_currency)
    send_sms_alert(final_alert_message)

if __name__ == "__main__":
    CurrencyAgent.run()


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






