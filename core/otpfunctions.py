import nexmo

def send_otp(phone_number, otp):
    client = nexmo.Client (key="fa0d5408", secret="VHZOPwnIq8eCVM6I")
    response =  client.send_message({
        "from": "Vonage",
        "to": phone_number,
        "text": f"Your OTP is: {otp}",
    })
    if response["messages"][0]["status"] == "0":
        return True 
    else:
        return False