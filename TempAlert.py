# Import necessary libraries
from uagents import Agent, Context
import requests
from twilio.rest import Client
import smtplib

# Initialize global variables
API_KEY = 'a7778b9d2843b40392c4c57d823424c4'

# Twilio credentials
TWILIO_ACCOUNT_SID = 'AC9dbe08a33b8ccedb0c93f654a3b2c0ef'
TWILIO_AUTH_TOKEN = '67f9743973ae33d238f3b9de1df7d57c'
TWILIO_PHONE_NUMBER = '+12564641099'
TO_PHONE_NUMBER = '+919993193578'

# Email credentials
EMAIL_SENDER = 'email_of_sender'
EMAIL_PASSWORD = 'sender_email_password'
TO_EMAIL_ADDRESS = 'recipient_email_address'

# Create an agent
alice = Agent(name="alice", seed="alice recovery phrase")

# Set preferred temperature range and location
def set_preferences(min_temp, max_temp, location):
    global MIN_TEMP, MAX_TEMP, LOCATION, BASE_URL
    MIN_TEMP = min_temp
    MAX_TEMP = max_temp
    LOCATION = location
    BASE_URL = f'http://api.openweathermap.org/data/2.5/weather?q={LOCATION}&appid={API_KEY}'

# Connect to a weather API
@alice.on_interval(period=3600)
async def get_weather(ctx: Context):
    response = requests.get(BASE_URL)
    data = response.json()
    ctx.logger.info(f'Current temperature in {LOCATION} is {data["main"]["temp"]-273.15} Celsius')

# Send SMS alert
def send_sms_alert(message):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    client.messages.create(to=TO_PHONE_NUMBER, from_=TWILIO_PHONE_NUMBER, body=message)

# Send email alert
def send_email_alert(subject, body):
    message = f'Subject: {subject}\n\n{body}'
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(EMAIL_SENDER, EMAIL_PASSWORD)
    server.sendmail(EMAIL_SENDER, TO_EMAIL_ADDRESS, message)
    server.quit()

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