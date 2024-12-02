import os
from vonage import Sms, VonageHttpClient

def send_otp(phone_number, otp):
    # Create a client instance with API key and secret
    client = VonageHttpClient(api_key=os.getenv("VONAGE_API_KEY"), api_secret=os.getenv("VONAGE_API_SECRET"))
    sms = Sms(client)

    # Send the SMS message
    response = sms.send_message({
        "from": "YourAppName",
        "to": phone_number,
        "text": f"Your OTP is: {otp}",
    })

    if response["messages"][0]["status"] == "0":
        return True  # OTP sent successfully
    else:
        print(f"Error: {response['messages'][0]['error-text']}")
        return False  # OTP failed
