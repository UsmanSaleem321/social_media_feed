import vonage
import os
from vonage.http_client import HttpClient
from vonage.client import Client

# Initialize the HTTP client with your Vonage credentials
http_client = HttpClient(application_id=os.getenv("VONAGE_APPLICATION_ID"), private_key=os.getenv("VONAGE_PRIVATE_KEY"))
client = Client(http_client)

def send_otp(phone_number, otp):
    # Initialize the SMS client with the Vonage client
    sms = vonage.Sms(client)

    # Send the OTP message
    response = sms.send_message({
        "from": "YourAppName",
        "to": phone_number,
        "text": f"Your OTP is: {otp}",
    })

    # Check if the message was sent successfully
    if response["messages"][0]["status"] == "0":
        return True  # OTP sent successfully
    else:
        print(f"Error: {response['messages'][0]['error-text']}")
        return False  # OTP failed
