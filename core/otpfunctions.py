import os
import vonage
from vonage import Sms, Client

def send_otp(phone_number, otp):
    # Create a client instance with API key and secret
    client =Client(key="fa0d5408", secret="VHZOPwnIq8eCVM6I")
    sms = Sms(client)
    response = sms.send({
        "from": "YourAppName",
        "to": phone_number,
        "text": f"Your OTP is: {otp}",
    })

    if response["messages"][0]["status"] == "0":
        return True  # OTP sent successfully
    else:
        print(f"Error: {response['messages'][0]['error-text']}")
        return False  # OTP failed
