import vonage

def send_otp(phone_number, otp):
    # Initialize the Vonage client
    vonage_client = vonage.Client(key="fa0d5408", secret="VHZOPwnIq8eCVM6I")
    sms = vonage.Sms(vonage_client)

    # Send the SMS message
    response = sms.send_message({
        "from": "Vonage",
        "to": phone_number,
        "text": f"Your OTP is: {otp}",
    })

    # Check the response for status
    if response["messages"][0]["status"] == "0":
        return True  # OTP sent successfully
    else:
        return False  # OTP sending failed
