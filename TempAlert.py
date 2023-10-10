# Import necessary libraries
from uagents import Agent, Context
import requests
from twilio.rest import Client
import smtplib
import os 
from dotenv import dotenv_values

config = dotenv_values("config.env")


# Create an agent
alice = Agent(name="alice", seed="alice recovery phrase")

# Set preferred temperature range and location
def set_preferences(min_temp, max_temp, location):
    global MIN_TEMP, MAX_TEMP, LOCATION, BASE_URL
    MIN_TEMP = min_temp
    MAX_TEMP = max_temp
    LOCATION = location
    BASE_URL = f'http://api.openweathermap.org/data/2.5/weather?q={LOCATION}&appid={config['API_KEY']}'

# Connect to a weather API
@alice.on_interval(period=3600)
async def get_weather(ctx: Context):
    response = requests.get(BASE_URL)
    data = response.json()
    ctx.logger.info(f'Current temperature in {LOCATION} is {data["main"]["temp"]-273.15} Celsius')

# Send SMS alert
def send_sms_alert(message):
    client = Client(config['TWILIO_ACCOUNT_SID'], config['TWILIO_AUTH_TOKEN'])
    client.messages.create(to=(config['TO_PHONE_NUMBER'], from_=(config['TWILIO_PHONE_NUMBER'], body=message)



# Check temperature and send alert
@alice.on_interval(period=3600)
async def check_temperature(ctx: Context):
    response = requests.get(BASE_URL)
    data = response.json()
    current_temp = data['main']['temp']-273.15
    if current_temp < MIN_TEMP or current_temp > MAX_TEMP:
        alert_message = f'Temperature Alert! Current temperature in {LOCATION} is {current_temp} Celsius '
        ctx.logger.info(alert_message)
        send_sms_alert(alert_message)
        

# Handle requests from the client script
#@alice.on_message()
#async def handle_request(ctx: Context, sender: str, message: dict):
#    set_preferences(message['min_temp'], message['max_temp'], message['location'])

# Run the agent
if __name__ == "__main__":
    min_temp = float(input("Enter the minimum temperature: "))
    max_temp = float(input("Enter the maximum temperature: "))
    location = input("Enter the location: ")
    set_preferences(min_temp, max_temp, location)
    alice.run()
