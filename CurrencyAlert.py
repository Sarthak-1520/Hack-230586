from uagents import Agent, Context
from twilio.rest import Client
import requests

# Initialize the uAgent
alice = Agent(name="alice", seed="alice recovery phrase")

# Twilio configuration
TWILIO_ACCOUNT_SID = 'YOUR_TWILIO_ACCOUNT_SID'
TWILIO_AUTH_TOKEN = 'YOUR_TWILIO_AUTH_TOKEN'
TWILIO_PHONE_NUMBER = 'YOUR_TWILIO_PHONE_NUMBER'
TO_PHONE_NUMBER = 'RECIPIENT_PHONE_NUMBER'

# Initialize the Twilio client
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Exchange Rates API configuration
API_KEY = 'YOUR_EXCHANGE_RATES_API_KEY'
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
