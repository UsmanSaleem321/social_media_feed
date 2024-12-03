from vonage import Sms

def send_otp(phone_number, otp):
    sms = Sms(key="fa0d5408", secret="VHZOPwnIq8eCVM6I")

    response = sms.send_message({
        "from": "Vonage",
        "to": phone_number,
        "text": f"Your OTP is: {otp}",
    })

    if response["messages"][0]["status"] == "0":
        return True  # OTP sent successfully
    else:
        return False  # OTP sending failed