import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


# Function to send an email alert
def send_alert_email(message):
    sender_email = "justforfun55678@gmail.com"
    sender_password = ""
    recipient_email = "dsuman9704@gmail.com"

    subject = "Currency Alert"
    body = message

    # Create an email message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    # Attach the message body
    msg.attach(MIMEText(body, 'plain'))

    # Create a server instance and send the email
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, recipient_email, text)
        server.quit()
        print("Email sent successfully")
    except Exception as e:
        print(f"Email sending failed: {str(e)}")
