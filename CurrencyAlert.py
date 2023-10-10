from uagents import Agent, Context
from twilio.rest import Client
import requests

# Initialize the uAgent
alice = Agent(name="alice", seed="alice recovery phrase")

# Twilio credentials
TWILIO_ACCOUNT_SID = 'AC9dbe08a33b8ccedb0c93f654a3b2c0ef'
TWILIO_AUTH_TOKEN = '67f9743973ae33d238f3b9de1df7d57c'
TWILIO_PHONE_NUMBER = '+12564641099'
TO_PHONE_NUMBER = '+919993193578'

# Initialize the Twilio client
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Exchange Rates API configuration
API_KEY = 'c162e89ba3c4dad715caf5faeb3caa36'
BASE_URL = 'https://api.exchangeratesapi.io/v4/latest/'

@alice.on_interval(period=2.0)
async def monitor_exchange_rates(ctx: Context):
    # Connect to the currency exchange API to fetch real-time exchange rates
    response = requests.get(f'{BASE_URL}USD?access_key={API_KEY}')  # Updated API
    data = response.json()

    # Check if the exchange rate crosses the thresholds set by the user
    for currency in data['rates']:
        if data['rates'][currency] > 82.60 and currency == 'INR':  # Replace with the user's thresholds
            # Send an alert
            message = client.messages.create(
                body="Exchange rate alert: 1 USD is more than 82.60 INR",
                from_=TWILIO_PHONE_NUMBER,
                to=TO_PHONE_NUMBER
            )
        elif data['rates'][currency] < 82.55 and currency == 'EUR':  # Replace with the user's thresholds
            # Send an alert
            message = client.messages.create(
                body="Exchange rate alert: 1 USD is less than 82.55 EUR",
                from_=TWILIO_PHONE_NUMBER,
                to=TO_PHONE_NUMBER
            )

if __name__ == "__main__":
    alice.run()
