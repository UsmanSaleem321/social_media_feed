from vonage import Sms

def send_otp(phone_number, otp):
    client = Sms(api_key="fa0d5408", api_secret="VHZOPwnIq8eCVM6I")

    response = client.send_message({
        "from": "Vonage",
        "to": phone_number,
        "text": f"Your OTP is: {otp}",
    })

    if response["messages"][0]["status"] == "0":
        return True  # OTP sent successfully
    else:
        return False  # OTP sending failed

