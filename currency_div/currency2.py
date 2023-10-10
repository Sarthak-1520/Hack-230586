import requests
from twilio.rest import Client
import keys

from email_alert import send_alert_email
from dotenv import load_dotenv,dotenv_values

client = Client(keys.account_sid ,keys.auth_token)
load_dotenv()
# Define the base and foreign currencies to monitor
base_currency = "USD"
foreign_currency = "INR"

# Sample inputs :

# INR
# Y
# 3
# USD
# EUR
# AFN
# 10
# 10
# 10
# 10
# 10
# 10

#  INR
#  n
#  USD
#  82.60
#  82.55

#Take inputs for base_currency and foreign_currency
base_currency = input("Enter the base Currency Eg : 'INR' , 'USD', etc ")
flag = input("Do you want to choose multiple foreign Currencies : [y/n] ")
if(flag=='y' or flag == 'Y'):
    foreign_curr_list = []
    num = int(input("How many foreign currencies do you want to use ? "))
    for i in range(num):
         temp = input(f'Enter foreign currency {i+1} , Eg: {"USD"} , {"EUR"} etc ')
         foreign_curr_list.append(temp)
        # print(i)
        
    upper_threshold_list = []
    lower_threshold_list = []
    for i in range(num):
        temp1 = int(input(f'Enter the upper threshold for {foreign_curr_list[i]} ')) 
        upper_threshold_list.append(temp1)
        temp2 = int(input(f'Enter the lower threshold for {foreign_curr_list[i]} '))
        lower_threshold_list.append(temp2)
        
    # Fetch the latest exchange rate data from an API
    api_url = f"http://data.fixer.io/api/latest?access_key={Exchange_Key}"
    response = requests.get(api_url)
    
    if response.status_code == 200:
        data = response.json()
        print(data)
        
        alert_message_list = []
        final_alert_message = ""
        
        for i in range(num):
            exchange_rate = data['rates'][foreign_curr_list[i]]

            # Check if the exchange rate crosses the thresholds
            if exchange_rate > upper_threshold_list[i]:
                temp = f"Alert: 1 {base_currency} is now more than {foreign_curr_list[i]} {upper_threshold_list[i]}"
                alert_message_list.append(temp)
                # send_alert_email(alert_message)
            elif exchange_rate < lower_threshold_list[i]:
                temp = f"Alert: 1 {base_currency} is now less than {foreign_curr_list[i]} {lower_threshold_list[i]}"
                alert_message_list.append(temp)
                # send_alert_email(alert_message)
        
        
            final_alert_message = final_alert_message + alert_message_list[i] + "\n"   
           
            
        message = client.messages.create(
        body=final_alert_message,
        from_=keys.twilio_number, to = keys.target_number)

        print(message.body)
    else:
        print("Failed to fetch exchange rate data")
        
    
else:
    foreign_currency = input("Enter the foreign Currency ")

    # Set the thresholds for alerts
    upper_threshold = 82.60  # Example: Notify if 1 BASE CURR becomes more than 80 FOREIGN CURR
    lower_threshold = 82.55  # Example: Notify if 1 USD becomes less than 0.80 EUR

    # Take threshold inputs
    # upper_threshold , lower_threshold = int(input("Enter the Upper and Lower thresholds " )).split()
    # upper_threshold = int(upper_threshold)
    # lower_threshold = int(lower_threshold)
    upper_threshold = float(input("Enter the Upper Threshold " ))
    lower_threshold = float(input("Enter the Lower Threshold " ))
    
    # Sample Inputs :
# INR
# n
# USD
# 82.60
# 82.55




    # Fetch the latest exchange rate data from an API
    api_url = f"http://data.fixer.io/api/latest?access_key=95d1b51e9ec3c3d2beb0b7353d6830ad"
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        print(data)
        exchange_rate = data['rates'][foreign_currency]
        # exchange_rate = 0
        # exchange_rate = data['rates'][foreign_currency]

        # Check if the exchange rate crosses the thresholds
        if exchange_rate > upper_threshold:
            alert_message = f"Alert: 1 {base_currency} is now more than {foreign_currency} {upper_threshold}"
            # send_alert_email(alert_message)
        elif exchange_rate < lower_threshold:
            alert_message = f"Alert: 1 {base_currency} is now less than {foreign_currency} {lower_threshold}"
            # send_alert_email(alert_message)
            
        message = client.messages.create(
        body=alert_message,
        from_=keys.twilio_number, to = keys.target_number)

        print(message.body)
    else:
        print("Failed to fetch exchange rate data")



