import requests
import keys
from twilio.rest import Client

def get_inputs():
    flag = input("Do you want to choose multiple foreign Currencies : [y/n] ")
    num = 1 
    if(flag == "n" or flag=="N" ):
        num = 1 
    else:
        num = int(input("How many foreign currencies do you want to use ? "))
    num2 = num    
    foreign_curr_list = []
    for i in range(num):
        temp = input(f'Enter foreign currency {i+1} , Eg: {"USD"} , {"EUR"} etc ')
        foreign_curr_list.append(temp)
        
    upper_threshold_list = []
    lower_threshold_list = []
    for i in range(num):
        temp1 = float(input(f'Enter the upper threshold for {foreign_curr_list[i]} ')) 
        upper_threshold_list.append(temp1)
        temp2 = float(input(f'Enter the lower threshold for {foreign_curr_list[i]} '))
        lower_threshold_list.append(temp2)
        
    return num2 , foreign_curr_list , upper_threshold_list , lower_threshold_list

def get_exchange_rates(num2 ,foreign_curr_list, upper_threshold_list , lower_threshold_list , base_currency):    
    # Fetch the latest exchange rate data from an API
    api_url = f"http://data.fixer.io/api/latest?access_key={keys.access_key}"
    response = requests.get(api_url)
    
    if response.status_code == 200:
        data = response.json()
        print(data)
        
        alert_message_list = []
        final_alert_message = ""
        
        for i in range(num2): 
            a = data['rates'][foreign_curr_list[i]]
            b = data['rates'][foreign_curr_list[i]]
            exchange_rate = b/a

            # Check if the exchange rate crosses the thresholds
            if exchange_rate > upper_threshold_list[i]:
                temp = f"Alert: 1 {base_currency} is now more than {foreign_curr_list[i]} {upper_threshold_list[i]} \n At Present 1 {foreign_curr_list[i]}  = {exchange_rate} "
                alert_message_list.append(temp)
                # send_alert_email(alert_message)
            elif exchange_rate < lower_threshold_list[i]:
                temp = f"Alert: 1 {base_currency} is now less than {foreign_curr_list[i]} {lower_threshold_list[i]} \n At Present 1 {foreign_curr_list[i]}  = {exchange_rate}"
                alert_message_list.append(temp)
                # send_alert_email(alert_message)
    
            
            final_alert_message = final_alert_message + alert_message_list[i] + "\n"   

        print(final_alert_message)
        return final_alert_message
        
        
        
    else:
        print("Failed to fetch exchange rate data")
            
def send_sms_alert( final_alert_message ):  
    client = Client(keys.account_sid ,keys.auth_token)  
    
    message = client.messages.create(
    body=final_alert_message,
    from_=keys.twilio_number, to = keys.target_number)
   

    
 
    