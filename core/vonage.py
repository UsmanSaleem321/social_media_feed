import vonage
import os

def send_otp(phone_number, otp):
    client = vonage.Client(key=os.getenv("VONAGE_API_KEY"), secret=os.getenv("VONAGE_API_SECRET"))
    sms = vonage.Sms(client)

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


